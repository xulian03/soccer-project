from models import User
from database import RepositoryProvider

class ReportService:
    _instance = None

    def __init__(self):
        pass

    def generate_player_report():
        pass

    def generate_team_report():
        pass

    def format_report_header():
        pass

    def get_instance():
        if ReportService._instance is None:
            ReportService._instance = ReportService()
        return ReportService._instance