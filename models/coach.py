from .user import User
from database import RepositoryProvider

class Coach(User):
    """
    Representa a miembros del cuerpo técnico de un equipo.
    
    Incluye entrenadores, preparadores físicos, staff administrativo, etc.
    El atributo _role permite diferenciar entre los distintos tipos de personal.
    
    Attributes:
    _team (str): ID del equipo al que pertenece (puede ser None al inicio)
    """
    def __init__(self, id, name, age, password=None, team=None):
        """
        Constructor de ClubMember.
        
        Args:
        id (str): Identificador único
        name (str): Nombre completo
        age (int): Edad
        password (str, optional): Contraseña
        team (str, optional): ID del equipo
        """
        super().__init__(id, name, age, password)
        self._team = team
        # Agrega atributos específicos a la lista de serialización
        self._serializable_attr += ["_team"]

    def get_team(self):
        """
        Retorna el objeto Team asociado a este miembro.
        
        Si _team es solo un ID (string), lo convierte en objeto Team
        consultando el repositorio. Esto implementa lazy loading para
        optimizar el uso de memoria.
        
        Returns:
        Team: Objeto del equipo al que pertenece
        """
        if isinstance(self._team, str):
            teams_repo = RepositoryProvider.get("Team")
            self._team = teams_repo.find(self._team)
        return self._team
    
    def set_team(self, team):
        """
        Asigna un equipo a este miembro del club.
        
        Args:
        team (str|Team): ID del equipo u objeto Team
        """
        self._team = team 
    
    def serialize(self):
        """
        Serializa el miembro de club a diccionario.
        
        Convierte el objeto Team a ID para
        permitir almacenamiento en JSON.
        
        Returns:
        dict: Diccionario serializable del jugador
        """
        data = super().serialize()
        # Convierte objeto Team a ID
        data["_team"] = self._team.get_id() if not isinstance(self._team, str) else self._team
        return data