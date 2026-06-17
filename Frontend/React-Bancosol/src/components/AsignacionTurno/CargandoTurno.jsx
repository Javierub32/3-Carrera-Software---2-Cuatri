export default function CargandoTurno() {
    return (
        <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '60vh', flexDirection: 'column', gap: '10px' }}>
            <i
                className="ri-loader-4-line"
                style={{ fontSize: '3rem', color: 'var(--primary-blue)', animation: 'spin 1s linear infinite' }}
            ></i>
            <p style={{ color: 'var(--text-muted)', fontSize: '1.2rem', fontWeight: 500 }}>
                Cargando datos del turno...
            </p>
            <style>
                {`
                    @keyframes spin {
                        0% { transform: rotate(0deg); }
                        100% { transform: rotate(360deg); }
                    }
                `}
            </style>
        </div>
    );
}
