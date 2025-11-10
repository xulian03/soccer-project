from models import Season, Player, Coach, Referee, Team
from database import CSVRepository
from database.repository import RepositoryProvider

import os



def test_season_and_player():
    print("Create", "\n")

    player1 = Player("1", name="Lionel Messi", age=36, position="RW")

    season1 = Season(
        "1",
        team=Team("1", "PSG", [], Coach("1", "Luis Enrique", 55)),
        year=2023
    )

    season2 = Season(
        "2",
        team=Team("2", "Inter Miami", [], Coach("2", "Guardiola", 50)),
        year=2024
    )
    player1.add_season(season1)
    player1.add_season(season2)
    print(player1.get_seasons())
    print(player1.serialize())

    RepositoryProvider.get("Player").replace(player1.get_id(), player1)
    
    print(RepositoryProvider.get("Player").find(player1.get_id()).get_seasons())
    

    print("Player:", player1.get_name())
    print("Total seasons:", len(player1.get_seasons()))
    print("First season team:", player1.get_seasons()[0].get_team().get_name())
    print("Las season:", player1.get_latest_season().get_team().get_name())
    print("Serialized player:\n", player1.serialize())


def test_repository():
    print("Save repo", "\n")

    player = Player("2", name="Kylian Mbappé", age=25, position="DC")
    season = Season("3", team="PSG", year=2023)
    player.add_season(season)

    
    RepositoryProvider.get("Player").save(player)
    print(RepositoryProvider.get("Player").findAll())


def test_team():
    print("\n")

    team: Team = RepositoryProvider.get("Team").find("2")
    messi = RepositoryProvider.get("Player").find("1")
    busquets = Player(3, name="Sergio Busquets", age=35, position="MCD")

    team.add_player(messi)
    team.add_player(busquets)

    print("Team name:", team.get_name())
    print("Players in team:", [p.get_name() for p in team.get_players()])


if __name__ == "__main__":
    players_repo = CSVRepository(Player)
    coachs_repo = CSVRepository(Coach)
    teams_repo = CSVRepository(Team)
    referee_repo = CSVRepository(Referee)

    test_season_and_player()
    test_repository()
    test_team()
