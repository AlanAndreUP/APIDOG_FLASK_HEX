from typing import List, Optional

from src.application.ports.output.dog_repository import DogRepository
from src.domain.entities.breed import Breed
from src.domain.entities.fact import Fact
from src.domain.entities.group import Group
from src.domain.entities.pagination import PaginationParams, SearchParams, PaginatedResponse


class DogService:
    def __init__(self, dog_repository: DogRepository):
        self._dog_repository = dog_repository

    def get_all_breeds(self, pagination: PaginationParams, search: Optional[SearchParams] = None) -> PaginatedResponse[Breed]:
        """Use case: Get all dog breeds with pagination and search"""
        return self._dog_repository.get_breeds(pagination, search)

    def get_breed_by_id(self, breed_id: str) -> Optional[Breed]:
        """Use case: Get a specific breed"""
        return self._dog_repository.get_breed_by_id(breed_id)

    def get_all_facts(self) -> List[Fact]:
        """Use case: Get all dog facts"""
        return self._dog_repository.get_facts()

    def get_all_groups(self, pagination: PaginationParams, search: Optional[SearchParams] = None) -> PaginatedResponse[Group]:
        """Use case: Get all groups with pagination and search"""
        return self._dog_repository.get_groups(pagination, search)

    def get_group_by_id(self, group_id: str) -> Optional[Group]:
        """Use case: Get a specific group"""
        return self._dog_repository.get_group_by_id(group_id)

    def get_group_details(self, group_id: str) -> Optional[Group]:
        """Use case: Get group details"""
        return self._dog_repository.get_group_details(group_id)

    def get_breed_in_group(self, group_id: str, breed_id: str) -> Optional[Breed]:
        """Use case: Get a breed within a group"""
        return self._dog_repository.get_breed_in_group(group_id, breed_id) 