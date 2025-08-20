from fastapi import APIRouter, Depends
from adapters.web.schemas.user_schema import (
    UserCreateRequest,
    UserResponse,
)
from core.use_cases.create_user import create_user
from adapters.db.sqlite_user_repository import SQLiteUserRepository

router = APIRouter(prefix="/users", tags=["users"])


def get_user_repository():
    return SQLiteUserRepository()


@router.post("/", response_model=UserResponse)
def create_user_route(
    request: UserCreateRequest,
    repo: SQLiteUserRepository = Depends(get_user_repository),
):
    user = create_user(
        repo, request.email, request.name, request.password, request.role.value
    )

    return UserResponse(
        id=user.id,
        email=user.email,
        name=user.name,
        role=user.role,  # type: ignore
        created_at=user.created_at.isoformat(),
        updated_at=user.updated_at.isoformat(),
    )


@router.get("/")
def list_users(page: int = 1, size: int = 10):
    return {"message": f"list users page={page} size={size}"}


@router.get("/{user_id}")
def get_user(user_id: str):
    return {"message": f"get user {user_id}"}


@router.put("/{user_id}")
def update_user(user_id: str):
    return {"message": f"update user {user_id}"}


@router.delete("/{user_id}")
def delete_user(user_id: str):
    return {"message": f"delete user {user_id}"}
