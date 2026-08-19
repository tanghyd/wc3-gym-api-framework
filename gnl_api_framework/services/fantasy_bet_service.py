import logging
from gnl_api_framework.services.base_service import BaseGNLBackendService
from gnl_api_framework.model.fantasy_bet import FantasyBet

logger = logging.getLogger(__name__)

class FantasyBetService(BaseGNLBackendService):
    
    def get_fantasy_bet(self, bet_id: int):
        logger.debug(f"Fetching fantasy bet with ID: {bet_id}")
        result = self.get(f"fantasy/bets/{bet_id}")
        logger.debug(f"Received response: {result}")
        return FantasyBet(result)
    
    def update_bet(self, bet_id, fbet: FantasyBet):
        if not fbet or not bet_id:
            logger.error(f"Fantasy Bet or bet ID not defined: {fbet}")
            raise Exception(f"Fantasy Bet or bet id not defined: {fbet}")
        logger.debug(f"Updating bet with ID: {bet_id}, data: {fbet.to_dict()}")
        result = self.put(f"fantasy/bets/{bet_id}", fbet.to_dict())
        logger.debug(f"Received response: {result}")
        return FantasyBet(result)
    
    def create_bet(self, fbet: FantasyBet):
        if not fbet:
            logger.error(f"Fantasy Bet not defined: {fbet}")
            raise Exception(f"Fantasy Bet not defined: {fbet}")
        logger.debug(f"Creating new bet with data: {fbet.to_dict()}")
        result = self.post("fantasy/bets", fbet.to_dict())
        logger.debug(f"Received response: {result}")
        return FantasyBet(result)
    
    def delete_bet(self, bet_id):
        if not bet_id:
            logger.error(f"Fantasy Bet ID not defined: {bet_id}")
            raise Exception(f"Fantasy Bet id not defined: {bet_id}")
        logger.debug(f"Deleting fantasy bet with ID: {bet_id}")
        self.delete(f"fantasy/bets/{bet_id}")
        logger.debug(f"Fantasy bet with ID {bet_id} deleted successfully")
        return True
    
    def search_bet(self, search_string, limit: int = None, offset: int = None):
        if not search_string:
            logger.error(f"Search String not defined: {search_string}")
            raise Exception(f"Search String not defined: {search_string}")
        logger.debug(f"Searching bets with query: {search_string}")
        bets = self.search("fantasy/bets/search", search_string, limit=limit, offset=offset)
        logger.debug(f"Received response: {bets}")
        l = [FantasyBet(bet) for bet in bets]
        return l

    def get_all_bets(self, limit: int = None, offset: int = None):
        logger.debug("Fetching all fantasy bets")
        bets = self.get("fantasy/bets", limit=limit, offset=offset)
        logger.debug(f"Received response: {bets}")
        l = [FantasyBet(bet) for bet in bets]
        return l