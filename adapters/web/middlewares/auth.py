from fastapi import Header, HTTPException, status
from adapters.auth.jwt_auth_service import decode_token
from datetime import datetime


def validate_session(
    authorization: str = Header(None)
):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token ausente ou inválido"
        )
    token = authorization.split("Bearer ")[1]
    payload = decode_token(token)
    if "error" in payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=payload["error"])

    exp = payload.get("exp")
    if exp is None or int(exp) < int(datetime.utcnow().timestamp()):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expirado"
        )
    # TODO: Implement query to validate token in db
    return payload
