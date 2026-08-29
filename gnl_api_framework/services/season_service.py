import logging
from gnl_api_framework.services.base_service import BaseGNLBackendService
from gnl_api_framework.model.season import Season

logger = logging.getLogger(__name__)

class SeasonService(BaseGNLBackendService):

    def get_season(self, season_id: int) -> Season:
        logger.debug(f"Fetching season with ID: {season_id}")
        result = self.get(f"seasons/{season_id}")
        logger.debug(f"Received response: {result}")
        return Season(result)
    
    def update_season(self, season_id: int, season: Season) -> Season:
        if not season or not season_id:
            logger.error(f"Season or season ID not defined: {season}")
            raise Exception(f"Season or season id not defined: {season}")
        logger.debug(f"Updating season with ID: {season_id}, data: {season.to_dict()}")
        result = self.put(f"seasons/{season_id}", season.to_dict())
        logger.debug(f"Received response: {result}")
        return Season(result)
    
    def create_season(self, season: Season) -> Season:
        if not season:
            logger.error(f"Season not defined: {season}")
            raise Exception(f"Season not defined: {season}")
        logger.debug(f"Creating new season with data: {season.to_dict()}")
        result = self.post("seasons", season.to_dict())
        logger.debug(f"Received response: {result}")
        return Season(result)
    
    def delete_season(self, season_id: int) -> bool:
        if not season_id:
            logger.error(f"Season ID not defined: {season_id}")
            raise Exception(f"Season id not defined: {season_id}")
        logger.debug(f"Deleting season with ID: {season_id}")
        self.delete(f"seasons/{season_id}")
        logger.debug(f"Season with ID {season_id} deleted successfully")
        return True
    
    def get_all_seasons(self, limit: int | None = None, offset: int | None = None) -> list[Season]:
        logger.debug("Fetching all seasons")
        seasons = self.get("seasons", limit=limit, offset=offset)
        logger.debug(f"Received response: {seasons}")
        l = [Season(season) for season in seasons]
        return l

    def search_seasons(self, search_string: str, limit: int | None = None, offset: int | None = None) -> list[Season]:
        if not search_string:
            logger.error(f"Search String not defined: {search_string}")
            raise Exception(f"Search String not defined: {search_string}")
        logger.debug(f"Searching seasons with query: {search_string}")
        seasons = self.search("seasons/search", search_string, limit=limit, offset=offset)
        logger.debug(f"Received response: {seasons}")
        l = [Season(season) for season in seasons]
        return l
    
    def add_teams(self, season_id: int, team_ids: list[int]) -> Season:
        if not season_id:
            logger.error(f"Season ID not defined: {season_id}")
            raise Exception(f"Season id not defined: {season_id}")
        if not team_ids:
            logger.error(f"No team IDs defined: {team_ids}")
            raise Exception(f"No team ids defined: {team_ids}")
        logger.debug(f"Adding teams {team_ids} to season with ID: {season_id}")
        result = self.post(f"seasons/{season_id}/teams", {'team_ids' : team_ids})
        logger.debug(f"Received response: {result}")
        return Season(result)
    
    def remove_teams(self, season_id: int, team_ids: list[int]) -> Season:
        if not season_id:
            logger.error(f"Season ID not defined: {season_id}")
            raise Exception(f"Season id not defined: {season_id}")
        if not team_ids:
            logger.error(f"No team IDs defined: {team_ids}")
            raise Exception(f"No team ids defined: {team_ids}")
        logger.debug(f"Removing teams {team_ids} from season with ID: {season_id}")
        result = self.delete(f"seasons/{season_id}/teams", {'team_ids' : team_ids})
        logger.debug(f"Received response: {result}")
        return Season(result)


    def add_maps(self, season_id: int, map_ids: list[int]) -> Season:
        if not season_id:
            logger.error(f"Season ID not defined: {season_id}")
            raise Exception(f"Season id not defined: {season_id}")
        if not map_ids:
            logger.error(f"No map IDs defined: {map_ids}")
            raise Exception(f"No map ids defined: {map_ids}")
        logger.debug(f"Adding maps {map_ids} to season with ID: {season_id}")
        result = self.post(f"seasons/{season_id}/maps", {'map_ids' : map_ids})
        logger.debug(f"Received response: {result}")
        return Season(result)
    
    def remove_maps(self, season_id: int, map_ids: list[int]) -> Season:
        if not season_id:
            logger.error(f"Season ID not defined: {season_id}")
            raise Exception(f"Season id not defined: {season_id}")
        if not map_ids:
            logger.error(f"No map IDs defined: {map_ids}")
            raise Exception(f"No map ids defined: {map_ids}")
        logger.debug(f"Removing maps {map_ids} from season with ID: {season_id}")
        result = self.delete(f"seasons/{season_id}/maps", {'map_ids' : map_ids})
        logger.debug(f"Received response: {result}")
        return Season(result)
