import { useEffect, useState } from "react";
import { api, getCurrentUser } from "../api";

export default function DashboardPage() {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);
  const currentUser = getCurrentUser();

  useEffect(() => {
    api.dashboard()
      .then(setData)
      .catch((err) => setError(err.status === 403 ? "Apenas administradores acessam o dashboard." : err.message));
  }, []);

  if (error) return <div className="page"><p className="error-text">{error}</p></div>;
  if (!data) return <div className="page"><p>Carregando…</p></div>;

  return (
    <div className="page">
      <h1>Dashboard agregado</h1>
      <p className="sub">
        Empresa: {currentUser?.company_name} · {data.total_respondents} respondentes na base
      </p>

      <div className="maturity-hero">
        <span className="maturity-value">{data.maturity}</span>
        <span className="maturity-label">Maturidade em IA da empresa /100</span>
      </div>

      <div className="mods3">
        <DistCard title="Prontidão" d={data.readiness} />
        <DistCard title="Literacia" d={data.literacy} />
        <DistCard title="Oportunidade" d={data.opportunity} />
      </div>
      {data.technical && (
        <div className="mods3">
          <DistCard title="Índice Técnico" d={data.technical} />
        </div>
      )}

      <h3 className="section-title">Mapa por área</h3>
      {data.by_area.map((a) => (
        <div key={a.area} className="metric">
          <div className="metric-top"><span className="name">{a.area}</span></div>
          <p className="sub">
            Prontidão: {a.readiness.mean} (n={a.readiness.n}) ·
            Literacia: {a.literacy.mean} (n={a.literacy.n}) ·
            Oportunidade: {a.opportunity.mean} (n={a.opportunity.n})
          </p>
        </div>
      ))}

      <h3 className="section-title">Distribuição do quadrante</h3>
      {data.quadrant_distribution.map((q) => (
        <div key={q.badge} className="metric">
          <div className="metric-top">
            <span className="name">{q.badge}</span>
            <span className="val">{q.count}</span>
          </div>
        </div>
      ))}
    </div>
  );
}

function DistCard({ title, d }) {
  return (
    <div className="mm">
      <b>{d.mean}</b>
      <span>{title} (n={d.n})</span>
    </div>
  );
}
