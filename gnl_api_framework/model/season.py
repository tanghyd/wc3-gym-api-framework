from typing import Any
from gnl_api_framework.model.map import Map
class Season:
    def __init__(self, data: dict[str, Any]) -> None:
        self.id = data.get('id')
        self.name = data.get('name')
        self.number_weeks = data.get('number_weeks')
        self.series_per_week = data.get('series_per_week')
        self.pick_ban = data.get('pick_ban')
        maps = data.get('maps')
        if maps:
            maps = [Map(map) for map in maps]
        self.maps = maps

    def to_dict(self) -> dict[str, Any]:
        return {
            'name': self.name,
            'number_weeks': self.number_weeks,
            'pick_ban': self.pick_ban,
            'series_per_week': self.series_per_week
        }
    
    def __str__(self) -> str:
        maps_str = None
        if self.maps:
            maps_str = ", ".join(
                f"{map}" for map in self.maps
            )
        return (
            f"Season(id={self.id}, "
            f"name={self.name}, "
            f"number_weeks={self.number_weeks}, "
            f"series_per_week={self.series_per_week}, "
            f"pick_ban={self.pick_ban}, " 
            f"maps={maps_str})"
        )
