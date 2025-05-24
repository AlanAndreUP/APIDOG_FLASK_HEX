from functools import wraps
from typing import Callable, Any, Dict
from .api_response import ApiResponse

def format_response(f: Callable) -> Callable:
    """
    Decorator that automatically formats API responses
    """
    @wraps(f)
    def decorated_function(*args: Any, **kwargs: Any) -> Dict[str, Any]:
        result = f(*args, **kwargs)
        if isinstance(result, tuple) and len(result) == 2:
            response, status_code = result
            if isinstance(response, dict) and 'status' in response:
                return response, status_code
    
        if isinstance(result, dict) and 'status' in result:
            return result, 200
            
        return ApiResponse.success(data=result)
        
    return decorated_function 
