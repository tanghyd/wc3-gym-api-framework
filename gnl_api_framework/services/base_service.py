from abc import ABC, abstractmethod
import logging
import requests
import jwt
from datetime import datetime, timezone

logger = logging.getLogger(__name__)

class BaseGNLBackendService(ABC):
    class HTTPMethods: 
        GET = "GET"
        POST = "POST"
        PUT = "PUT"
        DELETE = "DELETE"
        PATCH = "PATCH"
        HEAD = "HEAD"
        OPTIONS = "OPTIONS"

    def __init__(self, url, admin_token):
        self.admin_token = admin_token
        self.url = url
        self.token = None
        self.refresh_token = None
        logger.debug("Bakend URL: " + self.url)


    def send_request(self, method, url, data=None, headers=None, params=None):
        try:
            # Send the request
            logger.debug(f"Send Reqest with Method:{method}, URL: {url}, data:{data}, headers:{headers}, params:{params}")
            response = requests.request(method, url, json=data, headers=headers, params=params)

            # Check the status code
            if response.status_code in [200, 201]:
                logger.debug(f"Request successful: {response.status_code}")
                try:
                    return response.json()  # Parse JSON response
                except ValueError:
                    raise Exception(response.text)  # Return plain text if not JSON
            if response.status_code == 204:
                logger.debug(f"Request successful: {response.status_code}")
                return response.text
            else:
                # Log or raise an error for non-200 status codes
                raise Exception(f"Request failed with status code {response.status_code}: {response.text}")

        except requests.exceptions.RequestException as e:
            # Handle network-related errors
            raise Exception(f"An exception occurred: {str(e)}")


    def login(self):
        if not self.refresh_token:
            response = self.send_request(method=self.HTTPMethods.POST, url=self.buildURL("/login"), data={'token':self.admin_token})
            if response and response.get('access_token'):
                self.token = response.get('access_token')
                self.refresh_token = response.get('refresh_token')
            else:
                raise Exception(f"Login not successful, token could not be retreived: {response}")                
        else:
            response = self.send_request(method=self.HTTPMethods.POST, url=self.buildURL("/refresh"), headers={'Authorization':f"Bearer {self.refresh_token}"})
            if response and response.get('access_token'):
                self.token = response.get('access_token')
            else:
                raise Exception(f"Login not successful, token could not be retreived: {response}")

    def buildURL(self, endpoint: str):
        if endpoint.startswith('/'):
            endpoint = endpoint[1:]
        return f"{self.url}/{endpoint}"

    def get(self, endpoint, params=None, limit: int = None, offset: int = None):
        params = self.add_paging_params(params, limit, offset)
        return self.send_request(method=self.HTTPMethods.GET, url=self.buildURL(endpoint), params=params)

    def search(self, endpoint: str, search_str: str = None, limit: int = None, offset: int = None):
        params = {'query': search_str} if search_str else {}
        params = self.add_paging_params(params, limit, offset)
        return self.send_request(method=self.HTTPMethods.POST, url=self.buildURL(endpoint), params=params)

    @staticmethod
    def add_paging_params(params: dict, limit: int = None, offset: int = None):
        params = dict(params) if params else {}
        if limit is not None:
            params['limit'] = limit
        if offset is not None:
            params['offset'] = offset
        return params or None


    def post(self, endpoint, data: dict):
        if self.is_token_expired():
            self.login()
        if data:
            return self.send_request(method=self.HTTPMethods.POST, url=self.buildURL(endpoint), headers={'Authorization':f"Bearer {self.token}"}, data=data)
        else:
            return self.send_request(method=self.HTTPMethods.POST, url=self.buildURL(endpoint), headers={'Authorization':f"Bearer {self.token}"})

    def delete(self, endpoint):
        if self.is_token_expired():
            self.login()
        return self.send_request(method=self.HTTPMethods.DELETE, url=self.buildURL(endpoint), headers={'Authorization':f"Bearer {self.token}"})

    def put(self, endpoint, data: dict):
        if self.is_token_expired():
            self.login()
        return self.send_request(method=self.HTTPMethods.PUT, url=self.buildURL(endpoint), headers={'Authorization':f"Bearer {self.token}"}, data=data)

    def is_token_expired(self):
        try:
            if not self.token:
                return True
            # Decode the JWT without verifying the signature
            decoded = jwt.decode(self.token, options={"verify_signature": False})
            
            # Get the current time in UTC
            current_time = datetime.now(timezone.utc).timestamp()
            
            # Check the `exp` claim
            if "exp" in decoded:
                if current_time > decoded["exp"]:
                    return True  # Token has expired
                else:
                    return False  # Token is still valid
            else:
                print("Token does not contain an expiration ('exp') claim.")
                return True  # Treat as expired if no `exp` is present
        except jwt.DecodeError:
            print("Invalid token format.")
            return True  # Treat as expired for safety