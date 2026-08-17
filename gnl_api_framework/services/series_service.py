import logging
from gnl_api_framework.services.base_service import BaseGNLBackendService
from gnl_api_framework.model.series import Series

# Configure the logging
logger = logging.getLogger(__name__)

class SeriesService(BaseGNLBackendService):

    def get_series(self, series_id: int):
        logger.debug(f"Fetching series with ID: {series_id}")
        result = self.get(f"series/{series_id}")
        logger.debug(f"Received response: {result}")
        return Series(result)
    
    def update_series(self, series_id, series: Series):
        if not series or not series_id:
            logger.error(f"Series or series ID not defined: {series}")
            raise Exception(f"Series or series id not defined: {series}")
        logger.debug(f"Updating series with ID: {series_id}, data: {series.to_dict()}")
        result = self.put(f"series/{series_id}", series.to_dict())
        logger.debug(f"Received response: {result}")
        return Series(result)
    
    def create_series(self, series: Series):
        if not series:
            logger.error(f"Series not defined: {series}")
            raise Exception(f"Series not defined: {series}")
        logger.debug(f"Creating new series with data: {series.to_dict()}")
        result = self.post("series", series.to_dict())
        logger.debug(f"Received response: {result}")
        return Series(result)
    
    def delete_series(self, series_id):
        if not series_id:
            logger.error(f"Series ID not defined: {series_id}")
            raise Exception(f"Series id not defined: {series_id}")
        logger.debug(f"Deleting series with ID: {series_id}")
        self.delete(f"series/{series_id}")
        logger.debug(f"Series with ID {series_id} deleted successfully")
        return True
    
    def get_all_series(self):
        logger.debug("Fetching all series")
        # No plain list route on the backend, so match every row by id.
        series_l = self.search("series/search", "id > 0")
        logger.debug(f"Received response: {series_l}")
        l = [Series(series) for series in series_l]
        return l

    def search_series(self, search_string):
        if not search_string:
            logger.error(f"Search String not defined: {search_string}")
            raise Exception(f"Search String not defined: {search_string}")
        logger.debug(f"Searching series with query: {search_string}")
        series_l = self.search("series/search", search_string)
        logger.debug(f"Received response: {series_l}")
        l = [Series(series) for series in series_l]
        return l
    
    def search_series_by_season(self, season_id, search_string=None):
        logger.debug(f"Searching series for season[{season_id}] with query: {search_string}")
        series_l = self.search(f"series/season/{season_id}/search", search_string)
        logger.debug(f"Received response: {series_l}")
        l = [Series(series) for series in series_l]
        return l
    
    def search_series_by_season_and_playday(self, season_id, playday, search_string=None):
        logger.debug(f"Searching series for season[{season_id}] with query: {search_string}")
        series_l = self.search(f"series/season/{season_id}/playday/{playday}/search", search_string)
        logger.debug(f"Received response: {series_l}")
        l = [Series(series) for series in series_l]
        return l
