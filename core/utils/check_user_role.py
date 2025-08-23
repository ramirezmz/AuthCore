from fastapi import HTTPException, status


def check_user_role(user: dict, allowed_roles: list[str]):
    if user.get("role") not in allowed_roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado"
        )
