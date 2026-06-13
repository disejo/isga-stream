# Aplicación de Registro de Leads con Streamlit, Google OAuth y Google Sheets

Esta es una aplicación interactiva desarrollada en **Streamlit** que permite a los usuarios iniciar sesión de manera segura utilizando su cuenta de Google (OAuth 2.0) y registrar datos en una hoja de cálculo centralizada de **Google Sheets** a través de un formulario web dinámico y con diseño premium.

## Características principales
- 🔒 **Autenticación con Google**: Inicio de sesión seguro vía OAuth 2.0 con validación de estado (anti-CSRF) para proteger las sesiones de usuario.
- 📊 **Conectividad con Google Sheets**: Envío automatizado de datos de formularios (nombre, correo, teléfono, categoría, mensaje) utilizando una Cuenta de Servicio segura de Google.
- ⚡ **Auditoría e Identidad**: Registra automáticamente la fecha/hora exacta y el correo electrónico del usuario autenticado que insertó cada fila, para total trazabilidad.
- 🎨 **Diseño Moderno & Premium**: Interfaz oscura estilizada, con efectos de cristal (glassmorphism), tipografía premium (Outfit de Google Fonts) y micro-animaciones.
- 🛠️ **Asistente de Configuración Integrado**: Si faltan variables en el archivo `.env`, la aplicación muestra un asistente visual guiado paso a paso para ayudarte a configurar las credenciales en Google Cloud Console.

---

## Estructura del Proyecto

```text
├── .venv/                   # Entorno virtual de Python
├── .env                     # Variables de entorno con credenciales secretas (ignorado por git)
├── example.env              # Plantilla de variables de entorno de ejemplo
├── app.py                   # Archivo principal de la aplicación Streamlit
├── auth.py                  # Módulo de integración de Google OAuth2
├── google_sheets.py         # Módulo de integración de Google Sheets API
├── pyproject.toml           # Configuración de empaquetado y dependencias
└── README.md                # Documentación del proyecto
```

---

## Requisitos Previos

Asegúrate de tener instalado Python 3.12 o superior en tu sistema.

### 1. Clonar e inicializar el entorno virtual
El entorno virtual ya ha sido creado en este directorio. Para activarlo:

**En Linux/macOS:**
```bash
source .venv/bin/activate
```

**En Windows:**
```cmd
.venv\Scripts\activate
```

Las dependencias necesarias ya se encuentran instaladas en tu entorno virtual local. Si deseas reinstalarlas, ejecuta:
```bash
pip install -r requirements.txt
# O usa pyproject.toml:
pip install .
```

---

## Configuración de Integraciones (Google Cloud Console)

Crea un archivo `.env` en la raíz del proyecto (la aplicación ya crea uno por defecto con plantillas). Completa las siguientes variables:

### A. Google OAuth 2.0 (Inicio de sesión)
1. Entra a [Google Cloud Console](https://console.cloud.google.com/).
2. Configura tu **Pantalla de Consentimiento OAuth** (OAuth Consent Screen). Agrega el alcance `openid`, `email` y `profile`.
3. Ve a **Credenciales** -> **Crear credenciales** -> **ID de cliente de OAuth**.
4. Selecciona tipo **Web Application**.
5. En **Orígenes de JavaScript autorizados**, añade: `http://localhost:8501`.
6. En **URI de redireccionamiento autorizados**, añade: `http://localhost:8501`.
7. Copia el `Client ID` y `Client Secret` en tu `.env`.

### B. Google Sheets API (Escritura en Base de Datos)
1. Habilita la **Google Sheets API** en tu proyecto de Google Cloud.
2. Ve a **Credenciales** -> **Crear credenciales** -> **Cuenta de servicio** (Service Account).
3. Entra a la cuenta creada, ve a la pestaña **Claves** (Keys) -> **Agregar clave** -> **Crear clave nueva** -> Selecciona **JSON**.
4. Descarga el archivo JSON. Tienes dos formas de usarlo:
   - **Opción A (Recomendada):** Abre el JSON descargado, copia todo su contenido en una sola línea y asígnalo a `GOOGLE_SERVICE_ACCOUNT_JSON` en tu archivo `.env`.
   - **Opción B:** Guarda el archivo JSON en este directorio como `google-credentials.json` (está configurado para ser detectado automáticamente).
5. Crea una nueva hoja de cálculo en Google Sheets.
6. Copia su ID de la URL (`https://docs.google.com/spreadsheets/d/ID_DE_HOJA/edit`) y asígnalo a `GOOGLE_SHEET_ID` en el `.env`.
7. **Crucial:** Comparte la hoja de cálculo dándole permisos de **Editor** al email de tu Cuenta de Servicio Google (ej. `mi-cuenta-servicio@proyecto.iam.gserviceaccount.com`).

---

## Cómo Ejecutar en Local

Para iniciar tu servidor de desarrollo Streamlit:

```bash
.venv/bin/streamlit run app.py
```

La aplicación se abrirá automáticamente en tu navegador web en `http://localhost:8501`.

*Nota: Si es la primera vez que la ejecutas y no has configurado tu `.env`, la aplicación te guiará con el **Asistente de Configuración** y te dará la opción de ingresar en **Modo Demostración** para ver la interfaz interactiva simulada.*
