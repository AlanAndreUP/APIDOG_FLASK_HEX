from abc import ABC, abstractmethod
from typing import List, Optional

from src.domain.entities.breed import Breed
from src.domain.entities.fact import Fact
from src.domain.entities.group import Group
from src.domain.entities.pagination import PaginationParams, SearchParams, PaginatedResponse


class DogRepository(ABC):
    @abstractmethod
    def get_breeds(self, pagination: PaginationParams, search: Optional[SearchParams] = None) -> PaginatedResponse[Breed]:
        """Get all dog breeds with pagination and search"""
        pass

    @abstractmethod
    def get_breed_by_id(self, breed_id: str) -> Optional[Breed]:
        """Get a specific breed by its ID"""
        pass

    @abstractmethod
    def get_facts(self) -> List[Fact]:
        """Get interesting facts about dogs"""
        pass

    @abstractmethod
    def get_groups(self, pagination: PaginationParams, search: Optional[SearchParams] = None) -> PaginatedResponse[Group]:
        """Get all breed groups with pagination and search"""
        pass

    @abstractmethod
    def get_group_by_id(self, group_id: str) -> Optional[Group]:
        """Get a specific group by its ID"""
        pass

    @abstractmethod
    def get_group_details(self, group_id: str) -> Optional[Group]:
        """Get complete details of a group"""
        pass

    @abstractmethod
    def get_breed_in_group(self, group_id: str, breed_id: str) -> Optional[Breed]:
        """Get a specific breed within a group"""
        pass 