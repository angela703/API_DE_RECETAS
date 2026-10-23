CREATE DATABASE IF NOT EXISTS api_recetas
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

-- Reemplace el marcador por la misma contraseña definida en el archivo .env
-- antes de ejecutar este script. No suba una contraseña real a GitHub.
CREATE USER IF NOT EXISTS 'api_recetas_user'@'localhost'
IDENTIFIED BY 'CAMBIAR_POR_LA_MISMA_PASSWORD_DE_ENV';

-- Puede volver a ejecutar este GRANT para actualizar los permisos de la aplicación.
GRANT ALL PRIVILEGES ON api_recetas.*
TO 'api_recetas_user'@'localhost';

FLUSH PRIVILEGES;
