from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import require_roles
from app.models import Area, Role, User
from app.schemas import PersonCreateRequest, PersonOut
from app.security import hash_password

router = APIRouter(prefix="/people", tags=["people"])


def _get_or_create_area(db: Session, company_id, area_name: str | None) -> Area | None:
    if not area_name:
        return None
    area = db.query(Area).filter(Area.company_id == company_id, Area.name == area_name).first()
    if area is None:
        area = Area(company_id=company_id, name=area_name)
        db.add(area)
        db.flush()
    return area


def _to_person_out(user: User) -> PersonOut:
    return PersonOut(
        id=user.id,
        name=user.name,
        email=user.email,
        role=user.role,
        area_name=user.area.name if user.area else None,
    )


@router.get("", response_model=list[PersonOut])
def list_people(
    admin: User = Depends(require_roles(Role.admin)),
    db: Session = Depends(get_db),
) -> list[PersonOut]:
    users = db.query(User).filter(User.company_id == admin.company_id).order_by(User.name).all()
    return [_to_person_out(u) for u in users]


@router.post("", response_model=PersonOut, status_code=status.HTTP_201_CREATED)
def create_person(
    payload: PersonCreateRequest,
    admin: User = Depends(require_roles(Role.admin)),
    db: Session = Depends(get_db),
) -> PersonOut:
    area = _get_or_create_area(db, admin.company_id, payload.area_name)

    user = User(
        company_id=admin.company_id,
        area_id=area.id if area else None,
        name=payload.name,
        email=payload.email,
        hashed_password=hash_password(payload.password),
        role=payload.role,
    )
    db.add(user)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Já existe uma pessoa cadastrada com este email.",
        ) from exc

    db.refresh(user)
    return _to_person_out(user)
