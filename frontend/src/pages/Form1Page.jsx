import { useMemo, useState } from "react";
import { Link } from "react-router-dom";
import { FORM1_SECTIONS, FORM1_REQUIRED_IDS } from "../formSchemas/form1";
import QuestionField from "../components/QuestionField";
import { api } from "../api";

export default function Form1Page() {
  const [answers, setAnswers] = useState({});
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [submitting, setSubmitting] = useState(false);

  const answeredCount = useMemo(
    () => FORM1_REQUIRED_IDS.filter((id) => {
      const v = answers[id];
      return Array.isArray(v) ? v.length > 0 : v !== undefined;
    }).length,
    [answers]
  );
  const total = FORM1_REQUIRED_IDS.length;
  const complete = answeredCount === total;

  function setAnswer(id, value) {
    setAnswers((prev) => ({ ...prev, [id]: value }));
  }

  async function handleSubmit() {
    setError(null);
    setSubmitting(true);
    try {
      const res = await api.submitForm1(answers);
      setResult(res);
    } catch (err) {
      if (err.status === 409) {
        setError("Você já respondeu este formulário nesta versão do instrumento.");
      } else if (err.status === 401) {
        setError("Sua sessão expirou. Faça login novamente.");
      } else {
        setError(err.message || "Não foi possível enviar suas respostas.");
      }
    } finally {
      setSubmitting(false);
    }
  }

  if (result) {
    return (
      <div className="page">
        <h1>Seu resultado</h1>
        <Metric name="Prontidão percebida" value={result.readiness} band={result.readiness_band} />
        <div className="mods3">
          <div className="mm"><b>{result.m1_idx}</b><span>Organização</span></div>
          <div className="mm"><b>{result.m2_idx}</b><span>Times</span></div>
          <div className="mm"><b>{result.m3_idx}</b><span>Pessoas</span></div>
        </div>
        <Metric name="Literacia em IA" value={result.literacy} band={result.literacy_band} sub={`Checagem objetiva: ${result.objective_correct} de 6 acertos.`} />
        <Metric name="Oportunidade no trabalho" value={result.opportunity} sub={`Automatabilidade: ${result.automatability_label}`} />
        <div className="quad">
          <span className="qbadge">{result.quadrant_badge}</span>
          <h4>{result.quadrant_title}</h4>
          <p>{result.quadrant_text}</p>
          {result.quadrant_provisional && (
            <p className="hint">Quadrante provisório — poucos respondentes na base ainda para usar percentil.</p>
          )}
        </div>
        <Link to="/formulario-2" className="cta ghost">Ir para o Formulário Técnico (gestores)</Link>
      </div>
    );
  }

  return (
    <div className="page">
      <header className="form-header">
        <h1>Diagnóstico Geral de Prontidão em IA</h1>
        <span className="count">{answeredCount} / {total}</span>
      </header>
      {FORM1_SECTIONS.map((sec) => (
        <section key={sec.tag}>
          <h3 className="section-title">{sec.tag} · {sec.title}</h3>
          {sec.items.map((item) => (
            <QuestionField
              key={item.id}
              item={item}
              value={answers[item.id]}
              onChange={(v) => setAnswer(item.id, v)}
            />
          ))}
        </section>
      ))}
      {error && <p className="error-text">{error}</p>}
      <button type="button" className="cta" disabled={!complete || submitting} onClick={handleSubmit}>
        {submitting ? "Enviando…" : complete ? "Ver meu resultado" : `${total - answeredCount} perguntas restantes`}
      </button>
    </div>
  );
}

function Metric({ name, value, band, sub }) {
  return (
    <div className="metric">
      <div className="metric-top">
        <span className="name">{name}</span>
        <span className="val">{value}<small>/100</small></span>
      </div>
      <div className="gauge"><i style={{ width: `${value}%` }} /></div>
      {band && <span className="band">{band}</span>}
      {sub && <p className="sub">{sub}</p>}
    </div>
  );
}
