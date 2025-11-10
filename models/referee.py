from .user import User

class Referee(User):
    """
    Representa a un árbitro del sistema.
    
    Los árbitros tienen permisos especiales para validar estadísticas de
    partidos y acceder a información de todos los equipos y jugadores.
    
    Attributes:
    _license (str): Número de licencia único que identifica al árbitro
    """
    def __init__(self, id, name, age, password=None, license=None):
        """
        Constructor de Referee.
        
        Args:
        id (str): Identificador único
        name (str): Nombre completo
        age (int): Edad
        password (str, optional): Contraseña
        license (str, optional): Número de licencia único
        """
        super().__init__(id, name, age, password)
        self._license = license
        self._serializable_attr += ["_license"]

    def get_license(self):
        """Retorna el número de licencia del árbitro."""
        return self._license
    
    def set_license(self, license):
        """
        Actualiza el número de licencia.
        
        Args:
        license (str): Nueva licencia
        """
        self._license = license