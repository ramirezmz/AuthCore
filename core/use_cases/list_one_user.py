from fastapi import HTTPException, status
from core.ports.user_repository import UserRepository


def get_user(user_repository: UserRepository, user_id: str):
    user = user_repository.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user
