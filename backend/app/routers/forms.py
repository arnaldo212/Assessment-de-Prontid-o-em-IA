from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app import scoring_service
from app.database import get_db
from app.deps import get_current_user, require_roles
from app.models import Form1Response, Form2Response, InstrumentVersion, Role, User
from app.scoring import compute_quadrant
from app.schemas import (
    Form1ResultOut,
    Form1SubmitRequest,
    Form2ResultOut,
    Form2SubmitRequest,
)

router = APIRouter(prefix="/forms", tags=["forms"])


def _active_instrument_version(db: Session) -> InstrumentVersion:
    version = db.query(InstrumentVersion).filter(InstrumentVersion.is_active.is_(True)).first()
    if version is None:
        raise HTTPException(
            status_code=500,
            detail="Nenhuma versão ativa do instrumento — configure uma InstrumentVersion antes de aceitar respostas.",
        )
    return version


def _distributions_for_quadrant(db: Session, company_id) -> tuple[list[float], list[float]]:
    """
    Distribuição de referência para o cálculo de percentil do quadrante.
    Escopada pela empresa do respondente (specs/01-scoring/requirements.md,
    seção 7: "a distribuição de referência é o conjunto de respostas já
    registradas — escopo: mesma empresa").
    """
    rows = (
        db.query(Form1Response.literacy, Form1Response.opportunity)
        .join(User, Form1Response.user_id == User.id)
        .filter(User.company_id == company_id)
        .all()
    )
    literacia = [r[0] for r in rows]
    oportunidade = [r[1] for r in rows]
    return literacia, oportunidade


@router.post("/form1", response_model=Form1ResultOut, status_code=status.HTTP_201_CREATED)
def submit_form1(
    payload: Form1SubmitRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Form1ResultOut:
    version = _active_instrument_version(db)
    computed = scoring_service.compute_form1(payload.answers)

    response = Form1Response(
        user_id=user.id,
        instrument_version_id=version.id,
        answers=payload.answers,
        m1_raw=computed["m1"].raw, m1_idx=computed["m1"].idx,
        m2_raw=computed["m2"].raw, m2_idx=computed["m2"].idx,
        m3_raw=computed["m3"].raw, m3_idx=computed["m3"].idx,
        readiness=computed["readiness"],
        literacy=computed["literacy"],
        opportunity=computed["opportunity"],
        objective_correct=computed["objective_correct"],
        automatability_label=computed["automatability_label"],
    )
    db.add(response)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Você já respondeu o Formulário 1 nesta versão do instrumento.",
        ) from exc

    dist_lit, dist_opp = _distributions_for_quadrant(db, user.company_id)
    quad = compute_quadrant(computed["literacy"], computed["opportunity"], dist_lit, dist_opp)

    return Form1ResultOut(
        m1_idx=computed["m1"].idx, m2_idx=computed["m2"].idx, m3_idx=computed["m3"].idx,
        readiness=computed["readiness"], readiness_band=computed["readiness_band"],
        literacy=computed["literacy"], literacy_band=computed["literacy_band"],
        objective_correct=computed["objective_correct"],
        opportunity=computed["opportunity"], automatability_label=computed["automatability_label"],
        quadrant_badge=quad.badge, quadrant_title=quad.title, quadrant_text=quad.text,
        quadrant_provisional=quad.provisorio,
    )


@router.post("/form2", response_model=Form2ResultOut, status_code=status.HTTP_201_CREATED)
def submit_form2(
    payload: Form2SubmitRequest,
    user: User = Depends(require_roles(Role.manager, Role.admin)),
    db: Session = Depends(get_db),
) -> Form2ResultOut:
    version = _active_instrument_version(db)
    computed = scoring_service.compute_form2(payload.answers)

    response = Form2Response(
        user_id=user.id,
        instrument_version_id=version.id,
        answers=payload.answers,
        technical_idx=computed["technical_idx"],
    )
    db.add(response)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Você já respondeu o Formulário 2 nesta versão do instrumento.",
        ) from exc

    return Form2ResultOut(**computed)
