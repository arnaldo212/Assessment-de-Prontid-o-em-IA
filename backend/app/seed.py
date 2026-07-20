"""
Seed inicial: cria uma empresa, a primeira versão do instrumento (v1,
igual aos pesos/cortes dos protótipos) e sete usuários de exemplo
espalhados em áreas diferentes — o suficiente para o mapa por área do
dashboard ter mais de um grupo com >=3 respondentes depois que todos
responderem o Formulário 1. Rode com: `python -m app.seed` dentro do
container.
"""
from __future__ import annotations

from app.database import SessionLocal
from app.models import Area, Company, InstrumentVersion, Role, User
from app.security import hash_password

DEFAULT_WEIGHTS = {
    "literacy": {"self": 0.50, "breadth": 0.15, "objective": 0.35},
    "readiness_band_cuts": {"fundamentos_max": 52, "zona_incerta_max": 63},
    "technical_band_cuts": {"fragil_max": 40, "construcao_max": 65},
    "quadrant_percentile_cuts": {"baixa_max": 40, "alta_min": 60},
    "quadrant_min_respondentes_percentil": 5,
}

# (nome, email, perfil, área)
SEED_PEOPLE = [
    ("Ana Colaboradora", "colaborador@demo.com", Role.collaborator, "Tecnologia"),
    ("Bruno Gestor", "gestor@demo.com", Role.manager, "Tecnologia"),
    ("Carla Admin", "admin@demo.com", Role.admin, "Tecnologia"),
    ("Diego Marketing", "colaborador2@demo.com", Role.collaborator, "Marketing"),
    ("Elisa Vendas", "colaborador3@demo.com", Role.collaborator, "Vendas"),
    ("Fabio Financeiro", "gestor2@demo.com", Role.manager, "Financeiro"),
    ("Gabriela Operações", "colaborador4@demo.com", Role.collaborator, "Operações"),
]


def run() -> None:
    db = SessionLocal()
    try:
        company = db.query(Company).filter(Company.name == "Empresa Demo").first()
        if company is None:
            company = Company(name="Empresa Demo")
            db.add(company)
            db.flush()

        version = db.query(InstrumentVersion).filter(InstrumentVersion.label == "v1").first()
        if version is None:
            version = InstrumentVersion(label="v1", weights=DEFAULT_WEIGHTS, is_active=True)
            db.add(version)

        areas_cache: dict[str, Area] = {}
        for name, email, role, area_name in SEED_PEOPLE:
            area = areas_cache.get(area_name)
            if area is None:
                area = db.query(Area).filter(Area.company_id == company.id, Area.name == area_name).first()
                if area is None:
                    area = Area(company_id=company.id, name=area_name)
                    db.add(area)
                    db.flush()
                areas_cache[area_name] = area

            existing = db.query(User).filter(User.email == email).first()
            if existing is None:
                db.add(
                    User(
                        company_id=company.id,
                        area_id=area.id,
                        name=name,
                        email=email,
                        hashed_password=hash_password("trocar123"),
                        role=role,
                    )
                )
            elif not existing.name:
                existing.name = name

        db.commit()
        print(f"Seed concluído: empresa, versão v1 do instrumento e {len(SEED_PEOPLE)} usuários (senha: trocar123)")
    finally:
        db.close()


if __name__ == "__main__":
    run()
