import { Navigate, useNavigate } from "react-router-dom";
import AuthLayout from "../components/AuthLayout";
import FormRegistro from "../components/FormRegistro";
import { useAuth } from "../context/AuthContext";
import { rutaDe } from "../utils/areas";

export default function RegistroPage() {
  const { usuario, verificando } = useAuth();
  const navegar = useNavigate();
  if (!verificando && usuario) return <Navigate to={rutaDe(usuario.area)} replace />;

  // Cuenta creada: se lleva al socio a iniciar sesión con un aviso de confirmación.
  const alRegistrar = (correo) =>
    navegar("/ingresar", { replace: true, state: { aviso: `¡Cuenta creada! Ya puedes iniciar sesión con ${correo}.` } });

  return (
    <AuthLayout etiqueta="Crear cuenta">
      <FormRegistro alRegistrar={alRegistrar} />
    </AuthLayout>
  );
}
