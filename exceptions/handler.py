



import logging


from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from exceptions import AppException, BadRequestException, ConflictException, ForbiddenException, NotFoundException, UnauthorizedException


logger=logging.getLogger(__name__)

_STATUS_MAP: dict[type[AppException], int]={
        NotFoundException: status.HTTP_404_NOT_FOUND,
        ConflictException: status.HTTP_409_CONFLICT,
        BadRequestException: status.HTTP_400_BAD_REQUEST,
        UnauthorizedException: status.HTTP_401_UNAUTHORIZED,        
}

def register_exception_handlers(app:FastAPI)->None:
    """Attach all application exception handlers to app"""

    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc:AppException)->JSONResponse:
        code=_STATUS_MAP.get(type(exc),status.HTTP_500_INTERNAL_SERVER_ERROR)
        return JSONResponse(status_code=code, content={"detail": exc.detail})
    
    @app.exception_handler(NotFoundException)
    async def not_found_exception_handler(request: Request,exc: NotFoundException):
        return JSONResponse(
                status_code=404,
                content={"detail": str(exc)}
        )
    
    @app.exception_handler(ForbiddenException)
    async def forbidden_exception_handler(request: Request,exc: NotFoundException):
        return JSONResponse(
                status_code=403,
                content={"detail": str(exc)}
        )
