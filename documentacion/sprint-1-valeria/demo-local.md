# Demostración local del registro

Última actualización: [validación solo de diez dígitos y corrección del esquema de la base original](decision-cedula-diez-digitos.md). La aplicación habitual de localhost:5173 ya puede registrar cuentas generales; la demo de 5174 continúa separada, con sus cuentas de prueba. Las notas anteriores sobre ausencia de esquema en la base original corresponden al diagnóstico previo a esa corrección.

Actualización funcional del 9 de noviembre: la demo admite [usuarios generales](decision-registro-general.md) para cédulas válidas que no aparezcan en el padrón. Se probó el alta real de `usuario.demo`, login, perfil y denegación de áreas de socio, administrador y Marketing. Se añadió `/mi-cuenta` para su acceso básico. Los usuarios anteriores de la demo se conservan.

El 9 de noviembre de 2026 se diagnosticó que la base configurada originalmente no tenía `padron_prueba` ni los dos índices normalizados. El backend estaba activo, pero el registro nuevo requiere ese esquema. No era un segundo fallo del verificador.

Se preparó una base separada `sprint1_valeria_demo_1c8c1dff`, con SQL 01–05, migraciones de auth/contenttypes y el comando de carga sintética. No se aplicó el esquema ni se cargaron datos en cooperativa_db. No se modificaron archivos .env.

Instancia de demostración iniciada:

- Frontend: http://localhost:5174
- Backend: http://127.0.0.1:8001
- Cédulas activas disponibles al entregar: `0100000009` y `0100000017`.
- Cédula inactiva: `0100000025`.

Se comprobó un registro HTTP mediante APIClient con respuesta 201 dentro de una transacción revertida, para conservar disponible la primera cédula. Además, el frontend respondió 200 y el backend devolvió el origen CORS correcto para localhost:5174. La comprobación no creó una cuenta persistente.

La página anterior del puerto 5173 conserva su configuración anterior. Utilizar el enlace 5174 para esta demostración. Una vez completado un registro real en la demo, esa cédula ya no podrá crear otra cuenta; iniciar sesión con el usuario y la contraseña elegidos.

## Reiniciar la demo si se detienen los servidores

Desde la raíz del repositorio, en una terminal:

```powershell
cd backend
$env:DB_NAME = 'sprint1_valeria_demo_1c8c1dff'
$env:CORS_ALLOWED_ORIGINS = 'http://localhost:5174,http://127.0.0.1:5174'
& .\venv\Scripts\python.exe manage.py runserver 127.0.0.1:8001 --noreload
```

En otra terminal, desde la raíz:

```powershell
cd frontend
$env:VITE_API_URL = 'http://127.0.0.1:8001/api'
npm.cmd run dev -- --host localhost --port 5174 --strictPort
```

Estos valores solo afectan a sus terminales. No volver a ejecutar los scripts de creación sobre esta base ya preparada. La demo es local y sus servidores deben permanecer en ejecución para utilizarla.
