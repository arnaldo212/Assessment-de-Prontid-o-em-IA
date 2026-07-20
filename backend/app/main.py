from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.routers import auth, dashboard, forms, people

settings = get_settings()

app = FastAPI(
    title="Assessment de Prontidão em IA",
    version="0.1.0",
    description="API multiusuário para diagnóstico de prontidão em IA (organização, times, pessoas, literacia, oportunidade e índice técnico).",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.cors_origins] if settings.cors_origins != "*" else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(forms.router)
app.include_router(dashboard.router)
app.include_router(people.router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
