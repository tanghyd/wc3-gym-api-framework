from typing import Any
from gnl_api_framework.model.team import Team
from gnl_api_framework.model.season import Season
from gnl_api_framework.model.map import Map

class Match:
    def __init__(self, data: dict[str, Any]) -> None:
        self.id = data.get('id')
        self.team1_id = data.get('team1_id')
        team1 = data.get('team1')
        if team1:
            team1 = Team(team1)
        self.team1 = team1
        self.team2_id = data.get('team2_id')
        team2 = data.get('team2')
        if team2:
            team2 = Team(team2)
        self.team2 = team2
        self.season_id = data.get('season_id')
        season = data.get('season')
        if season:
            season = Season(season)
        self.season = season
        self.playday = data.get('playday')
        self.date_frame = data.get('date_frame')
        self.fixed_map_id = data.get('fixed_map_id')
        self.fixed_map = None if not data.get('fixed_map') else Map(data.get('fixed_map'))
        self.team1_score = data.get('team1_score')
        self.team2_score = data.get('team2_score')

    def to_dict(self) -> dict[str, Any]:
        return {
            'team1_id': self.team1_id,
            'team2_id': self.team2_id,
            'season_id': self.season_id,
            'playday': self.playday,
            'date_frame': self.date_frame,
            'fixed_map_id': self.fixed_map_id,
            'team1_score': self.team1_score,
            'team2_score': self.team2_score
        }
    
    def __str__(self) -> str:
        return (
            f"Match(id={self.id}, "
            f"team1_id={self.team1_id}, team1={self.team1}, team1_score={self.team1_score} "
            f"team2_id={self.team2_id}, team2={self.team2}, team2_score={self.team2_score} "
            f"season_id={self.season_id}, season={self.season}, playday={self.playday}, "
            f"date_frame={self.date_frame}, fixed_map_id={self.fixed_map_id}, fixed_map={self.fixed_map})"
        )
