from .serializable import Serializable
from database import RepositoryProvider

class Team(Serializable):
    """
    Representa un equipo de fútbol en el sistema.
    
    Agrupa jugadores bajo la supervisión de un entrenador y permite
    gestionar la organización del personal técnico. Es fundamental para
    el control de permisos (usuarios solo pueden ver información de su equipo).
    
    Attributes:
    _id (str): Identificador único del equipo
    _name (str): Nombre del equipo
    coach (str): ID del entrenador principal
    players (list): Lista de IDs de jugadores
    staff (list): Lista de IDs del personal técnico
    """
    def __init__(self, id, name, players=[], coach=None):
        """
        Constructor de Team.
        
        Args:
        id (str): Identificador único
        name (str): Nombre del equipo
        coach (str, optional): ID del entrenador
        players (list, optional): Lista de IDs de jugadores
        staff (list, optional): Lista de IDs del staff
        """
        self._id = id
        self._name = name
        self.coach = coach
        self.players = players or []
        self._serializable_attr = ["_id", "_name", "coach", "players"]
        self.get_coach().set_team(self)
        RepositoryProvider.get("Coach").save(self.coach)
        RepositoryProvider.get("Team").save(self)

    def get_id(self):
        """Retorna el ID del equipo."""
        return self._id

    def get_name(self):
        """Retorna el nombre del equipo."""
        return self._name

    def set_name(self, name):
        """
        Actualiza el nombre del equipo.
        
        Args:
        name (str): Nuevo nombre
        """
        self._name = name

    def get_coach(self):
        """Retorna el ID o objeto del entrenador del equipo."""
        if isinstance(self.coach, str):
            self.coach = RepositoryProvider.get('Coach').find(self.coach)
        return self.coach

    def set_coach(self, coach_id):
        """
        Asigna un entrenador al equipo.
        
        Args:
        coach_id (str): ID del entrenador
        """
        self.coach = coach_id

    def get_players(self) -> list:
        """
        Retorna la lista de jugadores del equipo.
        
        Si los jugadores están almacenados como IDs, los convierte en
        objetos Player consultando el repositorio (lazy loading).
        
        Returns:
        list: Lista de objetos Player
        """
        if len(self.players) > 0 and isinstance(self.players[0], str):
            players_repo = RepositoryProvider.get("Player")
            self.players = [players_repo.find(player) for player in self.players]
        return self.players

    def add_player(self, player):
        """
        Agrega un jugador al equipo.
        
        Args:
        player (str|Player): ID del jugador u objeto Player
            
        Note:
        Previene duplicados verificando si el jugador ya existe
        """
        if player not in self.players:
            self.players.append(player)

    def remove_player(self, player_id):
        """
        Elimina un jugador del equipo.
        
        Args:
        player_id (str): ID del jugador a eliminar
        """
        if player_id in self.players:
            self.players.remove(player_id)

    def serialize(self):
        """
        Serializa el equipo a diccionario.
        
        Convierte objetos anidados (coach, players, staff) a sus IDs
        para evitar serialización recursiva infinita.
        
        Returns:
        dict: Diccionario serializable del equipo
        """
        data = super().serialize()
        # Convierte objetos a IDs si es necesario
        data["coach"] = self.coach.get_id() if not isinstance(self.coach, str) else self.coach
        data["players"] = [p.get_id() if not isinstance(p, str) else p for p in self.players]
        return data