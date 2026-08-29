from typing import Any
from gnl_api_framework.model.season import Season
class SeasonInfo:
    def __init__(self, data: dict[str, Any]) -> None:
        self.season_id = data.get('season_id')
        self.final_score = data.get('final_score')
        self.points_available = data.get('points_available')
        self.points_against = data.get('points_against')
        season = data.get('season')
        if season:
            season = Season(season)
        self.season = season
        
    def __str__(self) -> str:
        return (
            f"SeasonInfo(season_id={self.season_id}, "
            f"final_score={self.final_score}, "
            f"points_available={self.points_available}, "
            f"points_against={self.points_against}, "
            f"season={self.season})"
        )
