from abc import ABC, abstractmethod
from typing import TypeVar, Generic, List, Optional
from src.domain.entities.pagination import PaginationParams, SearchParams, PaginatedResponse

T = TypeVar('T')

class BaseService(Generic[T], ABC):
    @abstractmethod
    async def get_all(
        self,
        pagination_params: PaginationParams,
        search_params: Optional[SearchParams] = None
    ) -> PaginatedResponse[T]:
        """
        Gets all elements with pagination and search
        """
        pass

    @abstractmethod
    async def search(
        self,
        query: str,
        pagination_params: PaginationParams,
        filters: Optional[dict] = None
    ) -> PaginatedResponse[T]:
        """
        Performs a search with pagination
        """
        pass

    @abstractmethod
    async def get_by_id(self, id: str) -> Optional[T]:
        """
        Gets an element by its ID
        """
        pass

    @abstractmethod
    async def create(self, data: dict) -> T:
        """
        Creates a new element
        """
        pass

    @abstractmethod
    async def update(self, id: str, data: dict) -> Optional[T]:
        """
        Updates an existing element
        """
        pass

    @abstractmethod
    async def delete(self, id: str) -> bool:
        """
        Deletes an element
        """
        pass 