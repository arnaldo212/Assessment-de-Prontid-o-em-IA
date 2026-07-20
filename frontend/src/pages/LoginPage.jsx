import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { api, saveTokens, saveCurrentUser } from "../api";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  async function handleSubmit(e) {
    e.preventDefault();
    setError(null);
    setLoading(true);
    try {
      const tokens = await api.login(email, password);
      saveTokens(tokens);
      const me = await api.me();
      saveCurrentUser(me);
      navigate("/formulario-1");
    } catch (err) {
      setError(err.status === 401 ? "Email ou senha inválidos." : "Não foi possível entrar. Tente novamente.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="page-narrow">
      <h1>Diagnóstico de Prontidão em IA</h1>
      <p className="sub">Entre com sua conta para responder o assessment.</p>
      <form onSubmit={handleSubmit} className="login-form">
        <label>
          Email
          <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
        </label>
        <label>
          Senha
          <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
        </label>
        {error && <p className="error-text">{error}</p>}
        <button type="submit" className="cta" disabled={loading}>
          {loading ? "Entrando…" : "Entrar"}
        </button>
      </form>
    </div>
  );
}
