from fastapi import FastAPI
from socketio import Middleware

from app.core.database import engine, Base
from app.routers import user, role, auth, permission, role_permission
from app.middleware.auth_middleware import LoggingMiddleware
from starlette.middleware.cors import CORSMiddleware

from app.core.database import SessionLocal
from app.seeder import run_seeders

# Database Initialization
Base.metadata.create_all(bind=engine)

# Run Seeder
db = SessionLocal()
run_seeders(db)
db.close()

app = FastAPI(
    title="Modularized FastAPI",
)

app.add_middleware(LoggingMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api")
app.include_router(user.router, prefix="/api")
app.include_router(role.router, prefix="/api")
app.include_router(permission.router, prefix="/api")
app.include_router(role_permission.router, prefix="/api")

@app.get("/")
def root():
    return {"message": "Welcome to FastAPI Modular"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)