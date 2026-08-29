from typing import Any
from gnl_api_framework.model.user import User
from gnl_api_framework.model.season import Season
from gnl_api_framework.model.series import Series

class FantasyBet:
    def __init__(self, data: dict[str, Any]) -> None:
        self.id = data.get('id')
        self.series_id = data.get('series_id')
        series = data.get('series')
        if series:
            series = Series(series)
        self.series = series
        self.season_id = data.get('season_id')
        season = data.get('season')
        if season:
            season = Season(season)
        self.season = season
        self.user_id = data.get('user_id')
        user = data.get('user')
        if user:
            user = User(user)
        self.user = user
        self.winner_id = data.get('winner_id')
        winner = data.get('winner')
        if winner:
            winner = User(winner)
        self.winner = winner
        self.bet_points = data.get('bet_points')
        self.bet_result = data.get('bet_result')

    def to_dict(self) -> dict[str, Any]:
        return {
            'id': self.id,
            'series_id': self.series_id,
            'season_id': self.season_id,
            'user_id': self.user_id,
            'winner_id': self.winner_id,
            'bet_points': self.bet_points,
            'bet_result': self.bet_result
        }
    
    def __str__(self) -> str:
        return (
            f"FantasyBet(id={self.id}, "
            f"series={str(self.series)}, "
            f"season={str(self.season)}, "
            f"user=[{str(self.user)}], "
            f"winner={self.winner}, "
            f"bet_points={self.bet_result})"
            f"bet_result={self.bet_result}, "
        )
