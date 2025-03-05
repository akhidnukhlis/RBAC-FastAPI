import jwt
from fastapi import Depends, HTTPException, Security
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.repositories.role_permission import check_role_permission
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.config import settings

security = HTTPBearer()


def require_permission(permission_id: int):
    def permission_dependency(
            credentials: HTTPAuthorizationCredentials = Security(security),
            db: Session = Depends(get_db)
    ):
        try:
            payload = jwt.decode(credentials.credentials, settings.SECRET_KEY, algorithms=["HS256"])
            role_id = payload.get("role_id")

            if role_id is None:
                raise HTTPException(status_code=401, detail="Invalid token: role_id not found")

            if not check_role_permission(db, role_id, permission_id):
                raise HTTPException(status_code=403, detail="You do not have permission to access this resource")

            return True

        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired")

        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")

    return permission_dependency
