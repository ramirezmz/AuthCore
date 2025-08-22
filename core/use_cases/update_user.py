from fastapi import HTTPException, status
from core.ports.user_repository import UserRepository
from adapters.web.schemas.user_schema import AvailableUserUpdateRequest


def update_user(
        user_repository: UserRepository,
        user_id: str,
        user_data: AvailableUserUpdateRequest
):
    target_user = user_repository.get_user_by_id(user_id)
    if not target_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    updated_user = target_user.merge(user_data)
    return user_repository.update_one_user(user_id, updated_user)
