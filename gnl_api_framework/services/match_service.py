import logging
from gnl_api_framework.services.base_service import BaseGNLBackendService
from gnl_api_framework.model.match import Match

logger = logging.getLogger(__name__)

class MatchService(BaseGNLBackendService):
    
    def get_match(self, match_id: int):
        logger.debug(f"Fetching match with ID: {match_id}")
        result = self.get(f"matches/{match_id}")
        logger.debug(f"Received response: {result}")
        return Match(result)
    
    def update_match(self, match_id, match: Match):
        if not match or not match_id:
            logger.error(f"Match or match ID not defined: {match}")
            raise Exception(f"Match or match id not defined: {match}")
        logger.debug(f"Updating match with ID: {match_id}, data: {match.to_dict()}")
        result = self.put(f"matches/{match_id}", match.to_dict())
        logger.debug(f"Received response: {result}")
        return Match(result)
    
    def create_match(self, match: Match):
        if not match:
            logger.error(f"Match not defined: {match}")
            raise Exception(f"Match not defined: {match}")
        logger.debug(f"Creating new match with data: {match.to_dict()}")
        result = self.post("matches", match.to_dict())
        logger.debug(f"Received response: {result}")
        return Match(result)
    
    def delete_match(self, match_id):
        if not match_id:
            logger.error(f"Match ID not defined: {match_id}")
            raise Exception(f"Match id not defined: {match_id}")
        logger.debug(f"Deleting match with ID: {match_id}")
        self.delete(f"matches/{match_id}")
        logger.debug(f"Match with ID {match_id} deleted successfully")
        return True
    
    def search_matches(self, search_string, limit: int = None, offset: int = None):
        if not search_string:
            logger.error(f"Search String not defined: {search_string}")
            raise Exception(f"Search String not defined: {search_string}")
        logger.debug(f"Searching matches with query: {search_string}")
        matches = self.search("matches/search", search_string, limit=limit, offset=offset)
        logger.debug(f"Received response: {matches}")
        l = [Match(match) for match in matches]
        return l
