import { Navigate, useLocation } from "react-router-dom";
import AuthLayout from "../components/AuthLayout";
import FormLogin from "../components/FormLogin";
import { useAuth } from "../context/AuthContext";
import { rutaDe } from "../utils/areas";

export default function LoginPage() {
  const { usuario, verificando } = useAuth();
  const { state } = useLocation();   // el registro manda aquí con el aviso «¡Cuenta creada!»
  if (!verificando && usuario) return <Navigate to={rutaDe(usuario.area)} replace />;
  return (
    <AuthLayout etiqueta="Iniciar sesión">
      <FormLogin aviso={state?.aviso || ""} />
    </AuthLayout>
  );
}
