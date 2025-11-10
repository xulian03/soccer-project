from .repository import Repository, RepositoryProvider
from models import Serializable
from typing import Dict, Iterable
import csv
import os
import threading

class CSVRepository(Repository):
    def __init__(self, cls: Serializable):
        self.cls = cls
        self._lock = threading.Lock()
        folder = "data"
        os.makedirs(folder, exist_ok=True)
        self.filename = os.path.join(folder, f"{cls.__name__.lower()}s.csv")
        if not os.path.exists(self.filename):
            with open(self.filename, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([])
        RepositoryProvider.register(cls.__name__.capitalize(), self)
    
    def _load(self):
        data = []
        with open(self.filename, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append(row)
        return data

    def _save(self, data):
        if not data:
            with open(self.filename, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([])
            return
        
        fieldnames = data[0].keys()
        with open(self.filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)

    def _read_all(self):
        try:
            return self._load()
        except (FileNotFoundError, csv.Error):
            return []

    def find(self, id):
        data = self._load()
        for element in data:
            if element.get("_id") == id:
                return self.cls.deserialize(element)
        return None
    
    def findAll(self):
        return [self.cls.deserialize(element) for element in self._load()]

    def save(self, element):
        if element == None:
            return False
        data = self._load()
        id = element.get_id()
        print(element.get_id())
        for e in data:
            if e.get("_id") == id:
                return False
        data.append(element.serialize())
        self._save(data)
        return True

    def delete(self, id):
        data = self._load()
        new_data = [d for d in data if d.get("_id") != id]
        self._save(new_data)

    def replace(self, id, element):
        data = self._load()
        for i, d in enumerate(data):
            if d.get("_id") == id:
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
                    self._save(existing)
                    buf = []
            if buf:
                existing.extend(buf)
                self._save(existing)