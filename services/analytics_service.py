import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from .prediction_service import PredictionService, RandomForestPredictor
from .data_service import DataService

class AnalyticsService:
    def __init__(self, prediction_service, data_service, player_data: pd.DataFrame):
        self.predictor = prediction_service
        self.data_service = data_service
        
        self.stats_to_predict = [
            'score', 'goals', 'assists', 'pre_assists', 'clearances',
            'chances_created', 'shots', 'shots_on_target', 
            'pass_accuracy', 'yellow_cards', 'red_cards'
        ]
        
        training_data = self._prepare_training_data(player_data)
        
        # Registrar y entrenar UN SOLO modelo multi-output
        self.predictor.register_predictor("random-forest", RandomForestPredictor(100))
        
        # Filtrar solo las stats que existen
        available_stats = [s for s in self.stats_to_predict if s in training_data.columns]
        self.stats_to_predict = available_stats
        
        # Separar X e y (y es DataFrame con todas las stats)
        X = training_data.drop(columns=self.stats_to_predict)
        y = training_data[self.stats_to_predict]
        
        # Entrenar con multi-output
        self.predictor.load_predictor("random-forest")
    
    def _prepare_training_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Convierte historial de temporadas en features agregadas
        Cada fila representa: historial de N temporadas -> stats de temporada N+1
        """
        rows = []
        
        # Reset index si player_id está como índice
        if df.index.name == 'player_id':
            df = df.reset_index()
        
        for player_id in df['player_id'].unique():
            player_data = df[df['player_id'] == player_id].sort_values('season_year')
            
            # Necesitamos al menos 2 temporadas (una para features, otra para target)
            if len(player_data) < 2:
                continue
            
            # Crear ejemplos: usar temporadas 0 a i-1 para predecir temporada i
            for i in range(1, len(player_data)):
                historical = player_data.iloc[:i]
                target = player_data.iloc[i]
                
                # Crear features del historial
                row = self._create_features(historical)
                
                # Agregar todas las stats como target
                for stat in self.stats_to_predict:
                    if stat in target:
                        row[stat] = target[stat]
                
                rows.append(row)
        
        return pd.DataFrame(rows)
    
    def _create_features(self, history: pd.DataFrame):
        """
        Crea features a partir del historial de temporadas de un jugador
        """
        features = {}
        
        # Última temporada (más reciente)
        last = history.iloc[-1]
        features['last_score'] = last['score']
        features['last_goals'] = last['goals']
        features['last_assists'] = last['assists']
        features['last_games'] = last['games']
        features['last_minutes'] = last['minutes']
        features['age'] = last['age']
        
        # Promedios históricos
        features['avg_score'] = history['score'].mean()
        features['avg_goals'] = history['goals'].mean()
        features['avg_assists'] = history['assists'].mean()
        features['avg_games'] = history['games'].mean()
        
        # Número de temporadas jugadas
        features['seasons_count'] = len(history)
        
        # Tendencia (diferencia entre última y primera temporada)
        if len(history) >= 2:
            features['score_trend'] = history['score'].iloc[-1] - history['score'].iloc[0]
            features['goals_trend'] = history['goals'].iloc[-1] - history['goals'].iloc[0]
        else:
            features['score_trend'] = 0
            features['goals_trend'] = 0
        
        # Consistencia (desviación estándar)
        features['score_std'] = history['score'].std() if len(history) > 1 else 0
        
        # Posición (encoding simple)
        position_map = {'GK': 1, 'DEF': 2, 'MID': 3, 'FWD': 4}
        features['position'] = position_map.get(last['position'], 0)
        
        return features
    
    def predict_next_season(self, player_id: str, df: pd.DataFrame):
        """
        Predice las estadísticas de la siguiente temporada para un jugador
        
        Args:
            player_id: ID del jugador (puede ser string o int)
            df: DataFrame con el historial del jugador
        """
        if df.index.name == 'player_id':
            df = df.reset_index()
        
        player_history = df[df['player_id'] == player_id].sort_values('season_year')
        
        if len(player_history) == 0:
            raise ValueError(f"Jugador {player_id} no encontrado")
        
        features = self._create_features(player_history)
        features_df = pd.DataFrame([features])
        
        # Predecir con modelo multi-output
        result = self.predictor.predict_for_player("random-forest", features_df)
        
        # Convertir predicciones array 2D a dict
        predictions = {}
        preds_array = result['predictions'][0]  # Primera fila
        for i, stat in enumerate(self.stats_to_predict):
            predictions[stat] = round(float(preds_array[i]), 2)
        
        return {
            'player_id': player_id,
            'player_name': player_history.iloc[-1]['player_name'],
            'position': player_history.iloc[-1]['position'],
            'team_name': player_history.iloc[-1]['team_name'],
            'current_season': int(player_history['season_year'].max()),
            'next_season': int(player_history['season_year'].max() + 1),
            'predictions': predictions,
            'confidence': result['confidence']
        }
    
    def predict_team_next_season(self, team_id: str, df: pd.DataFrame):
        """
        Predice las estadísticas agregadas de un equipo para la siguiente temporada
        
        Args:
            team_id: ID del equipo
            df: DataFrame con datos de jugadores
        """
        if df.index.name == 'player_id':
            df = df.reset_index()
        
        # Obtener jugadores del equipo en la última temporada
        latest_season = df['season_year'].max()
        team_players = df[(df['team_id'] == team_id) & (df['season_year'] == latest_season)]
        
        if len(team_players) == 0:
            raise ValueError(f"Equipo {team_id} no encontrado")
        
        team_name = team_players.iloc[0]['team_name']
        
        # Predecir para cada jugador y agregar
        team_predictions = {stat: 0.0 for stat in self.stats_to_predict}
        successful_predictions = 0
        player_predictions = []
        
        for player_id in team_players['player_id'].unique():
            try:
                pred = self.predict_next_season(player_id, df)
                player_predictions.append(pred)
                
                for stat in self.stats_to_predict:
                    team_predictions[stat] += pred['predictions'][stat]
                
                successful_predictions += 1
            except Exception as e:
                # Si un jugador no tiene suficiente historial, lo saltamos
                print(f"Warning: No se pudo predecir para jugador {player_id}: {e}")
                continue
        
        # Redondear totales
        for stat in team_predictions:
            team_predictions[stat] = round(team_predictions[stat], 2)
        
        return {
            'team_id': team_id,
            'team_name': team_name,
            'current_season': int(latest_season),
            'next_season': int(latest_season + 1),
            'players_predicted': successful_predictions,
            'total_predictions': team_predictions,
            'player_predictions': player_predictions
        }