from typing import Any
from gnl_api_framework.model.team import Team
from gnl_api_framework.model.user import User
from gnl_api_framework.model.season import Season

class FantasyTeam:
    def __init__(self, data: dict[str, Any]) -> None:
        self.id = data.get('id')
        self.name = data.get('name')
        self.season_id = data.get('season_id')
        season = data.get('season')
        if season:
            season = Season(season)
        self.season = season
        self.captain_id = data.get('captain_id')
        captain = data.get('captain')
        if captain:
            captain = User(captain)
        self.captain = captain
        self.drafted_team_id = data.get('drafted_team_id')
        drafted_team = data.get('drafted_team')
        if drafted_team:
            drafted_team = Team(drafted_team)
        self.drafted_team = drafted_team
        self.drafted_race = data.get('drafted_race')
        drafted_players = data.get('drafted_players')
        if drafted_players:
            drafted_players = [User(p) for p in drafted_players]
        self.drafted_players = drafted_players
        self.player_points = data.get('player_points')
        self.bench_points = data.get('bench_points')
        self.team_points = data.get('team_points')
        self.race_points = data.get('race_points')
        self.bet_points = data.get('bet_points')
        self.total_points = data.get('total_points')

    def to_dict(self) -> dict[str, Any]:
        return {
            'id': self.id,
            'name': self.name,
            'season_id': self.season_id,
            'captain_id': self.captain_id,
            'drafted_team_id': self.drafted_team_id,
            'drafted_race': self.drafted_race,
            'player_points': self.player_points,
            'bench_points': self.bench_points,
            'team_points': self.team_points,
            'race_points': self.race_points,
            'bet_points': self.bet_points,
            'total_points': self.total_points
        }
    
    def __str__(self) -> str:
        drafted_players_str = ", ".join(str(player) for player in self.drafted_players) if self.drafted_players else None
        return (
            f"FantasyTeam(id={self.id}, name={self.name}, "
            f"captain={str(self.captain)}, "
            f"captain={str(self.drafted_team)}, "
            f"drafted_players=[{drafted_players_str}], "
            f"drafted_race={self.drafted_race}, "
            f"season={str(self.season)})"
            f"player_points={self.player_points}, "
            f"bench_points={self.bench_points}, "
            f"team_points={self.team_points}, "
            f"race_points={self.race_points}, "
            f"total_points={self.total_points}, "
        )
