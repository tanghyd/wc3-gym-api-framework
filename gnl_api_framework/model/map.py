from typing import Any


class Map:
    def __init__(self, data: dict[str, Any]) -> None:
        self.id = data.get('id')
        self.name = data.get('name')
        self.shortname = data.get('shortname')
        self.image = data.get('image')

    def to_dict(self) -> dict[str, Any]:
        return {
            'id': self.id,
            'name': self.name,
            'shortname': self.shortname,
            'image': self.image
        }
    
    def __str__(self) -> str:
        return (
            f"Map(id={self.id}, "
            f"name={self.name}, "
            f"shortname={self.shortname}, "
            f"image={self.image})"
        )
