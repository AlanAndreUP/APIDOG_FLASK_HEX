from flask import Flask
from src.infrastructure.api.controllers.dog_controller import DogController
from src.domain.entities.pagination import PaginationParams, SearchParams
from src.shared.decorators import format_response
from typing import Dict, Any, Tuple, Optional

def _get_pagination_params(args: Dict[str, Any]) -> Tuple[int, int]:
    """
    Gets and validates pagination parameters safely.
    Returns a tuple with (page, per_page)
    """
    try:
        page = int(args.get('page', 1))
        page_size = int(args.get('per_page', 5))
        
        if page < 1:
            page = 1
        if page_size < 1:
            page_size = 5
        if page_size > 100:
            page_size = 100
            
        return page, page_size
    except (ValueError, TypeError):
        return 1, 10

def _get_search_params(args: Dict[str, Any]) -> Optional[SearchParams]:
    """
    Gets and validates search parameters safely.
    Returns None if there is no search or the parameter is empty.
    """
    search = args.get('search', '').strip()
    return SearchParams(query=search) if search else None

def register_routes(app: Flask, controller: DogController) -> None:
    
    @app.route('/breeds', methods=['GET'])
    @format_response
    def get_breeds(page: int = 1, per_page: int = 5, search: str = ''):
        """Get all dog breeds with pagination and search"""
        page, page_size = _get_pagination_params({'page': page, 'per_page': per_page})
        search_params = _get_search_params({'search': search})
        pagination = PaginationParams(page=page, page_size=page_size)
        response, status_code = controller.get_breeds(pagination, search_params)
        return response, status_code

    @app.route('/breeds/<breed_id>', methods=['GET'])
    @format_response
    def get_breed(breed_id: str):
        """Get a specific breed by ID"""
        response, status_code = controller.get_breed(breed_id)
        return response, status_code

    @app.route('/facts', methods=['GET'])
    @format_response
    def get_facts():
        """Get dog facts"""
        response, status_code = controller.get_facts()
        return response, status_code

    @app.route('/groups', methods=['GET'])
    @format_response
    def get_groups(page: int = 1, per_page: int = 5, search: str = ''):
        """Get all groups with pagination and search"""
        page, page_size = _get_pagination_params({'page': page, 'per_page': per_page})
        search_params = _get_search_params({'search': search})
        pagination = PaginationParams(page=page, page_size=page_size)
        response, status_code = controller.get_groups(pagination, search_params)
        return response, status_code

    @app.route('/groups/<group_id>', methods=['GET'])
    @format_response
    def get_group(group_id: str):
        """Get a specific group by ID"""
        response, status_code = controller.get_group(group_id)
        return response, status_code

    @app.route('/group-details/<group_id>', methods=['GET'])
    @format_response
    def get_group_details(group_id: str):
        """Get group relationships"""
        response, status_code = controller.get_group_details(group_id)
        return response, status_code

    @app.route('/group-details/<group_id>/breed/<breed_id>', methods=['GET'])
    @format_response
    def get_breed_in_group(group_id: str, breed_id: str):
        """Get a breed within a group"""
        response, status_code = controller.get_breed_in_group(group_id, breed_id)
        return response, status_code 