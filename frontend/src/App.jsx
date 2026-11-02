import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";
import RutaPorArea from "./components/RutaPorArea";
import { AuthProvider } from "./context/AuthContext";
import AuthPage from "./pages/AuthPage";
import PanelArea from "./pages/PanelArea";
import RecuperarPage from "./pages/RecuperarPage";
import RestablecerPage from "./pages/RestablecerPage";
import SinRol from "./pages/SinRol";
import { RUTA_DE_AREA } from "./utils/areas";

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<AuthPage />} />
          {Object.entries(RUTA_DE_AREA).map(([area, ruta]) => (
            <Route key={area} path={ruta}
                   element={<RutaPorArea area={area}><PanelArea area={area} /></RutaPorArea>} />
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
