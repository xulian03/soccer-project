from models import User, Player, Coach, Referee
from .auth_service import AuthService
from database import RepositoryProvider

class PlayerManagementService:
    _instance = None

    def __init__(self):
        self.auth_service: AuthService = AuthService.get_instance()

    def get_player_stats(self, player_id=None):
        if player_id and isinstance(self.auth_service.get_current_user(), Player):
            raise ValueError("No tienes permisos")
        players_repo = self.auth_service.players_repo
        player = players_repo.find(player_id) if player_id else self.auth_service.get_current_user()
        if not isinstance(player, Player):
            return False
        return player.serialize()
    
    def get_player_profile(self, player_id=None):
        pass

    def update_player_profile(self, player_id=None, **updates):
        current_user = self.auth_service.get_current_user()
        players_repo = self.auth_service.players_repo

        if player_id:
            player = players_repo.find(player_id)
            if not player:
                return False
            if isinstance(current_user, Player):
                raise ValueError("No tienes permisos")
            if player.get_team() != current_user.get_team():
                raise ValueError("No tienes permisos")
        else:
            player = current_user

        if not isinstance(player, Player):
            return False

        player.set_name(updates.get("name"))
        player.set_age(updates.get("age"))
        if updates.get("position"):
            player.set_position(updates.get("position"))

        players_repo.replace(player.get_id(), player)
        return True
    
    def add_season_to_player(self, player_id=None, season_data=None):
        pass

    def get_player_seasons(self, player_id=None):
        pass

    def compute_career_stats(self):
        pass

    def get_all_players(self, team_id=None):
        players_repo = self.auth_service.players_repo
        current_user = self.auth_service.get_current_user()
        if isinstance(current_user, Player):
            raise ValueError("No tienes permisos")
        if isinstance(current_user, Coach):
            if not current_user.get_team():
                return []
            return [p.serialize() for p in players_repo.findAll() if 
                    p.get_team().get_id() == current_user.get_team().get_id()]
        if isinstance(current_user, Referee):
            if team_id:
                return [p.serialize() for p in players_repo.findAll() if p.get_team().get_id() == team_id]
            return [p.serialize() for p in players_repo.findAll()]

        raise ValueError("No tienes permisos")


    def search_players(self, filters):
        players_repo = self.auth_service.players_repo
        current_user = self.auth_service.get_current_user()

        if isinstance(current_user, Player):
            raise ValueError("No tienes permisos")

        if isinstance(current_user, (Coach, Referee)):
            players = players_repo.findAll()
            results = []
            for p in players:
                match = True
                for key, value in filters.items():
                    if getattr(p, key, None) != value:
                        match = False
                        break
                if match:
                    results.append(p.serialize())
            return results

        raise ValueError("No tienes permisos")


    def get_instance():
        if PlayerManagementService._instance is None:
            PlayerManagementService._instance = PlayerManagementService()
        return PlayerManagementService._instance