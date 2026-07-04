from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.routers import auth, tests, public, dashboard, billing, templates
from app.config import settings

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Quiz Platform API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url, "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(tests.router)
app.include_router(public.router)
app.include_router(dashboard.router)
app.include_router(billing.router)
app.include_router(templates.router)


@app.get("/health")
def health_check():
    return {"status": "ok"}
