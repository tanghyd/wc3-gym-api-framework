from typing import Any
from abc import ABC, abstractmethod
import logging
import requests
import jwt
from datetime import UTC, datetime

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

    def __init__(self, url: str, admin_token: str) -> None:
        self.admin_token = admin_token
        self.url = url
        self.token = None
        self.refresh_token = None
        logger.debug("Bakend URL: " + self.url)


    def send_request(self, method: str, url: str, data: dict[str, Any] | None = None, headers: dict[str, str] | None = None, params: dict[str, Any] | None = None) -> Any:  # noqa: ANN401
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


    def login(self) -> None:
        if not self.refresh_token:
            response = self.send_request(method=self.HTTPMethods.POST, url=self.build_url("/login"), data={'token':self.admin_token})
            if response and response.get('access_token'):
                self.token = response.get('access_token')
                self.refresh_token = response.get('refresh_token')
            else:
                raise Exception(f"Login not successful, token could not be retreived: {response}")                
        else:
            response = self.send_request(method=self.HTTPMethods.POST, url=self.build_url("/refresh"), headers={'Authorization':f"Bearer {self.refresh_token}"})
            if response and response.get('access_token'):
                self.token = response.get('access_token')
            else:
                raise Exception(f"Login not successful, token could not be retreived: {response}")

    def build_url(self, endpoint: str) -> str:
        endpoint = endpoint.removeprefix('/')
        return f"{self.url}/{endpoint}"

    def get(self, endpoint: str, params: dict[str, Any] | None = None, limit: int | None = None, offset: int | None = None) -> Any:  # noqa: ANN401
        params = self.add_paging_params(params, limit, offset)
        return self.send_request(method=self.HTTPMethods.GET, url=self.build_url(endpoint), params=params)

    def search(self, endpoint: str, search_str: str | None = None, limit: int | None = None, offset: int | None = None) -> Any:  # noqa: ANN401
        params = {'query': search_str} if search_str else {}
        params = self.add_paging_params(params, limit, offset)
        return self.send_request(method=self.HTTPMethods.POST, url=self.build_url(endpoint), params=params)

    @staticmethod
    def add_paging_params(params: dict[str, Any] | None, limit: int | None = None, offset: int | None = None) -> dict[str, Any] | None:
        params = dict(params) if params else {}
        if limit is not None:
            params['limit'] = limit
        if offset is not None:
            params['offset'] = offset
        return params or None


    def post(self, endpoint: str, data: dict[str, Any] | None) -> Any:  # noqa: ANN401
        if self.is_token_expired():
            self.login()
        if data:
            return self.send_request(method=self.HTTPMethods.POST, url=self.build_url(endpoint), headers={'Authorization':f"Bearer {self.token}"}, data=data)
        else:
            return self.send_request(method=self.HTTPMethods.POST, url=self.build_url(endpoint), headers={'Authorization':f"Bearer {self.token}"})

    def delete(self, endpoint: str, data: dict[str, Any] | None = None) -> Any:  # noqa: ANN401
        if self.is_token_expired():
            self.login()
        if data:
            return self.send_request(method=self.HTTPMethods.DELETE, url=self.build_url(endpoint), headers={'Authorization':f"Bearer {self.token}"}, data=data)
        return self.send_request(method=self.HTTPMethods.DELETE, url=self.build_url(endpoint), headers={'Authorization':f"Bearer {self.token}"})

    def put(self, endpoint: str, data: dict[str, Any]) -> Any:  # noqa: ANN401
        if self.is_token_expired():
            self.login()
        return self.send_request(method=self.HTTPMethods.PUT, url=self.build_url(endpoint), headers={'Authorization':f"Bearer {self.token}"}, data=data)

    def is_token_expired(self) -> bool:
        try:
            if not self.token:
                return True
            # Decode the JWT without verifying the signature
            decoded = jwt.decode(self.token, options={"verify_signature": False})
            
            # Get the current time in UTC
            current_time = datetime.now(UTC).timestamp()
            
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
