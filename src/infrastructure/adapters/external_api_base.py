from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Optional, Dict, Any
import aiohttp
from src.domain.entities.pagination import PaginationParams, SearchParams, PaginatedResponse

T = TypeVar('T')

class ExternalAPIBase(Generic[T], ABC):
    def __init__(self, base_url: str, api_key: Optional[str] = None):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self._session: Optional[aiohttp.ClientSession] = None

    async def _get_session(self) -> aiohttp.ClientSession:
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession()
        return self._session

    async def close(self):
        if self._session and not self._session.closed:
            await self._session.close()

    def _get_headers(self) -> Dict[str, str]:
        headers = {'Content-Type': 'application/json'}
        if self.api_key:
            headers['Authorization'] = f'Bearer {self.api_key}'
        return headers

    @abstractmethod
    def _parse_response(self, data: Dict[str, Any]) -> T:
        """
        Converts the external API response to type T
        """
        pass

    @abstractmethod
    def _build_pagination_params(self, params: PaginationParams) -> Dict[str, Any]:
        """
        Converts pagination parameters to the format expected by the external API
        """
        pass

    @abstractmethod
    def _build_search_params(self, params: SearchParams) -> Dict[str, Any]:
        """
        Converts search parameters to the format expected by the external API
        """
        pass

    async def get_all(
        self,
        endpoint: str,
        pagination_params: PaginationParams,
        search_params: Optional[SearchParams] = None
    ) -> PaginatedResponse[T]:
        session = await self._get_session()
        params = self._build_pagination_params(pagination_params)
        
        if search_params:
            params.update(self._build_search_params(search_params))

        async with session.get(
            f"{self.base_url}/{endpoint.lstrip('/')}",
            headers=self._get_headers(),
            params=params
        ) as response:
            response.raise_for_status()
            data = await response.json()
            items = [self._parse_response(item) for item in data['items']]
            total = data['total']
            
            return PaginatedResponse.create(items, total, pagination_params)

    async def get_by_id(self, endpoint: str, id: str) -> Optional[T]:
        session = await self._get_session()
        async with session.get(
            f"{self.base_url}/{endpoint.lstrip('/')}/{id}",
            headers=self._get_headers()
        ) as response:
            if response.status == 404:
                return None
            response.raise_for_status()
            data = await response.json()
            return self._parse_response(data) 