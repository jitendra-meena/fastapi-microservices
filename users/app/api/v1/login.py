from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_session
from app.core.security import create_access_token
from app.crud import users as crud_user
from app.schemas.token import Token

router = APIRouter(prefix="/login", tags=["Login"])


@router.post("/", response_model=Token)
async def login(
    data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_session),
):
    user = await crud_user.authenticate(
        session, email=data.username, password=data.password
    )
    if user is None:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return {"access_token": create_access_token(user), "token_type": "bearer"}