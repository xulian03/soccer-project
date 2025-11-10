

from database import RepositoryProvider, PlayerRepository
from services.data_service import DataService
from services.prediction_service import PredictionService
from services.analytics_service import AnalyticsService
from models import Season
import numpy as np

data_service = DataService(PlayerRepository())
prediction_service = PredictionService("stats-models")
df = data_service.load_file(r"data\players.csv")
analytics = AnalyticsService(prediction_service, data_service, df)
prediction = analytics.predict_next_season(player_id="P0", df=df)

# Acceder a las predicciones
print(prediction['predictions']['goals'])  # 25
print(prediction['predictions']['assists'])  # 15
print(prediction['predictions']['score'])  # 8.5

print(prediction)