from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
import json
from app.core.config import settings

class ResponseWrapperMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
        except Exception as e:
            # This should rarely be hit now due to global handlers, 
            # but serves as a final safety net.
            return JSONResponse(
                status_code=500,
                content={
                    "success": False,
                    "message": "Something went wrong",
                    "error": {
                        "code": "SERVER_ERROR",
                        "details": str(e)
                    }
                }
            )
        
        # Paths that are NEVER wrapped (docs, openapi, etc.)
        exclude_paths = ["/api/openapi.json", "/docs", "/redoc"]
        if request.url.path in exclude_paths or not request.url.path.startswith("/api"):
            return response

        # Read the body carefully
        response_body = b""
        async for chunk in response.body_iterator:
            response_body += chunk

        try:
            data = json.loads(response_body)
            
            headers = dict(response.headers)
            if "content-length" in headers:
                del headers["content-length"]

            # If already FULLY wrapped with success key, just return as is
            if isinstance(data, dict) and "success" in data:
                return JSONResponse(content=data, status_code=response.status_code, headers=headers)
            
            # Success logic
            is_success = response.status_code < 400
            
            if is_success:
                # Standardize success response
                wrapped_data = {
                    "success": True,
                    "message": "Action completed successfully",
                    "data": data
                }
                # Use 201 for POST success if not already set otherwise
                status_code = response.status_code
                if request.method == "POST" and status_code == 200:
                    status_code = 201
                    
                return JSONResponse(content=wrapped_data, status_code=status_code, headers=headers)
            else:
                # If it's an error but NOT wrapped (e.g. from FastAPI defaults)
                return JSONResponse(
                    status_code=response.status_code,
                    content={
                        "success": False,
                        "message": data["detail"] if isinstance(data, dict) and "detail" in data else "An error occurred",
                        "data": None
                    },
                    headers=headers
                )
        except Exception:
            # Fallback for non-JSON or raw responses
            try:
                content = response_body.decode('utf-8')
            except:
                content = str(response_body)
                
            headers = dict(response.headers)
            if "content-length" in headers:
                del headers["content-length"]

            return JSONResponse(
                content={
                    "success": response.status_code < 400,
                    "message": "Action completed" if response.status_code < 400 else "An error occurred",
                    "data": content if response.status_code < 400 else None,
                    "error": {
                        "code": "RAW_RESPONSE",
                        "details": content
                    } if response.status_code >= 400 else None
                },
                status_code=response.status_code,
                headers=headers
            )

        
