from dataclasses import dataclass
from typing import TypeVar, Generic, List, Optional

T = TypeVar('T')

@dataclass
class PaginationParams:
    page: int = 1
    page_size: int = 10
    sort_by: Optional[str] = None
    sort_order: Optional[str] = None  

@dataclass
class SearchParams:
    query: Optional[str] = None
    filters: Optional[dict] = None

@dataclass
class PaginatedResponse(Generic[T]):
    items: List[T]
    total: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_previous: bool

    @classmethod
    def create(cls, items: List[T], total: int, params: PaginationParams) -> 'PaginatedResponse[T]':
        total_pages = (total + params.page_size - 1) // params.page_size
        return cls(
            items=items,
            total=total,
            page=params.page,
            page_size=params.page_size,
            total_pages=total_pages,
            has_next=params.page < total_pages,
            has_previous=params.page > 1
        ) 