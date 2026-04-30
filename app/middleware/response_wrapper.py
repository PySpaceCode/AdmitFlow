from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
import json
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)

class ResponseWrapperMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Always pass through OPTIONS preflight requests untouched
        # so CORSMiddleware can handle them without interference
        if request.method == "OPTIONS":
            return await call_next(request)

        try:
            response = await call_next(request)
        except Exception as e:
            logger.error(f"Error in ResponseWrapperMiddleware: {e}", exc_info=True)
            return JSONResponse(
                status_code=500,
                content={
                    "success": False,
                    "message": "Internal server error during response processing",
                    "data": None
                }
            )
        
        # Paths that are NEVER wrapped (docs, openapi, static files, root)
        exclude_paths = ["/openapi.json", "/docs", "/redoc", "/", "/static"]
        if any(request.url.path.startswith(p) for p in exclude_paths):
            return response

        # Only wrap JSON responses and skip empty/streaming responses
        content_type = response.headers.get("content-type", "")
        if "application/json" not in content_type.lower() or response.status_code == 204:
            return response

        # Read the body
        response_body = b""
        try:
            async for chunk in response.body_iterator:
                response_body += chunk
        except Exception as e:
            logger.error(f"Could not read response body: {e}")
            # If we fail to read the body, we can't wrap it. 
            # But we've already started consuming the iterator, so we can't return the original 'response'.
            # We must return a new error response.
            return JSONResponse(
                status_code=500,
                content={
                    "success": False,
                    "message": "Response body consumption failed",
                    "data": None
                }
            )

        # Prepare headers for the new response
        # We MUST strip Content-Length because JSONResponse will calculate it
        # We also strip other body-related headers
        exclude_headers = {
            "content-length", "content-type", "content-encoding", "transfer-encoding"
        }
        new_headers = {
            k: v for k, v in response.headers.items() 
            if k.lower() not in exclude_headers
        }

        # If body is empty, we still want to return a wrapped success/error
        # but we can't parse it as JSON.
        if not response_body:
            return JSONResponse(
                status_code=response.status_code,
                content={
                    "success": response.status_code < 400,
                    "message": "No content received",
                    "data": None
                },
                headers=new_headers
            )

        try:
            data = json.loads(response_body)
            
            # If already FULLY wrapped with success key, just return as is
            if isinstance(data, dict) and "success" in data:
                return JSONResponse(content=data, status_code=response.status_code, headers=new_headers)
            
            # Success logic
            is_success = response.status_code < 400
            
            if is_success:
                wrapped_data = {
                    "success": True,
                    "message": "Action completed successfully",
                    "data": data
                }
                status_code = response.status_code
                if request.method == "POST" and status_code == 200:
                    status_code = 201
                
                return JSONResponse(content=wrapped_data, status_code=status_code, headers=new_headers)
            else:
                # Standardize error responses from FastAPI (which usually have a 'detail' field)
                error_msg = "An error occurred"
                if isinstance(data, dict):
                    error_msg = data.get("detail", data.get("message", "An error occurred"))
                
                return JSONResponse(
                    status_code=response.status_code,
                    content={
                        "success": False,
                        "message": error_msg,
                        "data": data
                    },
                    headers=new_headers
                )
        except json.JSONDecodeError:
            # Fallback for non-JSON content that was marked as application/json
            content_str = response_body.decode('utf-8', errors='replace')
            return JSONResponse(
                content={
                    "success": response.status_code < 400,
                    "message": "Raw response received",
                    "data": content_str
                },
                status_code=response.status_code,
                headers=new_headers
            )
        except Exception as e:
            logger.error(f"Unexpected error in middleware logic: {e}")
            return JSONResponse(
                status_code=500,
                content={
                    "success": False,
                    "message": "Final middleware safety net",
                    "data": str(e)
                }
            )
        
