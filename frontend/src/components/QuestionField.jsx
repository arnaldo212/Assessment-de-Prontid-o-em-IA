export default function QuestionField({ item, value, onChange }) {
  if (item.type === "likert") {
    return (
      <div className="question">
        <p className="question-label">
          {item.label} {item.rev && <span className="rev-badge">R</span>}
        </p>
        <div className="likert-row">
          {[1, 2, 3, 4, 5].map((v) => (
            <button
              key={v}
              type="button"
              className={value === v ? "likert-btn active" : "likert-btn"}
              onClick={() => onChange(v)}
            >
              {v}
            </button>
          ))}
        </div>
        <div className="likert-ends">
          <span>1 · discordo</span>
          <span>concordo · 5</span>
        </div>
      </div>
    );
  }

  if (item.type === "ladder" || item.type === "objective") {
    return (
      <div className="question">
        <p className="question-label">{item.label}</p>
        <div className="opts-col">
          {item.opts.map((txt, i) => {
            const optValue = item.type === "objective" ? i : i + 1;
            return (
              <button
                key={txt}
                type="button"
                className={value === optValue ? "opt active" : "opt"}
                onClick={() => onChange(optValue)}
              >
                {txt}
              </button>
            );
          })}
        </div>
      </div>
    );
  }

  if (item.type === "multicheck") {
    const chosen = value || [];
    const toggle = (txt) => {
      const next = chosen.includes(txt) ? chosen.filter((t) => t !== txt) : [...chosen, txt];
      onChange(next);
    };
    return (
      <div className="question">
        <p className="question-label">{item.label}</p>
        <div className="opts-col">
          {item.opts.map((txt) => (
            <button
              key={txt}
              type="button"
              className={chosen.includes(txt) ? "opt active" : "opt"}
              onClick={() => toggle(txt)}
            >
              {txt}
            </button>
          ))}
        </div>
      </div>
    );
  }

  return null;
}
