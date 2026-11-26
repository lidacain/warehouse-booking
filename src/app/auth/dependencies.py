import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel
from config.settings import get_settings

bearer_scheme = HTTPBearer(auto_error=False)


class CurrentUser(BaseModel):
    sub: str
    org_id: int
    org_type: str


def get_current_user(
    creds: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> CurrentUser:
    if creds is None:
        raise HTTPException(status_code=401, detail="Не авторизован")
    try:
        payload = jwt.decode(
            creds.credentials,
            get_settings().JWT_SECRET,
            algorithms=["HS256"],
        )
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Невалидный или просроченный токен")
    return CurrentUser(sub=payload["sub"], org_id=payload["org_id"], org_type=payload["org_type"])