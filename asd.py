from services.data_service import DataService
from services.prediction_service import PredictionService
from services.analytics_service import AnalyticsService
from database import PlayerRepository

# Configurar servicios
data_service = DataService(PlayerRepository())
prediction_service = PredictionService("stats-models")

# Cargar datos
df = data_service.load_file(r"data\players.csv")

print(f"Datos cargados: {len(df)} registros")
print(f"Jugadores únicos: {df['player_id'].nunique()}")
print(f"Equipos únicos: {df['team_id'].nunique()}")
print()

# Inicializar Analytics (esto entrena el modelo)
print("Entrenando modelo...")
analytics = AnalyticsService(prediction_service, data_service, df)
print("Modelo entrenado exitosamente!")
print()

# ======================
# PREDICCIÓN DE JUGADOR
# ======================
try:
    player_id = "P1"  # USAR STRING, no int
    print(f"Prediciendo temporada siguiente para jugador {player_id}...")
    
    prediction = analytics.predict_next_season(player_id=player_id, df=df)
    
    print(f"\nJugador: {prediction['player_name']}")
    print(f"Posición: {prediction['position']}")
    print(f"Equipo: {prediction['team_name']}")
    print(f"Temporada actual: {prediction['current_season']}")
    print(f"Temporada predicha: {prediction['next_season']}")
    print(f"Confianza: {prediction['confidence']:.2%}")
    print("\nPredicciones:")
    print("-" * 40)
    
    for stat, value in prediction['predictions'].items():
        print(f"  {stat:20s}: {value:8.2f}")
    
    # Acceso directo a estadísticas específicas
    print("\n" + "="*40)
    print(f"Goles esperados: {prediction['predictions']['goals']}")
    print(f"Asistencias esperadas: {prediction['predictions']['assists']}")
    print(f"Score esperado: {prediction['predictions']['score']}")
    
except Exception as e:
    print(f"Error al predecir jugador: {e}")

print("\n" + "="*60 + "\n")
