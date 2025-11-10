from database.csv_repository import CSVRepository
from models import Position
import random
import numpy as np
import time
from datetime import datetime
from faker import Faker
from typing import Dict, Iterable

class DataService:
    def __init__(self, repository=None, seed=42):
        self.repo = repository if repository else CSVRepository(None)
        self.faker = Faker("es_CO")
        random.seed(seed)
        np.random.seed(seed)
        self.seed = seed
        self.positions = [pos.value for pos in Position]

        self.position_profiles = {
            "GK":  {"goal_rate": 0.001, "assist_rate": 0.01, "shots90": 0.005, "clear90": 1.0, "chances90": 0.05, "pass_mean": 80},
            "DFC": {"goal_rate": 0.02,  "assist_rate": 0.02,  "shots90": 0.2, "clear90": 5.0, "chances90": 0.1, "pass_mean": 84},
            "LD":  {"goal_rate": 0.03,  "assist_rate": 0.1,   "shots90": 0.4, "clear90": 3.0, "chances90": 0.8, "pass_mean": 80},
            "LI":  {"goal_rate": 0.03,  "assist_rate": 0.1,   "shots90": 0.4, "clear90": 3.0, "chances90": 0.8, "pass_mean": 80},
            "MCD": {"goal_rate": 0.05,  "assist_rate": 0.05,  "shots90": 0.3, "clear90": 2.5, "chances90": 0.4, "pass_mean": 83},
            "MC":  {"goal_rate": 0.1,  "assist_rate": 0.12,  "shots90": 0.8, "clear90": 1.5, "chances90": 1.0, "pass_mean": 82},
            "MCO": {"goal_rate": 0.15,  "assist_rate": 0.2,   "shots90": 1.2, "clear90": 0.8, "chances90": 1.8, "pass_mean": 80},
            "LW":  {"goal_rate": 0.25,  "assist_rate": 0.25,  "shots90": 1.8, "clear90": 0.6, "chances90": 1.6, "pass_mean": 76},
            "RW":  {"goal_rate": 0.25,  "assist_rate": 0.25,  "shots90": 1.8, "clear90": 0.6, "chances90": 1.6, "pass_mean": 76},
            "DC":  {"goal_rate": 0.4,  "assist_rate": 0.2,  "shots90": 2.5, "clear90": 0.3, "chances90": 1.2, "pass_mean": 70},
        }

    def _clamp(self, v, lo, hi):
        return max(lo, min(hi, v))
    
    def _by_age(self, age):
        avg = 50 * np.exp(-0.5 * ((age - 27) / 6)**2)
        return int(np.clip(np.random.normal(avg, 8), 1, 50))

    def _generate_stats_for_position(self, position, games, age):
        profile = self.position_profiles.get(position, self.position_profiles["MC"])
        starter_minutes = np.random.normal(82, 6)
        minutes = int(round(games * self._clamp(starter_minutes * np.random.uniform(0.6, 1.0), 45, 90)))
        
        if age <= 18:
            minutes = int(minutes * np.random.uniform(0.4, 0.8))
        if games == 0:
            minutes = 0

        goal_rate = profile["goal_rate"]
        assist_rate = profile["assist_rate"]
        shots_per90 = profile["shots90"]
        clearances_per90 = profile["clear90"]
        chances_per90 = profile["chances90"]
        pass_acc_mean = profile["pass_mean"]

        exp_goals = goal_rate * minutes / 90.0
        exp_assists = assist_rate * minutes / 90.0
        exp_shots = shots_per90 * minutes / 90.0
        exp_clear = clearances_per90 * minutes / 90.0
        exp_chances = chances_per90 * minutes / 90.0

        goals = int(np.random.poisson(exp_goals)) if exp_goals > 0 else 0
        assists = int(np.random.poisson(exp_assists)) if exp_assists > 0 else 0
        shots = int(np.random.poisson(exp_shots)) if exp_shots > 0 else 0
        clearances = int(np.random.poisson(exp_clear)) if exp_clear > 0 else 0
        chances_created = int(np.random.poisson(exp_chances)) if exp_chances > 0 else 0

        if shots > 0:
            if position in ("DC", "LW", "RW"):
                s_on_target = np.random.binomial(shots, 0.45)
            elif position in ("MCO", "MC"):
                s_on_target = np.random.binomial(shots, 0.38)
            elif position in ("DFC", "LD", "LI", "MCD"):
                s_on_target = np.random.binomial(shots, 0.28)
            else:
                s_on_target = np.random.binomial(shots, 0.1)
        else:
            s_on_target = 0


        pass_accuracy = float(self._clamp(np.random.normal(pass_acc_mean, 4), 50, 95))
        pre_assists = int(np.random.binomial(chances_created, 0.25)) if chances_created > 0 else 0
        yc = int(np.random.poisson(0.01 * minutes / 90.0 * 10))
        rc = int(np.random.binomial(1, self._clamp(0.002 * minutes / 90.0 + 0.001 * max(0, age - 30), 0, 0.05)))
        injured_avg = np.clip(0.1 * (age - 18), 0, 0.5)
        injured = (50 - games) * injured_avg
        # TODO: Score based in weights by position
        score = random.uniform(5, 10)

        return {
            "games": int(games),
            "minutes": int(minutes),
            "goals": int(max(0, goals)),
            "assists": int(max(0, assists)),
            "pre_assists": int(pre_assists),
            "clearances": int(max(0, clearances)),
            "chances_created": int(max(0, chances_created)),
            "shots": int(max(0, shots)),
            "shots_on_target": int(max(0, s_on_target)),
            "pass_accuracy": round(pass_accuracy, 1),
            "yellow_cards": int(yc),
            "red_cards": int(rc),
            "injured": int(injured),
            "score": round(score, 2)
        }

    def _generate_seasons_for_player(self, player_id: str, min_age: int, max_age) -> Iterable[Dict]:
        teams = ["Real Madrid", "Barcelona", "Bayern Múnich", "Dortmund", "Liverpool", "PSG", 
                 "Sporting Club", "Benfica", "Atletico de Madrid", "Manchester City", "Chelsea", 
                 "Milan", "Inter de Milán", "Arsenal", "Napoli"]
        name = self.faker.name_male()
        
        position = random.choice(self.positions)
        current_team = random.choice(teams)
        team_id = f"T{random.randint(1, 100)}"
        password = "".join(map(str, np.random.randint(0, 10, size=8)))
        now_year = datetime.now().year
        start_year = random.randint(now_year - max_age + min_age, now_year - 1)
        num_seasons = now_year - start_year
        age = random.randint(min_age, max_age - num_seasons + 1) 
        
        for i in range(num_seasons):
            start_year += 1
            age += 1
            
            if random.random() < 0.5:
                current_team = random.choice(teams)
                team_id = f"T{random.randint(1, 100)}"
            
            games = self._games_by(age)
            stats = self._generate_stats_for_position(position, games, age)

            row = {
                "player_id": player_id,
                "player_name": name,
                "age": age,
                "password": password, 
                "position": position,
                "team_id": team_id,
                "team_name": current_team,
                "season_year": start_year,
            }
            row.update(stats)
            yield row

    def generate_data(self, count: int) -> Iterable[Dict]:
        
        for i in range(count):
            player_id = f"P{i}"
            base_age = int(np.random.choice(range(15, 33)))
            for row in self._generate_seasons_for_player(player_id, 15, 28):
                yield row

    def generate_dataset(self, target_rows: int, chunk_size: int = 10000) -> Dict:
        start_time = time.time()
        
        data_generator = self.generate_data(target_rows)
        self.repo.bulk_write_rows(data_generator, chunk_size=chunk_size)
        
        duration = time.time() - start_time
        
        sample_row = next(self.generate_data(1))

        columns = list(sample_row.keys())
        
        return {
            'rows_written': target_rows,
            'duration_s': round(duration, 2),
            'columns': columns
        }

    def load_file(self, path: str):
        import pandas as pd
        
        if path.endswith('.csv'):
            df = pd.read_csv(path)
        elif path.endswith('.json'):
            df = pd.read_json(path)
        elif path.endswith('.xlsx') or path.endswith('.xls'):
            df = pd.read_excel(path)
        elif path.endswith('.txt'):
            df = pd.read_csv(path, sep='\t')
        else:
            raise ValueError(f"Formato no soportado: {path}")
        
        for col in df.columns:
            if 'year' in col.lower() or 'age' in col.lower() or col in ['games', 'goals', 'assists']:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
            elif col in ['minutes', 'shots', 'clearances', 'chances_created', 'yellow_cards', 'red_cards']:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
            elif col in ['pass_accuracy', 'score']:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0.0).astype(float)
        return df

    def clean_data(self, df):
        import pandas as pd
        
        df_clean = df.copy()
        
        numeric_cols = df_clean.select_dtypes(include=['number']).columns
        
        for col in numeric_cols:
            nulls_before = df_clean[col].isnull().sum()
            if nulls_before > 0:
                median_val = df_clean[col].median()
                df_clean[col].fillna(median_val, inplace=True)
        
        categorical_cols = df_clean.select_dtypes(include=['object']).columns
        for col in categorical_cols:
            nulls_before = df_clean[col].isnull().sum()
            if nulls_before > 0:
                mode_val = df_clean[col].mode()[0] if not df_clean[col].mode().empty else 'Unknown'
                df_clean[col].fillna(mode_val, inplace=True)
        
        df_clean['_is_corrupt'] = False
        
        if 'age' in df_clean.columns:
            df_clean.loc[(df_clean['age'] < 15) | (df_clean['age'] > 28), '_is_corrupt'] = True
        
        if 'goals' in df_clean.columns and 'games' in df_clean.columns:
            df_clean.loc[df_clean['goals'] > df_clean['games'] * 3, '_is_corrupt'] = True
        
        return df_clean