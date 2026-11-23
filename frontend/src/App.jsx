import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";
import RutaPorArea from "./components/RutaPorArea";
import { AuthProvider } from "./context/AuthContext";
import InicioPage from "./pages/InicioPage";
import LoginPage from "./pages/LoginPage";
import Perfil from "./panel/sprint2/Perfil";
import Notificaciones from "./panel/sprint2/Notificaciones";
import Invitacion from "./pages/Invitacion";
import ConfirmarReferido from "./pages/ConfirmarReferido";
import VerificarCertificado from "./pages/VerificarCertificado";
import PanelRol from "./panel/PanelRol";
import RecuperarPage from "./pages/RecuperarPage";
import RegistroPage from "./pages/RegistroPage";
import RestablecerPage from "./pages/RestablecerPage";
import CuentaGeneral from "./pages/CuentaGeneral";
import { RUTA_DE_AREA } from "./utils/areas";

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<InicioPage />} />
          <Route path="/ingresar" element={<LoginPage />} />
          <Route path="/registro" element={<RegistroPage />} />
          {Object.entries(RUTA_DE_AREA).map(([area, ruta]) => (
            <Route key={area} path={`${ruta}/*`}
                   element={<RutaPorArea area={area}><PanelRol area={area} /></RutaPorArea>} />
          ))}
          <Route path="/recuperar" element={<RecuperarPage />} />
          <Route path="/restablecer" element={<RestablecerPage />} />
          <Route path="/mi-cuenta" element={<CuentaGeneral />} />
          <Route path="/mi-perfil" element={<main className="s2-centrado"><Perfil /></main>} />
          <Route path="/mis-notificaciones" element={<main className="s2-centrado"><Notificaciones /></main>} />
          <Route path="/invitacion/:codigo" element={<Invitacion />} />
          <Route path="/confirmar-referido/:token" element={<ConfirmarReferido />} />
          <Route path="/verificar-certificado/:codigo?" element={<VerificarCertificado />} />
          <Route path="/sin-rol" element={<Navigate to="/mi-cuenta" replace />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}
