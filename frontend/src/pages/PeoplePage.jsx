import { useEffect, useState } from "react";
import { api } from "../api";

const ROLE_LABELS = {
  collaborator: "Colaborador",
  manager: "Gestor",
  admin: "Admin",
};

export default function PeoplePage() {
  const [people, setPeople] = useState(null);
  const [error, setError] = useState(null);
  const [form, setForm] = useState({ name: "", email: "", password: "", role: "collaborator", area_name: "" });
  const [creating, setCreating] = useState(false);
  const [createError, setCreateError] = useState(null);

  function loadPeople() {
    api.listPeople().then(setPeople).catch((err) => setError(err.message));
  }

  useEffect(loadPeople, []);

  async function handleCreate(e) {
    e.preventDefault();
    setCreateError(null);
    setCreating(true);
    try {
      await api.createPerson({ ...form, area_name: form.area_name || null });
      setForm({ name: "", email: "", password: "", role: "collaborator", area_name: "" });
      loadPeople();
    } catch (err) {
      setCreateError(err.status === 409 ? "Já existe uma pessoa com este email." : err.message);
    } finally {
      setCreating(false);
    }
  }

  if (error) return <div className="page"><p className="error-text">{error}</p></div>;

  return (
    <div className="page">
      <h1>Pessoas</h1>
      <p className="sub">Cadastre novas pessoas na sua empresa e acompanhe quem já pode responder o assessment.</p>

      <h3 className="section-title">Nova pessoa</h3>
      <form onSubmit={handleCreate} className="login-form">
        <label>
          Nome
          <input value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} required />
        </label>
        <label>
          Email
          <input type="email" value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} required />
        </label>
        <label>
          Senha temporária
          <input type="text" value={form.password} onChange={(e) => setForm({ ...form, password: e.target.value })} required />
        </label>
        <label>
          Perfil
          <select value={form.role} onChange={(e) => setForm({ ...form, role: e.target.value })}>
            <option value="collaborator">Colaborador</option>
            <option value="manager">Gestor</option>
            <option value="admin">Admin</option>
          </select>
        </label>
        <label>
          Área (opcional)
          <input value={form.area_name} onChange={(e) => setForm({ ...form, area_name: e.target.value })} />
        </label>
        {createError && <p className="error-text">{createError}</p>}
        <button type="submit" className="cta" disabled={creating}>
          {creating ? "Cadastrando…" : "Cadastrar pessoa"}
        </button>
      </form>

      <h3 className="section-title">Pessoas cadastradas</h3>
      {!people ? (
        <p className="sub">Carregando…</p>
      ) : (
        people.map((p) => (
          <div key={p.id} className="metric">
            <div className="metric-top">
              <span className="name">{p.name}</span>
              <span className="band">{ROLE_LABELS[p.role] || p.role}</span>
            </div>
            <p className="sub">{p.email} {p.area_name ? `· ${p.area_name}` : ""}</p>
          </div>
        ))
      )}
    </div>
  );
}
