import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";
import RutaPorArea from "./components/RutaPorArea";
import { AuthProvider } from "./context/AuthContext";
import InicioPage from "./pages/InicioPage";
import LoginPage from "./pages/LoginPage";
import PanelArea from "./pages/PanelArea";
import PanelRol from "./panel/PanelRol";
import RecuperarPage from "./pages/RecuperarPage";
import RegistroPage from "./pages/RegistroPage";
import RestablecerPage from "./pages/RestablecerPage";
import SinRol from "./pages/SinRol";
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
            <Route key={area} path={["socio", "marketing", "admin"].includes(area) ? `${ruta}/*` : ruta}
                   element={<RutaPorArea area={area}>{["socio", "marketing", "admin"].includes(area)
                     ? <PanelRol area={area} /> : <PanelArea area={area} />}</RutaPorArea>} />
          ))}
          <Route path="/recuperar" element={<RecuperarPage />} />
          <Route path="/restablecer" element={<RestablecerPage />} />
          <Route path="/sin-rol" element={<SinRol />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}
