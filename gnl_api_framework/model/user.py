from typing import Any


class User:
    def __init__(self, data: dict[str, Any]) -> None:
        self.id = data.get('id')
        self.name = data.get('name')
        self.battleTag = data.get('battleTag')
        self.discordTag = data.get('discordTag')
        self.race = data.get('race')
        self.mmr = data.get('mmr')
        self.country = data.get('country')
        self.fantasy_tier = data.get('fantasy_tier')

    def to_dict(self) -> dict[str, Any]:
        return {
            'name': self.name,
            'battleTag': self.battleTag,
            'discordTag': self.discordTag,
            'race': self.race,
            'mmr': self.mmr,
            'country': self.country,
            'fantasy_tier': self.fantasy_tier
        }

    def __str__(self) -> str:
        return (
            f"User(id={self.id}, name={self.name}, "
            f"battleTag={self.battleTag}, discordTag={self.discordTag}, "
            f"race={self.race}, mmr={self.mmr}, country={self.country})"
            f"fantasy_tier={self.fantasy_tier})"
        )
