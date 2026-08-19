import logging
from gnl_api_framework.services.base_service import BaseGNLBackendService
from gnl_api_framework.model.fantasy_team import FantasyTeam

logger = logging.getLogger(__name__)

class FantasyTeamService(BaseGNLBackendService):
    
    def get_fantasy_team(self, team_id: int):
        logger.debug(f"Fetching fantasy team with ID: {team_id}")
        result = self.get(f"fantasy/teams/{team_id}")
        logger.debug(f"Received response: {result}")
        return FantasyTeam(result)
    
    def update_team(self, team_id, fteam: FantasyTeam):
        if not fteam or not team_id:
            logger.error(f"Fantasy Team or team ID not defined: {fteam}")
            raise Exception(f"Fantasy Team or team id not defined: {fteam}")
        logger.debug(f"Updating team with ID: {team_id}, data: {fteam.to_dict()}")
        result = self.put(f"fantasy/teams/{team_id}", fteam.to_dict())
        logger.debug(f"Received response: {result}")
        return FantasyTeam(result)
    
    def create_team(self, fteam: FantasyTeam):
        if not fteam:
            logger.error(f"Fantasy Team not defined: {fteam}")
            raise Exception(f"Fantasy Team not defined: {fteam}")
        logger.debug(f"Creating new team with data: {fteam.to_dict()}")
        result = self.post("fantasy/teams", fteam.to_dict())
        logger.debug(f"Received response: {result}")
        return FantasyTeam(result)
    
    def delete_team(self, team_id):
        if not team_id:
            logger.error(f"Fantasy Team ID not defined: {team_id}")
            raise Exception(f"Fantasy Team id not defined: {team_id}")
        logger.debug(f"Deleting fantasy team with ID: {team_id}")
        self.delete(f"fantasy/teams/{team_id}")
        logger.debug(f"Fantasy Team with ID {team_id} deleted successfully")
        return True
    
    def search_team(self, search_string, limit: int = None, offset: int = None):
        if not search_string:
            logger.error(f"Search String not defined: {search_string}")
            raise Exception(f"Search String not defined: {search_string}")
        logger.debug(f"Searching teams with query: {search_string}")
        teams = self.search("fantasy/teams/search", search_string, limit=limit, offset=offset)
        logger.debug(f"Received response: {teams}")
        l = [FantasyTeam(team) for team in teams]
        return l

    def get_all_teams(self, limit: int = None, offset: int = None):
        logger.debug("Fetching all fantasy teams")
        teams = self.get("fantasy/teams", limit=limit, offset=offset)
        logger.debug(f"Received response: {teams}")
        l = [FantasyTeam(team) for team in teams]
        return l

    def add_players(self, team_id, player_ids: list):
        if not team_id:
            logger.error(f"Fantady Team ID not defined: {team_id}")
            raise Exception(f"Fantady Team id not defined: {team_id}")
        if not player_ids:
            logger.error(f"No player IDs defined: {player_ids}")
            raise Exception(f"No player ids defined: {player_ids}")
        logger.debug(f"Adding players {player_ids} to fantasy team with ID: {team_id}")
        result = self.post(f"fantasy/teams/addPlayers/{team_id}", {"player_ids":player_ids})
        logger.debug(f"Received response: {result}")
        return FantasyTeam(result)
    
    def remove_players(self, team_id, player_ids: list):
        if not team_id:
            logger.error(f"Fantasy Team ID not defined: {team_id}")
            raise Exception(f"Fantasy Team id not defined: {team_id}")
        if not player_ids:
            logger.error(f"No player IDs defined: {player_ids}")
            raise Exception(f"No player ids defined: {player_ids}")
        logger.debug(f"Removing players {player_ids} from team with ID: {team_id}")
        result = self.post(f"fantasy/teams/removePlayers/{team_id}", {"player_ids":player_ids})
        logger.debug(f"Received response: {result}")
        return FantasyTeam(result)
