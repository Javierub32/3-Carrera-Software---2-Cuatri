import { Navigate, Outlet } from 'react-router-dom';
import { useAuth } from '../auth/useAuthHook';

export default function RutaProtegida({ children }) {
  const { estaAutenticado } = useAuth();

  if (!estaAutenticado) {
    return <Navigate to="/login" replace />;
  }
  return children ? children : <Outlet/>;
}