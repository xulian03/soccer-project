from .serializable import Serializable 

class User(Serializable):
    """
    Clase base para todos los tipos de usuario del sistema.
    
    Centraliza atributos y funcionalidad común a jugadores, entrenadores y
    árbitros, evitando duplicación de código y facilitando la autenticación.
    
    Attributes:
    _id (str): Identificador único del usuario
    _name (str): Nombre completo del usuario
    _age (int): Edad del usuario
    _password (str): Contraseña del usuario (debe ser encriptada antes de almacenar)
    """
    def __init__(self, id, name, age, password=None):
        """
        Constructor de la clase User.
        
        Args:
        id (str): Identificador único
        name (str): Nombre completo
        age (int): Edad del usuario
        password (str, optional): Contraseña. Por defecto None
        """
        self._id = id
        self._name = name
        self._age = age
        self._password = password
        # Define qué atributos se incluirán en la serialización
        self._serializable_attr = ["_id", "_name", "_age", "_password"]

    def get_id(self):
        """Retorna el ID único del usuario."""
        return self._id

    def get_name(self):
        """Retorna el nombre del usuario."""
        return self._name
    
    def get_age(self):
        """Retorna la edad del usuario."""
        return self._age
    
    def set_name(self, name):
        """
        Actualiza el nombre del usuario.
        
        Args:
        name (str): Nuevo nombre
        """
        self._name = name
    
    def set_age(self, age):
        """
        Actualiza la edad del usuario.
        
        Args:
        age (int): Nueva edad
        """
        self._age = age
    
    def verify_password(self, password):
        """
        Verifica si la contraseña proporcionada coincide con la almacenada.
        
        Args:
        password (str): Contraseña a verificar
            
        Returns:
        bool: True si las contraseñas coinciden, False en caso contrario
        """
        return self._password == password