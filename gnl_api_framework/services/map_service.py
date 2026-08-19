import logging
from gnl_api_framework.services.base_service import BaseGNLBackendService
from gnl_api_framework.model.map import Map

logger = logging.getLogger(__name__)

class MapService(BaseGNLBackendService):
    def search_maps(self, search_string, limit: int = None, offset: int = None):
        if not search_string:
            logger.error(f"Search String not defined: {search_string}")
            raise Exception(f"Search String not defined: {search_string}")
        logger.debug(f"Searching maps with query: {search_string}")
        maps = self.search("maps/search", search_string, limit=limit, offset=offset)
        logger.debug(f"Received response: {maps}")
        l = [Map(map) for map in maps]
        return l

    def get_map(self, map_id: int):
        logger.debug(f"Fetching map with ID: {map_id}")
        result = self.get(f"maps/{map_id}")
        logger.debug(f"Received response: {result}")
        return Map(result)

    def update_map(self, map_id, map: Map):
        if not map or not map_id:
            logger.error(f"Map or map ID not defined: {map}")
            raise Exception(f"Map or map id not defined: {map}")
        logger.debug(f"Updating map with ID: {map_id}, data: {map.to_dict()}")
        result = self.put(f"maps/{map_id}", map.to_dict())
        logger.debug(f"Received response: {result}")
        return Map(result)

    def create_map(self, map: Map):
        if not map:
            logger.error(f"Map not defined: {map}")
            raise Exception(f"Map not defined: {map}")
        logger.debug(f"Creating new map with data: {map.to_dict()}")
        result = self.post("maps", map.to_dict())
        logger.debug(f"Received response: {result}")
        return Map(result)

    def delete_map(self, map_id):
        if not map_id:
            logger.error(f"Map ID not defined: {map_id}")
            raise Exception(f"Map id not defined: {map_id}")
        logger.debug(f"Deleting map with ID: {map_id}")
        self.delete(f"maps/{map_id}")
        logger.debug(f"Map with ID {map_id} deleted successfully")
        return True

    def get_all_maps(self, limit: int = None, offset: int = None):
        logger.debug("Fetching all maps")
        maps = self.get("maps", limit=limit, offset=offset)
        logger.debug(f"Received response: {maps}")
        l = [Map(map) for map in maps]
        return l
