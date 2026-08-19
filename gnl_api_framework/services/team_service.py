import logging
from gnl_api_framework.services.base_service import BaseGNLBackendService
from gnl_api_framework.model.team import Team

logger = logging.getLogger(__name__)

class TeamService(BaseGNLBackendService):
    
    def get_team(self, team_id: int):
        logger.debug(f"Fetching team with ID: {team_id}")
        result = self.get(f"teams/{team_id}")
        logger.debug(f"Received response: {result}")
        return Team(result)
    
    def update_team(self, team_id, team: Team):
        if not team or not team_id:
            logger.error(f"Team or team ID not defined: {team}")
            raise Exception(f"Team or team id not defined: {team}")
        logger.debug(f"Updating team with ID: {team_id}, data: {team.to_dict()}")
        result = self.put(f"teams/{team_id}", team.to_dict())
        logger.debug(f"Received response: {result}")
        return Team(result)
    
    def create_team(self, team: Team):
        if not team:
            logger.error(f"Team not defined: {team}")
            raise Exception(f"Team not defined: {team}")
        logger.debug(f"Creating new team with data: {team.to_dict()}")
        result = self.post("teams", team.to_dict())
        logger.debug(f"Received response: {result}")
        return Team(result)
    
    def delete_team(self, team_id):
        if not team_id:
            logger.error(f"Team ID not defined: {team_id}")
            raise Exception(f"Team id not defined: {team_id}")
        logger.debug(f"Deleting team with ID: {team_id}")
        self.delete(f"teams/{team_id}")
        logger.debug(f"Team with ID {team_id} deleted successfully")
        return True
    
    def search_team(self, search_string, limit: int = None, offset: int = None):
        if not search_string:
            logger.error(f"Search String not defined: {search_string}")
            raise Exception(f"Search String not defined: {search_string}")
        logger.debug(f"Searching teams with query: {search_string}")
        teams = self.search("teams/search", search_string, limit=limit, offset=offset)
        logger.debug(f"Received response: {teams}")
        l = [Team(team) for team in teams]
        return l

    def get_all_teams(self, limit: int = None, offset: int = None):
        logger.debug("Fetching all teams")
        teams = self.get("teams", limit=limit, offset=offset)
        logger.debug(f"Received response: {teams}")
        l = [Team(team) for team in teams]
        return l
    
    def get_teams_for_season(self, season_id: int):
        logger.debug(f"Fetching teams for season ID: {season_id}")
        teams = self.get(f"teams/season/{season_id}")
        logger.debug(f"Received response: {teams}")
        l = [Team(team) for team in teams]
        return l
    
    def get_team_for_season(self, season_id: int, team_id: int):
        logger.debug(f"Fetching team with ID: {team_id} for season ID: {season_id}")
        result = self.get(f"teams/{team_id}/seasons/{season_id}")
        logger.debug(f"Received response: {result}")
        return Team(result)

    def add_player(self, team_id, season_id, player_ids: list):
        if not team_id:
            logger.error(f"Team ID not defined: {team_id}")
            raise Exception(f"Team id not defined: {team_id}")
        if not season_id:
            logger.error(f"Season ID not defined: {season_id}")
            raise Exception(f"Season id not defined: {season_id}")
        if not player_ids:
            logger.error(f"No player IDs defined: {player_ids}")
            raise Exception(f"No player ids defined: {player_ids}")
        logger.debug(f"Adding players {player_ids} to team with ID: {team_id}")
        result = self.post(f"teams/addPlayers/{team_id}/seasons/{season_id}", {"player_ids":player_ids})
        logger.debug(f"Received response: {result}")
        return Team(result)
    
    def remove_player(self, team_id, season_id, player_ids: list):
        if not team_id:
            logger.error(f"Team ID not defined: {team_id}")
            raise Exception(f"Team id not defined: {team_id}")
        if not season_id:
            logger.error(f"Season ID not defined: {season_id}")
            raise Exception(f"Season id not defined: {season_id}")
        if not player_ids:
            logger.error(f"No player IDs defined: {player_ids}")
            raise Exception(f"No player ids defined: {player_ids}")
        logger.debug(f"Removing players {player_ids} from team with ID: {team_id}")
        result = self.post(f"teams/removePlayers/{team_id}/seasons/{season_id}", {"player_ids":player_ids})
        logger.debug(f"Received response: {result}")
        return Team(result)
