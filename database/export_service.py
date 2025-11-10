import pandas as pd
from models import Serializable

class ExportService:

    def __init__(self):
        pass

    def export_to_json(self, data, filename):
        df = self.convert_to_df(data)
        df.to_json(filename)

    def export_to_csv(self, data, filename):
        df = self.convert_to_df(data)
        df.to_csv(filename, index=False)

    def export_to_excel(self, data, filename):
        pass

    def convert_to_df(self, data: list[Serializable]):
        if not data:
            return pd.DataFrame()
        df = pd.DataFrame([s.serialize() for s in data])
        return df