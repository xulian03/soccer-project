from abc import ABC, abstractmethod
import numpy as np
import pandas as pd
from typing import Any, Dict
from utils.model_loader import save_model, load_model
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
import os
from sklearn.metrics import mean_squared_error

class Predictor(ABC):

    @abstractmethod
    def train(self, X: pd.DataFrame, y: pd.Series) -> Any:
        pass

    @abstractmethod
    def predict(self, X: pd.DataFrame) -> np.ndarray:
        pass

    @abstractmethod
    def save(self, path: str) -> None:
        pass

    @abstractmethod
    def load(self, path: str) -> None:
        pass

class BaselinePredictor(Predictor):

    def __init__(self):
        self.mean_ = None

    def train(self, X, y):
        self.mean_ = float(y.mean())
        return self.mean_
    
    def predict(self, X):
        return np.full((len(X),), self.mean_)
    
    def save(self, path):
        save_model({"mean": self.mean_}, path)

    def load(self, path):
        data = load_model(path)
        self.mean_ = data["mean"]

class LinearRegressorPredictor(Predictor):
    def __init__(self):
        self.model = LinearRegression()

    def train(self, X, y):
        self.model.fit(X, y)
        return self
    
    def predict(self, X):
        return self.model.predict(X)
    
    def save(self, path):
        save_model(self.model, path)

    def load(self, path):
        self.model = load_model(path)

class RandomForestPredictor(Predictor):

    def __init__(self, n_estimators=100):
        self.model = RandomForestRegressor(n_estimators=n_estimators, n_jobs=-1)

    def train(self, X, y):
        self.model.fit(X, y)
        return self
    
    def predict(self, X):
        return self.model.predict(X)
    
    def save(self, path):
        save_model(self.model, path)
        
    def load(self, path):
        self.model = load_model(path)

class PredictionService:
    def __init__(self, model_dir: str = "models"):
        self.models = {}
        self.model_dir = model_dir

    def register_predictor(self, name: str, predictor: Predictor):
        self.models[name] = predictor

    def load_predictor(self, name):
        if not name in self.models:
            return False
        path = os.path.join(self.model_dir, f"{name}.joblib")
        self.models[name].load(path)

    def train_predictor(self, name: str, df: pd.DataFrame, target: str) -> Dict:
        if name not in self.models:
            raise KeyError(name)
        model = self.models[name]
        X = df.drop(columns=[target])
        X = X.select_dtypes(include=["number"]).fillna(0)
        y = df[target]
        model.train(X, y)
        path = os.path.join(self.model_dir, f"{name}.joblib")
        model.save(path)
        preds = model.predict(X)
        mse = float(mean_squared_error(y, preds))
        return {"model_id": name, "metrics": {"mse": mse}, "path": path}
    
    def train_predictor_multi(self, name: str, X: pd.DataFrame, y: pd.DataFrame) -> Dict:
        if name not in self.models:
            raise KeyError(name)
        model = self.models[name]
        model.train(X, y)  # y es DataFrame, no Series
        
        path = os.path.join(self.model_dir, f"{name}.joblib")
        model.save(path)
        
        preds = model.predict(X)
        mse = float(mean_squared_error(y, preds))
        return {"model_id": name, "metrics": {"mse": mse}, "path": path}
    
    
    def predict_for_player(self, model_name: str, player_seasons: pd.DataFrame) -> Dict:
        if model_name not in self.models:
            raise KeyError(model_name)
        model = self.models[model_name]
        X = player_seasons.select_dtypes(include=["number"]).fillna(0)
        preds = model.predict(X)
        conf = float(1.0 / (1.0 + float(X.std().mean() if X.shape[1] else 0)))
        return {"predictions": preds, "confidence": conf}  # preds es array 2D para multi-output