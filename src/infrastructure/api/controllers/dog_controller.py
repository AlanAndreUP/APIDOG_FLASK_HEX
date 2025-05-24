from typing import Dict, Any, Optional, Tuple

from src.application.services.dog_service import DogService
from src.domain.entities.breed import Breed
from src.domain.entities.fact import Fact
from src.domain.entities.group import Group
from src.domain.entities.pagination import PaginationParams, SearchParams, PaginatedResponse
from src.shared.exceptions.api_exception import APIException
from src.shared.api_response import ApiResponse


class DogController:
    def __init__(self, dog_service: DogService):
        self._dog_service = dog_service

    def _to_dict(self, obj: Any) -> Dict[str, Any]:
        """Converts an entity to a dictionary"""
        if hasattr(obj, '__dict__'):
            return {k: v for k, v in obj.__dict__.items() if v is not None}
        return obj

    def _extract_response_data(self, response: Any) -> Dict[str, Any]:
        """Extracts data from the external API response"""
        if isinstance(response, tuple) and len(response) == 2:
            data, _ = response
            if isinstance(data, dict):
                if data.get('status') == 'error':
                    return ApiResponse.error(data['message'])
                return data.get('data', {})
        return response

    def _handle_paginated_response(self, response: PaginatedResponse, resource_name: str) -> Tuple[Dict[str, Any], int]:
        """Handles paginated response and validates if there is data"""
        if not response.items:
            return ApiResponse.not_found(f"No {resource_name} found"), 404
        

        return {
            "data": [self._to_dict(item) for item in response.items],
            "meta": {
                "total": response.total,
                "page": response.page,
                "page_size": response.page_size,
                "total_pages": response.total_pages,
                "has_next": response.has_next,
                "has_previous": response.has_previous
            },
            "message": f"{resource_name.capitalize()} retrieved successfully",
            "status": "success"
        }, 200

    def get_breeds(self, pagination: PaginationParams, search: Optional[SearchParams] = None) -> Tuple[Dict[str, Any], int]:
        """Gets all dog breeds with pagination and search."""
        try:

            if pagination.page < 1:
                pagination.page = 1
            if pagination.page_size < 1:
                pagination.page_size = 10
            if pagination.page_size > 100:
                pagination.page_size = 100

            breeds = self._dog_service.get_all_breeds(pagination, search)
            return self._handle_paginated_response(breeds, "breeds")
        except APIException as e:
            return ApiResponse.error(str(e)), 400
        except Exception as e:
            return ApiResponse.error("Internal server error"), 500

    def get_breed(self, breed_id: str) -> Tuple[Dict[str, Any], int]:
        """Gets a specific breed."""
        try:
            breed = self._dog_service.get_breed_by_id(breed_id)
            if not breed:
                return ApiResponse.error("Breed not found"), 404
            
            return {
                "data": self._to_dict(breed),
                "message": "Breed retrieved successfully",
                "status": "success"
            }, 200
        except APIException as e:
            return ApiResponse.error(str(e)), 400
        except Exception as e:
            return ApiResponse.error("Internal server error"), 500

    def get_facts(self) -> Tuple[Dict[str, Any], int]:
        """Gets interesting facts about dogs."""
        try:
            facts = self._dog_service.get_all_facts()
            if not facts:
                return ApiResponse.not_found("No facts found"), 404

            return {
                "data": [self._to_dict(item) for item in facts],
                "message": "Facts retrieved successfully",
                "status": "success"
            }, 200
        except APIException as e:
            return ApiResponse.error(str(e)), 400
        except Exception as e:
            return ApiResponse.error("Internal server error"), 500

    def get_groups(self, pagination: PaginationParams, search: Optional[SearchParams] = None) -> Tuple[Dict[str, Any], int]:
        """Gets all groups with pagination and search."""
        try:
            if pagination.page < 1:
                pagination.page = 1
            if pagination.page_size < 1:
                pagination.page_size = 10
            if pagination.page_size > 100:
                pagination.page_size = 100

            groups = self._dog_service.get_all_groups(pagination, search)
            return self._handle_paginated_response(groups, "groups")
        except APIException as e:
            return ApiResponse.error(str(e)), 400
        except Exception as e:
            return ApiResponse.error("Internal server error"), 500

    def get_group(self, group_id: str) -> Tuple[Dict[str, Any], int]:
        """Gets a specific group."""
        try:
            group = self._dog_service.get_group_by_id(group_id)
            if not group:
                return ApiResponse.error("Group not found"), 404
            
            return {
                "data": self._to_dict(group),
                "message": "Group retrieved successfully",
                "status": "success"
            }, 200
        except APIException as e:
            return ApiResponse.error(str(e)), 400
        except Exception as e:
            return ApiResponse.error("Internal server error"), 500

    def get_group_details(self, group_id: str) -> Tuple[Dict[str, Any], int]:
        """Gets group relationships."""
        try:
            group = self._dog_service.get_group_details(group_id)
            if not group:
                return ApiResponse.error("Group not found"), 404
            
            return {
                "data": {
                    "relationships": self._to_dict(group.relationships) if group.relationships else {}
                },
                "message": "Group relationships retrieved successfully",
                "status": "success"
            }, 200
        except APIException as e:
            return ApiResponse.error(str(e)), 400
        except Exception as e:
            return ApiResponse.error("Internal server error"), 500

    def get_breed_in_group(self, group_id: str, breed_id: str) -> Tuple[Dict[str, Any], int]:
        """Gets a breed within a group."""
        try:
            breed = self._dog_service.get_breed_in_group(group_id, breed_id)
            if not breed:
                return ApiResponse.error("Breed not found in the specified group"), 404
            
            return {
                "data": self._to_dict(breed),
                "message": "Breed in group retrieved successfully",
                "status": "success"
            }, 200
        except APIException as e:
            return ApiResponse.error(str(e)), 400
        except Exception as e:
            return ApiResponse.error("Internal server error"), 500 