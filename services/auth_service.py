from models import User, Coach, Player, Referee
from database import RepositoryProvider

class AuthService:
    _instance = None

    def __init__(self):
        self.players_repo = RepositoryProvider.get("Player")
        self.coachs_repo = RepositoryProvider.get("Coach")
        self.referee_repo = RepositoryProvider.get("Referee")
        self.teams_repo = RepositoryProvider.get("Team")
        self._current_user = None

    def register_player(self, id, name, age, password, team_id, position):
        if self._current_user:
            return None
        if self.players_repo.find(id):
            raise ValueError("El usuario ya existe")
        
        if age <= 0:
            raise ValueError("Edad inválida")

        team = self.teams_repo.find(team_id) if team_id != None else None
        player = Player(id, name, age, password, team, position)
        self.players_repo.save(player)
        self._current_user = player
        return player

    def register_coach(self, id, password, name, age):
        if self._current_user:
            return None
        
        if self.coachs_repo.find(id):
            raise ValueError("El usuario ya existe")
        
        if age <= 0:
            raise ValueError("Edad inválida")

        club_member = Coach(id, name, age, password, None)
        self.coachs_repo.save(club_member)
        self._current_user = club_member
        return club_member

    def register_referee(self, id, password, name, age, license):
        if self._current_user:
            return None
        
        if self.referee_repo.find(id):
            raise ValueError("El usuario ya existe")
        
        if age <= 0:
            raise ValueError("Edad inválida")

        ref = Referee(id, name, age, password, license)
        self.referee_repo.save(ref)
        self._current_user = ref
        return ref

    def login(self, id, password, user_type: str):
        if self._current_user:
            return False
        user: User = None
        match user_type.lower():
            case "player":
                user = self.players_repo.find(id)
            case "coach":
                user = self.coachs_repo.find(id)
            case "referee":
                user = self.referee_repo.find(id)
            case _:
                return False
        if not user:
            return False
        if user.verify_password(password):
            self._current_user = user
            return True


    def get_current_user(self):
        return self._current_user
    
    def set_current_user(self, user):
        self._current_user = user

    def update_user_profile(self, name, age, user_id=None):
        user = None
        if not user_id:
             user = self._current_user
        else:
            user = self.players_repo.find(user_id)
            if user is None:
                user = self.coachs_repo.find(user_id)
            if user is None:
                user = self.referee_repo.find(user_id)

        if user is None:
            return False

        if name:
            user.set_name(name)
        if age:
            user.set_age(age)

        if isinstance(user, Player):
            self.players_repo.replace(user.get_id(), user)
        elif isinstance(user, Coach):
            self.coachs_repo.replace(user.get_id(), user)
        elif isinstance(user, Referee):
            self.referee_repo.replace(user.get_id(), user)
        return True

    def logout(self):
        user = self._current_user
        if user:
            if isinstance(user, Player):
                self.players_repo.replace(user.get_id(), user)
            elif isinstance(user, Coach):
                self.coachs_repo.replace(user.get_id(), user)
            elif isinstance(user, Referee):
                self.referee_repo.replace(user.get_id(), user)
            self._current_user = None
            return True
        return False

    def get_instance():
        if AuthService._instance is None:
            AuthService._instance = AuthService()
        return AuthService._instance