from .serializable import Serializable
from .user import User
from database import RepositoryProvider
from enum import Enum

class Position(Enum):
    """
    Enumeración de posiciones válidas en el campo de fútbol.
    
    Garantiza consistencia en los datos y previene errores de tipeo al
    limitar las posiciones a valores predefinidos.
    """
    GK = "GK"   # Portero (Goalkeeper)
    LD = "LD"   # Lateral Derecho
    LI = "LI"   # Lateral Izquierdo
    DFC = "DFC" # Defensa Central
    MCD = "MCD" # Medio Centro Defensivo
    MC = "MC"   # Medio Centro
    LW = "LW"   # Extremo Izquierdo (Left Wing)
    MCO = "MCO" # Medio Centro Ofensivo
    DC = "DC"   # Delantero Centro
    RW = "RW"   # Extremo Derecho (Right Wing)

class Season(Serializable):
    def __init__(
        self,
        id,
        year: int,
        team=None,  
        stats={"games": 0,
        "minutes": 0,
        "goals": 0, 
        "assists": 0,
        "pre_assists": 0,
        "clearances": 0,
        "chances_created": 0, 
        "shots": 0,   
        "shots_on_target": 0,
        "pass_accuracy": 0,
        "yellow_cards": 0,
        "red_cards": 0,
        "injured": 0,
        "score": 0.0}
    ):
        self._id = id
        self._team = team
        self._year = year
        self._stats = stats
        self._serializable_attr = ["_id", "_team", "_year", "_stats"]


    def get_id(self):
        return self._id

    def get_team(self):
        if isinstance(self._team, str):
            teams_repo = RepositoryProvider.get("Team")
            self._team = teams_repo.find(self._team)
        return self._team
    
    def get_stat(self, stat_name: str):
        if not stat_name in self._stats:
            return None
        return self._stats[stat_name]

    def set_state(self, stat_name: str, value):
        self._stats[stat_name] = value

    def get_year(self):
        return self._year
    
    def set_year(self, year):
        self._year = year

    def serialize(self):
        data = super().serialize()
        
        data["_team"] = self._team.get_id() if not isinstance(self._team, str) else self._team
        return data

    @classmethod
    def deserialize(cls, data):
        print(data)
        return super().deserialize(data)


class Player(User):
    def __init__(self, 
                 id,
                 name,
                 age,
                 password=None, 
                 position: Position=None, 
                 seasons=[]):
        super().__init__(id, name, age, password)
        # Maneja conversión automática de string a enum Position
        self._position = position if isinstance(position, Position) else (Position(position) if position else None)
        self._seasons: list[Season] = seasons
        # Registra atributos específicos para serialización
        self._serializable_attr += ["_position", "_seasons"]
        RepositoryProvider.get("Player").save(self)
    
    
    def get_position(self) -> Position | str:
        """
        Retorna la posición del jugador como enum.
        
        Convierte string a enum si es necesario para mantener consistencia.
        
        Returns:
        Position: Posición del jugador
        """
        return Position[self._position] if isinstance(self._position, str) else self._position

    def set_position(self, position):
        """
        Actualiza la posición del jugador.
        
        Args:
        position (Position|str): Nueva posición
        """
        if not isinstance(position, Position) and not position in Position.__members__:
            raise ValueError("Posición inválida")
        self._position = position if isinstance(position, Position) else Position(position)
    
    def get_seasons(self) -> list[Season]:
        return self._seasons

    def add_season(self, season: Season):
        self.get_seasons().append(season)

    def remove_season(self, season: Season):
        self.get_seasons().remove(season)

    def get_latest_season(self):
        return self.get_seasons()[-1]

    def get_season(self, num: int):
        if num <= 0 or len(self.get_seasons()) < num:
            return None
        return self.get_seasons()[num - 1]

    def serialize(self):
        """
        Serializa el jugador a diccionario.
        
        Convierte el enum Position a string y el objeto Team a ID para
        permitir almacenamiento en JSON.
        
        Returns:
        dict: Diccionario serializable del jugador
        """
        data = super().serialize()
        # Convierte enum a valor string
        data["_seasons"] = [s.serialize() for s in self.get_seasons()]
        data["_position"] = self.get_position().value if self.get_position() else None
        return data

    @classmethod
    def deserialize(cls, data: dict):
        """
        Crea un objeto Player desde un diccionario.
        
        Convierte el string de posición de vuelta a enum Position.
        
        Args:
        data (dict): Datos serializados del jugador
            
        Returns:
        Player: Instancia de jugador con datos cargados
        """
        # Convierte string a enum antes de crear el objeto
        if "_position" in data and data["_position"]:
            data["_position"] = Position(data["_position"])
        if "_seasons" in data and data["_seasons"]:
            data["_seasons"] = [Season.deserialize(s) for s in data["_seasons"]]
        return super().deserialize(data)
