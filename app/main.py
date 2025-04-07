from fastapi import FastAPI
from socketio import Middleware

from app.core.database import engine, Base
from app.routers import users, roles, auth, permissions, role_permissions, products, orders, notes, tenants
from app.middleware.auth_middleware import LoggingMiddleware
from app.middleware.tenant_middleware import TenantMiddleware
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

# Common middleware (TenantMiddleware is always used)
app.add_middleware(TenantMiddleware)

app.include_router(auth.router, prefix="/api")
app.include_router(users.router, prefix="/api")
app.include_router(roles.router, prefix="/api")
app.include_router(permissions.router, prefix="/api")
app.include_router(role_permissions.router, prefix="/api")
app.include_router(products.router, prefix="/api")
app.include_router(orders.router, prefix="/api")
app.include_router(notes.router, prefix="/api")
app.include_router(tenants.router, prefix="/api")


@app.get("/")
def root():
    return {"message": "Welcome to FastAPI Modular"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)