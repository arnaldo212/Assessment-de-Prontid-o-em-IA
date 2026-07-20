import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { isAuthenticated } from "./api";
import NavBar from "./components/NavBar";
import LoginPage from "./pages/LoginPage";
import Form1Page from "./pages/Form1Page";
import Form2Page from "./pages/Form2Page";
import DashboardPage from "./pages/DashboardPage";
import PeoplePage from "./pages/PeoplePage";

function RequireAuth({ children }) {
  if (!isAuthenticated()) return <Navigate to="/login" replace />;
  return (
    <>
      <NavBar />
      {children}
    </>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/formulario-1" element={<RequireAuth><Form1Page /></RequireAuth>} />
        <Route path="/formulario-2" element={<RequireAuth><Form2Page /></RequireAuth>} />
        <Route path="/dashboard" element={<RequireAuth><DashboardPage /></RequireAuth>} />
        <Route path="/pessoas" element={<RequireAuth><PeoplePage /></RequireAuth>} />
        <Route path="*" element={<Navigate to={isAuthenticated() ? "/formulario-1" : "/login"} replace />} />
      </Routes>
    </BrowserRouter>
  );
}
