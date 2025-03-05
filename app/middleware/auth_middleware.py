import time
import datetime
import jwt
import logging
from sqlalchemy.orm import Session
from fastapi import Request
from app.core.database import get_db
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Depends, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.repositories.user import get_user_by_access_token
from app.core.config import settings

security = HTTPBearer()

logging.basicConfig(filename="logs/app.log", level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time

        print(f"Request to {request.url.path} took {process_time:.2f} sec")

        log_message = f"{request.method} {request.url.path} - {response.status_code} - {process_time:.4f}s"
        logging.info(log_message)

        return response

def verify_token(token: str, db: Session):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user = get_user_by_access_token(db, token)

        if not user:
            raise HTTPException(status_code=401, detail="Unauthorized")

        exp_time = datetime.datetime.utcfromtimestamp(payload.get("exp"))
        if datetime.datetime.utcnow() > exp_time:
            raise HTTPException(status_code=401, detail="Access token expired")

        return {
            "user_id": user.id,
            "role_id": user.role_id,
            "status_id": user.status_id,
            "email": user.email,
        }

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

def auth_middleware(credentials: HTTPAuthorizationCredentials = Security(security), db: Session = Depends(get_db)):
    token = credentials.credentials
    return verify_token(token, db)
