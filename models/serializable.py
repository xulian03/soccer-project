from abc import ABC, abstractmethod

class Serializable(ABC):
    """
    Clase abstracta base para las entidades del sistema que deben almacenarse en JSON.
    
    Ofrece métodos de serialización y deserialización para convertir objetos en diccionarios 
    y reconstruirlos después, lo que permite manejar de forma sencilla el guardado y la carga 
    de datos.
    """

    @abstractmethod
    def get_id(self):
        """
        Método abstracto que debe ser implementado por todas las clases hijas.
        Retorna el identificador único de la entidad.
        """
        pass

    def serialize(self):
        """
        Convierte el objeto en un diccionario listo para guardar.

        Se basa en el atributo _serializable_attr, que cada clase define para indicar qué campos deben incluirse.

        Returns:
        dict: Diccionario con los atributos seleccionados del objeto.
        """
        return {attr: getattr(self, attr) for attr in self._serializable_attr}
    
    @classmethod
    def deserialize(cls, data: dict):
        """
        Crea una instancia de la clase a partir de un diccionario.
        
        Remueve los guiones bajos de las claves para hacerlas compatibles
        con los parámetros del constructor.
        
        Args:
        data (dict): Diccionario con los datos del objeto
            
        Returns:
        Instancia de la clase con los datos cargados
        """
        # Remueve el underscore inicial de las claves para que coincidan
        # con los nombres de parámetros del constructor
        clean_data = {k.lstrip("_"): v for k, v in data.items()}
        obj = cls(**clean_data)
        # Preserva la lista de atributos serializables si no existe
        if not hasattr(obj, "_serializable_attr"):
            obj._serializable_attr = list(data.keys())
        return obj