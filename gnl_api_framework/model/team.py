from typing import Any
from gnl_api_framework.model.user import User
from gnl_api_framework.model.season_info import SeasonInfo

class Team:
    def __init__(self, data: dict[str, Any]) -> None:
        self.id = data.get('id')
        self.name = data.get('name')
        self.icon = data.get('icon')
        self.discord_role = data.get('discord_role')
        players = data.get('player_by_season')
        pl = {}
        if players:
            for season_id, player in players.items():
                for p in player:
                    pl[season_id] = User(p)
        self.players_by_season = pl

        seasons_info = data.get('seasons_info')
        if seasons_info:
            seasons_info = [SeasonInfo(seasons_info) for seasons_info in seasons_info]
        self.seasons_info = seasons_info

    def to_dict(self) -> dict[str, Any]:
        return {
            'name': self.name,
            'icon' : self.icon,
            'discord_role' : self.discord_role
        }

    def __str__(self) -> str:
        players_by_season_str = None
        if self.players_by_season:
            players_by_season_str = ", ".join(
                f"{season_id}: {player}" for season_id, player in self.players_by_season.items()
            )
        seasons_info_str = ", ".join(str(season_info) for season_info in self.seasons_info) if self.seasons_info else None
        return (
            f"Team(id={self.id}, name={self.name}, icon={self.icon}, discord_role={self.discord_role} "
            f"players_by_season={{ {players_by_season_str} }}, "
            f"seasons_info=[{seasons_info_str}])"
        )
