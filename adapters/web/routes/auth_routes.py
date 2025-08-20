from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr
from adapters.db.sqlite_user_repository import SQLiteUserRepository
from core.use_cases.authenticate_user import authenticate_user, AuthenticationError

router = APIRouter(prefix="/auth", tags=["auth"])


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


@router.post("/login")
def login(body: LoginRequest):
    repo = SQLiteUserRepository()
    try:
        token = authenticate_user(repo, body.email, body.password)
    except AuthenticationError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )
    return {"status": "ok", "data": {"token": token}}
