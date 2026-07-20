import { Link, useNavigate } from "react-router-dom";
import { getCurrentUser, clearTokens } from "../api";

export default function NavBar() {
  const user = getCurrentUser();
  const navigate = useNavigate();

  if (!user) return null;

  function handleLogout() {
    clearTokens();
    navigate("/login");
  }

  return (
    <nav className="navbar">
      <Link to="/formulario-1">Formulário 1</Link>
      {(user.role === "manager" || user.role === "admin") && (
        <Link to="/formulario-2">Formulário 2</Link>
      )}
      {user.role === "admin" && <Link to="/dashboard">Dashboard</Link>}
      {user.role === "admin" && <Link to="/pessoas">Pessoas</Link>}
      <span className="navbar-spacer" />
      <span className="navbar-email">{user.name || user.email} · {user.company_name}</span>
      <button type="button" className="navbar-logout" onClick={handleLogout}>Sair</button>
    </nav>
  );
}
