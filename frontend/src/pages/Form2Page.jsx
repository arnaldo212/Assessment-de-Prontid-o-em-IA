import { useMemo, useState } from "react";
import { FORM2_ITEMS, FORM2_REQUIRED_IDS } from "../formSchemas/form2";
import QuestionField from "../components/QuestionField";
import { api } from "../api";

export default function Form2Page() {
  const [answers, setAnswers] = useState({});
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [submitting, setSubmitting] = useState(false);

  const answeredCount = useMemo(
    () => FORM2_REQUIRED_IDS.filter((id) => answers[id] !== undefined).length,
    [answers]
  );
  const total = FORM2_REQUIRED_IDS.length;
  const complete = answeredCount === total;

  function setAnswer(id, value) {
    setAnswers((prev) => ({ ...prev, [id]: value }));
  }

  async function handleSubmit() {
    setError(null);
    setSubmitting(true);
    try {
      const res = await api.submitForm2(answers);
      setResult(res);
    } catch (err) {
      if (err.status === 403) {
        setError("Este formulário é exclusivo para gestores/liderança técnica.");
      } else if (err.status === 409) {
        setError("Você já respondeu este formulário nesta versão do instrumento.");
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
        <h1>Índice Técnico (Módulo 4)</h1>
        <div className="metric">
          <div className="metric-top">
            <span className="name">Índice Técnico</span>
            <span className="val">{result.technical_idx}<small>/100</small></span>
          </div>
          <div className="gauge"><i style={{ width: `${result.technical_idx}%` }} /></div>
          <span className="band">{result.technical_band}</span>
        </div>
      </div>
    );
  }

  return (
    <div className="page">
      <header className="form-header">
        <h1>Diagnóstico Técnico (Módulo 4)</h1>
        <span className="count">{answeredCount} / {total}</span>
      </header>
      <p className="sub">Exclusivo para gestores, diretores e responsáveis por tecnologia.</p>
      {FORM2_ITEMS.map((item) => (
        <QuestionField key={item.id} item={item} value={answers[item.id]} onChange={(v) => setAnswer(item.id, v)} />
      ))}
      {error && <p className="error-text">{error}</p>}
      <button type="button" className="cta" disabled={!complete || submitting} onClick={handleSubmit}>
        {submitting ? "Enviando…" : complete ? "Ver resultado" : `${total - answeredCount} perguntas restantes`}
      </button>
    </div>
  );
}
