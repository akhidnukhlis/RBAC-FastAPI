from fastapi import Request, HTTPException, Depends
from app.middleware.auth_middleware import auth_handler

from app.core.database import db_manager
from app.repositories import role_permission_repository

class PermissionMiddleware:
    def __init__(self, required_permission_id: int):
        self.required_permission_id = required_permission_id

    async def __call__(self, request: Request, user_data: dict = Depends(auth_handler)):
        if not user_data:
             raise HTTPException(status_code=401, detail="Unauthorized")

        role_id = user_data.get("role_id")
        if not role_id:
            raise HTTPException(status_code=403, detail="Forbidden: User has no role assigned")

        # Check Superadmin (Role ID 1) - Bypass check
        if role_id == 1:
            return True

        # Check Permission in Database
        # Note: In high traffic apps, cache this check (Redis) or put permissions in JWT
        db = next(db_manager.get_db())
        repo = role_permission_repository.RolePermissionRepository(db)
        
        has_permission = repo.check_permission_exists(role_id, self.required_permission_id)
        
        if not has_permission:
            raise HTTPException(status_code=403, detail="Forbidden: You do not have permission to access this resource")

        return True
