from typing import Any, Dict, Optional
from dataclasses import dataclass
from http import HTTPStatus

@dataclass
class ApiResponse:
    """Class to handle standardized API responses."""
    
    @staticmethod
    def success(
        data: Any = None,
        message: str = "Success",
        status_code: int = HTTPStatus.OK
    ) -> Dict[str, Any]:
        """
        Generates a standardized success response.
        
        Args:
            data: Data to return in the response
            message: Descriptive message of the result
            status_code: HTTP status code (default: 200)
            
        Returns:
            Dict with standardized response structure
        """
        return {
            "status": "success",
            "message": message,
            "data": data
        }, status_code

    @staticmethod
    def error(
        message: str,
        status_code: int = HTTPStatus.BAD_REQUEST,
        errors: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Generates a standardized error response.
        
        Args:
            message: Descriptive error message
            status_code: HTTP status code (default: 400)
            errors: Additional error details (optional)
            
        Returns:
            Dict with standardized error response structure
        """
        response = {
            "status": "error",
            "message": message
        }
        
        if errors:
            response["errors"] = errors
            
        return response, status_code

    @staticmethod
    def created(
        data: Any = None,
        message: str = "Resource created successfully"
    ) -> Dict[str, Any]:
        """Response for successful creation (201)"""
        return ApiResponse.success(data, message, HTTPStatus.CREATED)

    @staticmethod
    def no_content(
        message: str = "No content available"
    ) -> Dict[str, Any]:
        """Response for no content (204)"""
        return ApiResponse.success(None, message, HTTPStatus.NO_CONTENT)

    @staticmethod
    def not_found(
        message: str = "Resource not found"
    ) -> Dict[str, Any]:
        """Response for resource not found (404)"""
        return ApiResponse.error(message, HTTPStatus.NOT_FOUND)

    @staticmethod
    def unauthorized(
        message: str = "Unauthorized access"
    ) -> Dict[str, Any]:
        """Response for unauthorized access (401)"""
        return ApiResponse.error(message, HTTPStatus.UNAUTHORIZED)

    @staticmethod
    def forbidden(
        message: str = "Forbidden access"
    ) -> Dict[str, Any]:
        """Response for forbidden access (403)"""
        return ApiResponse.error(message, HTTPStatus.FORBIDDEN)

    @staticmethod
    def bad_request(
        message: str = "Bad request",
        errors: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Response for bad request (400)"""
        return ApiResponse.error(message, HTTPStatus.BAD_REQUEST, errors)

    @staticmethod
    def validation_error(
        errors: Dict[str, Any],
        message: str = "Validation error"
    ) -> Dict[str, Any]:
        """Response for validation errors (422)"""
        return ApiResponse.error(message, HTTPStatus.UNPROCESSABLE_ENTITY, errors) 