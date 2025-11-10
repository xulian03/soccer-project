from models import User, Player, ClubMember, Referee
from .auth_service import AuthService
from database import RepositoryProvider

class TeamService:
    _instance = None

    def __init__(self):
        self.auth_service: AuthService = AuthService.get_instance()
        self.teams_repo = RepositoryProvider.get("Team")
        self.players_repo = RepositoryProvider.get("Player")

    def create_team(self, team_id, name=None):
        current_user = self.auth_service.get_current_user()
        if not isinstance(current_user, ClubMember) or current_user.get_role() != "coach":
            raise ValueError("No tienes permisos")
        if self.teams_repo.find(team_id):
            raise ValueError("El equipo ya existe")
        team = {"id": team_id, "name": name, "players": []}
        self.teams_repo.save(team)
        return team

    def get_team_info(self, team_id=None):
        team = self.teams_repo.find(team_id) if team_id else None
        if not team:
            return None
        return team

    def add_player_to_team(self, team_id, player_id):
        current_user = self.auth_service.get_current_user()
        if not isinstance(current_user, ClubMember) or current_user.get_role() != "coach":
            raise ValueError("No tienes permisos")
        team = self.teams_repo.find(team_id)
        if not team:
            return False
        player = self.players_repo.find(player_id)
        if not isinstance(player, Player):
            return False
        player.set_team(team)
        self.players_repo.replace(player.get_id(), player)
        return True

    def remove_player_to_team(self, team_id, player_id):
        current_user = self.auth_service.get_current_user()
        if not isinstance(current_user, ClubMember) or current_user.get_role() != "coach":
            raise ValueError("No tienes permisos")
        team = self.teams_repo.find(team_id)
        if not team:
            return False
        player = self.players_repo.find(player_id)
        if not isinstance(player, Player):
            return False
        if player.get_team() and player.get_team().get_id() == team_id:
            player.set_team(None)
            self.players_repo.replace(player.get_id(), player)
            return True
        return False
    
    def set_coach_to_team(self, team_id, coach_id):
        pass

    def get_all_teams(self):
        return self.teams_repo.find_all()

    def get_instance():
        if TeamService._instance is None:
            TeamService._instance = TeamService()
        return TeamService._instance
