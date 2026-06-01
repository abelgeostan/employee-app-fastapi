


from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from auth import service
from auth.schemas import LoginRequest, TokenResponse
from sqlalchemy.ext.asyncio import AsyncSession

from database.connection import get_db


router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login", response_model=TokenResponse)
async def login(form:OAuth2PasswordRequestForm=Depends(), db: AsyncSession = Depends(get_db)):
    # token=await service.login(db, body.email, body.password)
    # refresh_token=await service.create_refresh_token(db, body.email)
    # return TokenResponse(access_token=token, refresh_token=refresh_token)
    token=await service.login(db,form.username,form.password)
    # refresh_token=await service.create_refresh_token(db, form.username)
    return TokenResponse(access_token=token, refresh_token=token)
"""fix this issue, id attrib not found error on create refresh token"""



