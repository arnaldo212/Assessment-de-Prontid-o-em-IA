from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import aggregation
from app.database import get_db
from app.deps import require_roles
from app.models import Area, Form1Response, Form2Response, Role, User
from app.scoring import compute_quadrant
from app.schemas import AreaBreakdownOut, DashboardOut, DistributionOut, QuadrantCountOut

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


def _to_distribution_out(d: aggregation.Distribution) -> DistributionOut:
    return DistributionOut(mean=d.mean, median=d.median, stdev=d.stdev, n=d.n)


@router.get("", response_model=DashboardOut)
def get_dashboard(
    admin: User = Depends(require_roles(Role.admin)),
    db: Session = Depends(get_db),
) -> DashboardOut:
    rows = (
        db.query(Form1Response, Area.name)
        .join(User, Form1Response.user_id == User.id)
        .outerjoin(Area, User.area_id == Area.id)
        .filter(User.company_id == admin.company_id)
        .all()
    )

    registros = [
        {
            "area": area_name,
            "readiness": resp.readiness,
            "literacy": resp.literacy,
            "opportunity": resp.opportunity,
        }
        for resp, area_name in rows
    ]

    readiness_vals = [r["readiness"] for r in registros]
    literacy_vals = [r["literacy"] for r in registros]
    opportunity_vals = [r["opportunity"] for r in registros]

    by_area_grouped = aggregation.group_by_area(registros)
    by_area = [
        AreaBreakdownOut(
            area=area,
            readiness=_to_distribution_out(aggregation.distribution([r["readiness"] for r in regs])),
            literacy=_to_distribution_out(aggregation.distribution([r["literacy"] for r in regs])),
            opportunity=_to_distribution_out(aggregation.distribution([r["opportunity"] for r in regs])),
        )
        for area, regs in by_area_grouped.items()
    ]

    badges = []
    for r in registros:
        q = compute_quadrant(r["literacy"], r["opportunity"], literacy_vals, opportunity_vals)
        badges.append(q.badge)
    quad_counts = aggregation.quadrant_distribution(badges)
    quadrant_distribution = [QuadrantCountOut(badge=b, count=c) for b, c in quad_counts.items()]

    technical_vals = [
        r.technical_idx
        for r in (
            db.query(Form2Response)
            .join(User, Form2Response.user_id == User.id)
            .filter(User.company_id == admin.company_id)
            .all()
        )
    ]
    technical_out = _to_distribution_out(aggregation.distribution(technical_vals)) if technical_vals else None

    readiness_dist = aggregation.distribution(readiness_vals)
    literacy_dist = aggregation.distribution(literacy_vals)
    opportunity_dist = aggregation.distribution(opportunity_vals)
    maturity = (
        aggregation.company_maturity(readiness_dist.mean, literacy_dist.mean, opportunity_dist.mean)
        if registros
        else 0
    )

    return DashboardOut(
        total_respondents=len(registros),
        maturity=maturity,
        readiness=_to_distribution_out(readiness_dist),
        literacy=_to_distribution_out(literacy_dist),
        opportunity=_to_distribution_out(opportunity_dist),
        technical=technical_out,
        by_area=by_area,
        quadrant_distribution=quadrant_distribution,
    )
