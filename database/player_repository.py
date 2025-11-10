from .csv_repository import CSVRepository
from models import Player, Season, Position
from typing import Dict, List

class PlayerRepository(CSVRepository):
    def __init__(self):
        super().__init__(Player)
    
    def save(self, player: Player) -> bool:
        if player is None:
            return False
        
        data = self._load()
        player_id = player.get_id()
        for row in data:
            if row.get("player_id") == player_id:
                return False
        
        rows = self._player_to_rows(player)
        self.bulk_write_rows(rows)
        return True
    
    def replace(self, id: str, player: Player):
        data = self._load()
        data = [row for row in data if row.get("player_id") != id]
        
        rows = self._player_to_rows(player)
        data.extend(rows)
        
        self._save(data)
    
    def delete(self, id: str):
        data = self._load()
        new_data = [row for row in data if row.get("player_id") != id]
        self._save(new_data)
    
    def find(self, player_id: str) -> Player:
        data = self._load()
        player_rows = [row for row in data if row.get("player_id") == player_id]
        
        if not player_rows:
            return None
        
        return self._rows_to_player(player_rows)
    
    def findAll(self) -> List[Player]:
        data = self._load()
        
        players_dict = {}
        for row in data:
            pid = row.get("player_id")
            if pid not in players_dict:
                players_dict[pid] = []
            players_dict[pid].append(row)
        
        players = []
        for player_rows in players_dict.values():
            player = self._rows_to_player(player_rows)
            if player:
                players.append(player)
        
        return players
    
    def _player_to_rows(self, player: Player) -> List[Dict]:
        rows = []
        for season in player.seasons:
            row = {
                "player_id": player.get_id(),
                "player_name": player.name,
                "password": player._password,
                "age": player.age,
                "position": player.position.value if player.position else None,
                "team_name": season.get_team(),
                "season_year": season.get_year(),
            }
            row.update(season._stats)
            rows.append(row)
        
        return rows
    
    def _rows_to_player(self, rows: List[Dict]) -> Player:
        if not rows:
            return None
        
        first_row = rows[0]
        player_id = first_row.get("player_id")
        
        seasons = []
        for row in rows:
            excluded_keys = {"player_id", "player_name", "password", "age", "position", "team_name", "season_year"}
            stats = {k: v for k, v in row.items() if k not in excluded_keys and v != ''}
            
            for k, v in stats.items():
                try:
                    if '.' in str(v):
                        stats[k] = float(v)
                    else:
                        stats[k] = int(v)
                except (ValueError, TypeError):
                    pass
            
            season = Season(
                id=f"{player_id}_{row['season_year']}",
                year=int(row["season_year"]),
                team=row["team_name"],
                stats=stats
            )
            seasons.append(season)
        
        position_value = first_row.get("position")
        return Player(
            id=player_id,
            name=first_row["player_name"],
            password=first_row["password"],
            age=int(first_row["age"]),
            position=Position(position_value) if position_value else None,
            seasons=seasons
        )