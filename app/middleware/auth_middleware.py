import datetime
from jose import jwt
from sqlalchemy.orm import Session
from fastapi import HTTPException, Security, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.config import settings
from app.core.database import db_manager
from app.repositories.user_repository import UsersRepository

class AuthMiddleware:
    def __init__(self):
        self.security = HTTPBearer()
        self.secret_key = settings.SECRET_KEY
        self.algorithm = settings.ALGORITHM

    def verify_token(self, token: str, db: Session):
        """
        Logika inti untuk memverifikasi token JWT dan keberadaan user di database.
        """
        try:
            # 1. Decode Payload
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            
            # 2. Cek User berdasarkan token di DB
            user_repo = UsersRepository(db)
            user = user_repo.get_user_by_access_token(token)
            if not user:
                raise HTTPException(status_code=401, detail="Unauthorized: User not found or token invalid")

            # 3. Cek Expiration (Opsional jika jwt.decode sudah memvalidasi 'exp')
            exp_time = datetime.datetime.utcfromtimestamp(payload.get("exp"))
            if datetime.datetime.utcnow() > exp_time:
                raise HTTPException(status_code=401, detail="Access token expired")

            # 4. Return data user yang dibutuhkan
            return {
                "user_id": user.id,
                "role_id": user.role_id,
                "status_id": user.status_id,
                "email": user.email,
            }

        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expired")
        except jwt.JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")
        except Exception as e:
            raise HTTPException(status_code=401, detail=f"Could not validate credentials: {str(e)}")

    async def __call__(
        self, 
        credentials: HTTPAuthorizationCredentials = Security(HTTPBearer()), 
        db: Session = Depends(db_manager.get_db)
    ):
        """
        Method __call__ membuat class ini bisa langsung digunakan 
        sebagai Dependency di FastAPI: Depends(AuthMiddleware())
        """
        token = credentials.credentials
        return self.verify_token(token, db)

# Inisialisasi instance untuk digunakan di router
auth_handler = AuthMiddleware()