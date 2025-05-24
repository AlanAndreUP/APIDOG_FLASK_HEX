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
        Obtiene todos los elementos con paginación y búsqueda
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
        Realiza una búsqueda con paginación
        """
        pass

    @abstractmethod
    async def get_by_id(self, id: str) -> Optional[T]:
        """
        Obtiene un elemento por su ID
        """
        pass

    @abstractmethod
    async def create(self, data: dict) -> T:
        """
        Crea un nuevo elemento
        """
        pass

    @abstractmethod
    async def update(self, id: str, data: dict) -> Optional[T]:
        """
        Actualiza un elemento existente
        """
        pass

    @abstractmethod
    async def delete(self, id: str) -> bool:
        """
        Elimina un elemento
        """
        pass 