from fastapi import APIRouter, Depends, HTTPException, status
from adapters.web.schemas.user_schema import (
    AvailableUserUpdateRequest,
    UserCreateRequest,
    UserResponse,
    UserListAllResponse,
)
from core.use_cases.create_user import create_user
from core.use_cases.list_one_user import get_user
from core.use_cases.update_user import update_user
from adapters.db.sqlite_user_repository import SQLiteUserRepository
from adapters.web.middlewares.auth import validate_session
from core.utils.validate_query import validate_query, UserQuery
from core.utils.check_user_role import check_user_role

router = APIRouter(prefix="/users", tags=["users"])


def get_user_repository():
    return SQLiteUserRepository()


@router.post("/", response_model=UserResponse)
def create_user_route(
    body: UserCreateRequest,
    repo: SQLiteUserRepository = Depends(get_user_repository),
    user: dict = Depends(validate_session)
):
    check_user_role(user, ["admin", "user"])
    new_user = create_user(repo, body)

    return UserResponse(
        id=new_user.id,
        email=new_user.email,
        name=new_user.name,
        role=new_user.role,  # type: ignore
        created_at=new_user.created_at.isoformat(),
        updated_at=new_user.updated_at.isoformat(),
    )


@router.get("/", response_model=UserListAllResponse)
def list_users(
    repo: SQLiteUserRepository = Depends(get_user_repository),
    user: dict = Depends(validate_session),
    query: UserQuery = Depends(validate_query)
):
    check_user_role(user, ["admin", "user"])
    return repo.get_all_users(query)


@router.get("/{user_id}", response_model=UserResponse)
def get_user_route(
    user_id: str,
    repo: SQLiteUserRepository = Depends(get_user_repository),
    user: dict = Depends(validate_session)
):
    check_user_role(user, ["admin", "user"])
    return get_user(repo, user_id)


@router.put("/{user_id}", response_model=UserResponse)
def update_user_route(
    user_id: str,
    payload: AvailableUserUpdateRequest,
    repo: SQLiteUserRepository = Depends(get_user_repository),
    user: dict = Depends(validate_session)
):
    check_user_role(user, ["admin", "user"])
    result = update_user(repo, user_id=user_id, user_data=payload)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return result


@router.delete("/{user_id}")
def delete_user(
    user_id: str,
    repo: SQLiteUserRepository = Depends(get_user_repository),
    user: dict = Depends(validate_session)
):
    check_user_role(user, ["admin"])
    result = repo.delete_user(user_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return {"message": f"User {user_id} deleted successfully"}
