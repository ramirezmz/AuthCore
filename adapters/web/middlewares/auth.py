from fastapi import Depends, HTTPException, status
from adapters.auth.jwt_auth_service import decode_token
from datetime import datetime
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


security = HTTPBearer()


def validate_session(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    if not credentials or not credentials.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token ausente ou inválido"
        )
    token = credentials.credentials
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
