import { useState } from 'react';
import { ContextoAuten } from './ContextoAuten';
import { BASE_URL } from '../config';

export function ProveedorAuten({ children }) {

    const [usuario, setUsuario] = useState(() => {
        const guardado = sessionStorage.getItem('user');
        return guardado ? JSON.parse(guardado) : null;
    });

    const login = async (username, password) => {
        try {
            const response = await fetch(`${BASE_URL}/auth/login`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password })
            });

            if (response.ok) {
                const data = await response.json();
                
                if (data.token) {
                    sessionStorage.setItem('token', data.token);
                    sessionStorage.setItem('user', JSON.stringify(data.usuario));
                    
                    setUsuario(data.usuario);
                    return true;
                }
            }
            return false;
        } catch (error) {
            console.error("Error en petición de login:", error);
            return false;
        }
    };

    const logout = () => {
        console.log('Logout called');
        sessionStorage.removeItem('user');
        sessionStorage.removeItem('token');
        setUsuario(null);
    };

    return (
        <ContextoAuten value={{ usuario, estaAutenticado: !!usuario, login, logout }}>
        {children}
        </ContextoAuten>
    );
}
