from typing import Dict, Iterable
from .repository import Repository, RepositoryProvider
from models import Serializable
import json
import os

class JSONRepository(Repository):
    def __init__(self, cls: Serializable):
        self.cls = cls
        folder = "data"
        os.makedirs(folder, exist_ok=True)
        self.filename = os.path.join(folder, f"{cls.__name__.lower()}s.json")
        if not os.path.exists(self.filename):
            with open(self.filename, "w") as f:
                json.dump([], f)
        RepositoryProvider.register(cls.__name__.capitalize(), self)
    
    def _load(self):
        with open(self.filename, "r") as f:
            return json.load(f)

    def _save(self, data):
        with open(self.filename, "w") as f:
            json.dump(data, f, indent=2)

    def find(self, id):
        data = self._load()
        for element in data:
        
            if element["_id"] == id:
                return self.cls.deserialize(element)
        return None
    
    def findAll(self):
        return [self.cls.deserialize(element) for element in self._load()]

    def save(self, element):
        if element == None:
            return False
        data: list = self._load()
        id = element.get_id()
        print(element.get_id())
        for e in data:
            if e["_id"] == id:
                return False
        data.append(element.serialize())
        
        self._save(data)
        return True

    def delete(self, id):
        data = self._load()
        new_data = [d for d in data if d["_id"] != id]
        self._save(new_data)

    def replace(self, id, element):
        data = self._load()
        for i, d in enumerate(data):
            if d["_id"] == id:
                data[i] = element.serialize()
                break
        self._save(data)

    def bulk_write_rows(self, row_iterable: Iterable[Dict], chunk_size: int = 10000) -> None:
        with self._lock:
            existing = self._read_all()
            buf = []
            count = 0
            for row in row_iterable:
                buf.append(row)
                count += 1
                if len(buf) >= chunk_size:
                    existing.extend(buf)
                    with open(self.filename, "w", encoding="utf-8") as f:
                        json.dump(existing, f, ensure_ascii=False)
                    buf = []
            if buf:
                existing.extend(buf)
                with open(self.filename, "w", encoding="utf-8") as f:
                    json.dump(existing, f, ensure_ascii=False)