from fastapi import APIRouter, Depends
from adapters.web.schemas.user_schema import (
    UserCreateRequest,
    UserResponse,
)
from core.use_cases.create_user import create_user
from core.use_cases.list_one_user import get_user
from adapters.db.sqlite_user_repository import SQLiteUserRepository
from adapters.web.middlewares.auth import validate_session
from fastapi import HTTPException, status

router = APIRouter(prefix="/users", tags=["users"])


def get_user_repository():
    return SQLiteUserRepository()


@router.post("/", response_model=UserResponse)
def create_user_route(
    body: UserCreateRequest,
    repo: SQLiteUserRepository = Depends(get_user_repository),
    user: dict = Depends(validate_session)
):
    available_roles = ["admin", "user"]
    if user.get("role") not in available_roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado"
        )
    new_user = create_user(
        repo, body
    )

    return UserResponse(
        id=new_user.id,
        email=new_user.email,
        name=new_user.name,
        role=new_user.role,  # type: ignore
        created_at=new_user.created_at.isoformat(),
        updated_at=new_user.updated_at.isoformat(),
    )


@router.get("/")
def list_users(page: int = 1, size: int = 10):
    return {"message": f"list users page={page} size={size}"}


@router.get("/{user_id}", response_model=UserResponse)
def get_user_route(
    user_id: str,
    repo: SQLiteUserRepository = Depends(get_user_repository),
    user: dict = Depends(validate_session)
):
    available_roles = ["admin", "user"]
    if user.get("role") not in available_roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado"
        )
    return get_user(repo, user_id)


@router.put("/{user_id}")
def update_user(user_id: str):
    return {"message": f"update user {user_id}"}


@router.delete("/{user_id}")
def delete_user(user_id: str):
    return {"message": f"delete user {user_id}"}
