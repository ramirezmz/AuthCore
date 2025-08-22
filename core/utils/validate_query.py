from typing import Optional
from fastapi import Query
from pydantic import BaseModel


class UserQuery(BaseModel):
    page: int = 1
    limit: int = 10
    role: Optional[str] = None
    q: Optional[str] = None
    order: int = 1


def validate_query(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    role: Optional[str] = Query(None),
    q: Optional[str] = Query(None),
    order: int = Query(1)
) -> UserQuery:
    return UserQuery(
        page=page,
        limit=limit,
        role=role,
        q=q,
        order=order,
    )
