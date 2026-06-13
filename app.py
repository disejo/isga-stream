import os
import streamlit as st
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables dynamically
load_dotenv(override=True)

# Import local helpers
from auth import get_auth_url, handle_oauth_callback
from google_sheets import append_to_sheet

# Set page configuration
st.set_page_config(
    page_title="Gestión de Leads - Google Sheets Integration",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize Session States
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "user_info" not in st.session_state:
    st.session_state["user_info"] = None

# Process Google OAuth Callback if present in URL
handle_oauth_callback()

# Detect if environment variables are configured
def is_config_incomplete():
    load_dotenv(override=True)
    client_id = os.environ.get("GOOGLE_CLIENT_ID")
    client_secret = os.environ.get("GOOGLE_CLIENT_SECRET")
    sheet_id = os.environ.get("GOOGLE_SHEET_ID")
    
    # Check if they still have the placeholder values
    if not client_id or "TU_GOOGLE_CLIENT_ID" in client_id:
        return True
    if not client_secret or "TU_GOOGLE_CLIENT_SECRET" in client_secret:
        return True
    if not sheet_id or "ID_DE_TU_HOJA" in sheet_id:
        return True
    return False


# CSS Injection for Premium Styling
def inject_custom_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');
    
    /* Base styles */
    .stApp {
        font-family: 'Outfit', sans-serif !important;
        background: radial-gradient(circle at 50% 50%, #1e1b4b 0%, #0f0b29 100%) !important;
        color: #f3f4f6 !important;
    }
    
    /* Center columns styling */
    div[data-testid="column"] {
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    
    /* Glassmorphic Login Card */
    .login-container {
        background: rgba(255, 255, 255, 0.04);
        backdrop-filter: blur(20px) saturate(160%);
        -webkit-backdrop-filter: blur(20px) saturate(160%);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 28px;
        padding: 3rem;
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.4);
        text-align: center;
        max-width: 480px;
        margin: 4rem auto;
        transition: transform 0.4s cubic-bezier(0.165, 0.84, 0.44, 1), box-shadow 0.4s ease;
    }
    
    .login-container:hover {
        transform: translateY(-8px);
        box-shadow: 0 30px 60px rgba(99, 102, 241, 0.15);
        border-color: rgba(99, 102, 241, 0.3);
    }
    
    .login-logo {
        font-size: 3.5rem;
        margin-bottom: 1rem;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    .login-title {
        font-size: 2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #ffffff 40%, #a5b4fc 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    
    .login-subtitle {
        font-size: 0.95rem;
        color: #9ca3af;
        margin-bottom: 2.5rem;
        font-weight: 300;
    }
    
    /* Premium Google Button */
    .google-login-btn {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        background-color: #ffffff;
        color: #1f2937 !important;
        font-weight: 600;
        font-size: 1rem;
        padding: 0.85rem 1.8rem;
        border-radius: 9999px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        text-decoration: none !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
        width: 85%;
        margin: 0 auto;
        cursor: pointer;
    }
    
    .google-login-btn:hover {
        background-color: #f9fafb;
        transform: translateY(-2px) scale(1.02);
        box-shadow: 0 10px 25px rgba(99, 102, 241, 0.3);
    }
    
    .google-login-btn img {
        width: 22px;
        height: 22px;
        margin-right: 12px;
    }
    
    /* Dashboard & Cards styling */
    .dashboard-header {
        background: rgba(15, 11, 41, 0.6);
        backdrop-filter: blur(12px);
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        padding: 1rem 2rem;
        margin-bottom: 2rem;
        border-radius: 16px;
    }
    
    .user-profile-badge {
        display: flex;
        align-items: center;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.08);
        padding: 0.5rem 1rem;
        border-radius: 9999px;
        float: right;
    }
    
    .user-avatar {
        width: 32px;
        height: 32px;
        border-radius: 50%;
        margin-right: 10px;
        border: 1px solid rgba(99, 102, 241, 0.5);
    }
    
    .user-name {
        font-weight: 500;
        font-size: 0.9rem;
        color: #e5e7eb;
    }
    
    .card-panel {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 20px;
        padding: 2.5rem;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
    }
    
    /* Form elements customization */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea, .stSelectbox>div>div>div {
        background-color: rgba(255, 255, 255, 0.04) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        color: #f3f4f6 !important;
        border-radius: 10px !important;
        transition: all 0.3s ease;
    }
    
    .stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus {
        border-color: #6366f1 !important;
        box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.2) !important;
        background-color: rgba(255, 255, 255, 0.06) !important;
    }
    
    /* Config Wizard Styling */
    .wizard-card {
        background: rgba(30, 41, 59, 0.5);
        border: 1px solid rgba(99, 102, 241, 0.2);
        border-radius: 16px;
        padding: 1.5rem;
        margin-top: 1.5rem;
    }
    
    .badge-red {
        background-color: rgba(239, 68, 68, 0.2);
        color: #fca5a5;
        padding: 0.25rem 0.6rem;
        border-radius: 6px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    
    .badge-green {
        background-color: rgba(34, 197, 94, 0.2);
        color: #86efac;
        padding: 0.25rem 0.6rem;
        border-radius: 6px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    </style>
    """, unsafe_allow_html=True)

# Inject base styling
inject_custom_css()

# HIDE default Streamlit header/sidebar on Login screen
def hide_streamlit_chrome():
    st.markdown("""
    <style>
    [data-testid="stHeader"], [data-testid="stSidebar"], footer {
        visibility: hidden;
        height: 0%;
        position: fixed;
    }
    </style>
    """, unsafe_allow_html=True)

# ----------------- VIEW 1: CONFIGURATION WIZARD -----------------
def show_config_wizard():
    st.container()
    col1, col2, col3 = st.columns([1, 4, 1])
    
    with col2:
        st.markdown("<h1 style='text-align: center; margin-top: 2rem;'>🔧 Asistente de Configuración</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #9ca3af;'>Se han detectado variables faltantes o con valores por defecto. Sigue estas instrucciones para completar la integración.</p>", unsafe_allow_html=True)
        
        # Status board
        client_id = os.environ.get("GOOGLE_CLIENT_ID")
        client_secret = os.environ.get("GOOGLE_CLIENT_SECRET")
        sheet_id = os.environ.get("GOOGLE_SHEET_ID")
        sa_json = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON")
        sa_file = os.environ.get("GOOGLE_SERVICE_ACCOUNT_FILE")
        
        status_oauth = "<span class='badge-green'>Configurado</span>" if (client_id and "TU_GOOGLE_CLIENT_ID" not in client_id) else "<span class='badge-red'>Pendiente</span>"
        status_sheets = "<span class='badge-green'>Configurado</span>" if (sheet_id and "ID_DE_TU_HOJA" not in sheet_id) else "<span class='badge-red'>Pendiente</span>"
        status_sa = "<span class='badge-green'>Configurado</span>" if (sa_json or sa_file or os.path.exists("google-credentials.json")) else "<span class='badge-red'>Pendiente</span>"
        
        st.markdown(f"""
        <div class='wizard-card'>
            <h3>Estado de las Integraciones:</h3>
            <p>🔑 Google OAuth2 Login: {status_oauth}</p>
            <p>📝 Google Sheet ID: {status_sheets}</p>
            <p>🤖 Cuenta de Servicio Sheets: {status_sa}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        st.markdown("### 1. Configurar Google Login (OAuth 2.0)")
        st.markdown("""
        1. Dirígete a [Google Cloud Console](https://console.cloud.google.com/).
        2. Crea un proyecto o selecciona uno existente.
        3. Configura la **Pantalla de Consentimiento OAuth** (OAuth Consent Screen) como Externa o Interna y agrega el scope `openid`, `email`, `profile`.
        4. Ve a **Credenciales**, haz clic en **Crear Credenciales** -> **ID de cliente de OAuth**.
        5. Tipo de aplicación: *Web Application*.
        6. Agrega en **Orígenes autorizados de JavaScript**: `http://localhost:8501`.
        7. Agrega en **URI de redireccionamiento autorizados**: `http://localhost:8501`.
        8. Copia el **Client ID** y el **Client Secret** y colócalos en tu archivo `.env`.
        """)
        
        st.markdown("### 2. Configurar Google Sheets y Cuenta de Servicio")
        st.markdown("""
        1. En la misma Google Cloud Console, ve a **API y servicios** -> **Biblioteca** y busca **Google Sheets API**. Haz clic en **Habilitar**.
        2. Ve a **Credenciales** -> **Crear Credenciales** -> **Cuenta de servicio** (Service Account).
        3. Ponle un nombre y finaliza la creación.
        4. Entra a la cuenta de servicio creada, ve a la pestaña **Claves** (Keys) -> **Agregar clave** -> **Crear clave nueva** -> Selecciona **JSON**.
        5. Se descargará un archivo `.json`.
        6. **Muy importante:** Abre ese archivo JSON, copia todo su contenido y pégalo como valor de `GOOGLE_SERVICE_ACCOUNT_JSON` en tu archivo `.env` en una sola línea. Alternativamente, guárdalo como `google-credentials.json` en este directorio.
        7. Copia el email de la cuenta de servicio (ejemplo: `mi-servicio@proyecto.iam.gserviceaccount.com`).
        8. Ve a tu Google Sheet, haz clic en **Compartir** y otorga permisos de **Editor** a ese correo electrónico de la cuenta de servicio.
        9. Copia el ID de tu hoja de cálculo (está en la URL: `https://docs.google.com/spreadsheets/d/ID_DE_HOJA_AQUI/edit`) y ponlo en `GOOGLE_SHEET_ID` en el `.env`.
        """)
        
        st.markdown("### 3. Edita tu archivo `.env` local")
        st.info("El archivo `.env` ya ha sido creado en el directorio raíz. Edítalo con las credenciales que acabas de obtener y reinicia la aplicación Streamlit.")
        
        # Temporary fallback mode for demonstration purposes
        st.markdown("---")
        st.markdown("<p style='text-align: center; color: #9ca3af;'>¿Quieres probar la interfaz sin configurar las APIs de Google?</p>", unsafe_allow_html=True)
        if st.button("🚀 Ingresar en Modo Demostración (Simulado)", use_container_width=True):
            st.session_state["user_info"] = {
                "name": "Usuario Demo",
                "email": "demo@example.com",
                "picture": "https://www.gravatar.com/avatar/00000000000000000000000000000000?d=mp&f=y"
            }
            st.session_state["logged_in"] = True
            st.rerun()

# ----------------- VIEW 2: LOGIN PAGE -----------------
def show_login_page():
    hide_streamlit_chrome()
    
    col1, col2, col3 = st.columns([1.2, 1.8, 1.2])
    
    with col2:
        auth_url = get_auth_url()
        
        st.markdown("""
        <div class="login-container">
            <div class="login-logo">🔒</div>
            <h1 class="login-title">Control de Acceso</h1>
            <p class="login-subtitle">Inicia sesión con tu cuenta corporativa de Google para registrar información en la base de datos de Sheets.</p>
        """, unsafe_allow_html=True)
        
        if auth_url:
            st.markdown(f"""
                <a href="{auth_url}" target="_self" class="google-login-btn">
                    <svg style="margin-right: 12px;" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" width="22px" height="22px">
                        <path fill="#EA4335" d="M24 9.5c3.54 0 6.71 1.22 9.21 3.6l6.85-6.85C35.9 2.38 30.47 0 24 0 14.62 0 6.51 5.38 2.56 13.22l7.98 6.19C12.43 13.72 17.74 9.5 24 9.5z"/>
                        <path fill="#4285F4" d="M46.5 24c0-1.61-.15-3.16-.43-4.69H24v8.88h12.66c-.55 2.92-2.19 5.39-4.66 7.05l7.23 5.6C43.5 36.1 46.5 30.7 46.5 24z"/>
                        <path fill="#FBBC05" d="M10.54 28.59c-.48-1.45-.76-2.99-.76-4.59s.27-3.14.76-4.59l-7.98-6.19C.92 16.46 0 20.12 0 24c0 3.88.92 7.54 2.56 10.78l7.98-6.19z"/>
                        <path fill="#34A853" d="M24 48c6.48 0 11.93-2.13 15.89-5.81l-7.23-5.6c-2.11 1.41-4.8 2.25-8.66 2.25-6.26 0-11.57-4.22-13.46-9.91l-7.98 6.19C6.51 42.62 14.62 48 24 48z"/>
                    </svg>
                    Iniciar Sesión con Google
                </a>
            """, unsafe_allow_html=True)
        else:
            st.error("Error: Configuración de Google OAuth no disponible.")
            st.info("Configura GOOGLE_CLIENT_ID en tu archivo .env.")
            
        st.markdown("""
            <div style="margin-top: 2rem; font-size: 0.8rem; color: #6b7280; font-weight: 300;">
                Conexión cifrada directa mediante Google OAuth 2.0.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Link to Wizard if credentials are incomplete
        if is_config_incomplete():
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🛠️ Ver Instrucciones de Configuración", use_container_width=True):
                st.session_state["show_wizard"] = True
                st.rerun()

# ----------------- VIEW 3: DASHBOARD -----------------
def show_dashboard():
    user = st.session_state["user_info"]
    
    # Custom dashboard top menu bar
    col_title, col_user = st.columns([2, 1])
    
    with col_title:
        st.markdown("<h2 style='margin: 0; font-weight: 700; background: linear-gradient(135deg, #a5b4fc 0%, #818cf8 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>📊 Registro de Leads & Clientes</h2>", unsafe_allow_html=True)
        st.markdown("<p style='color: #9ca3af; font-size: 0.9rem; margin-top: -5px;'>Ingreso de información directa a Google Sheets</p>", unsafe_allow_html=True)
        
    with col_user:
        # Display user profile card
        user_name = user.get("name", "Usuario")
        user_email = user.get("email", "")
        user_pic = user.get("picture", "https://www.gravatar.com/avatar/00000000000000000000000000000000?d=mp&f=y")
        
        st.markdown(f"""
        <div class="user-profile-badge">
            <img class="user-avatar" src="{user_pic}" alt="Profile" />
            <div class="user-name">{user_name}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Logout button below badge
        st.markdown("<div style='clear: both; margin-top: 5px;'></div>", unsafe_allow_html=True)
        col_empty, col_btn = st.columns([1, 1])
        with col_btn:
            if st.button("Cerrar Sesión", key="logout_btn", use_container_width=True):
                st.session_state["logged_in"] = False
                st.session_state["user_info"] = None
                st.query_params.clear()
                st.rerun()

    st.markdown("<hr style='border-color: rgba(255,255,255,0.05); margin-top: 0.5rem;'>", unsafe_allow_html=True)
    
    # Check if we are running in simulated Demo Mode
    is_demo = user_email == "demo@example.com"
    if is_demo:
        st.warning("⚠️ Estás operando en Modo Demostración (Simulado). Los datos que envíes se mostrarán en la interfaz pero no se guardarán en Google Sheets hasta que configures el archivo `.env`.")

    # Form Container
    st.markdown("<div class='card-panel'>", unsafe_allow_html=True)
    st.markdown("<h3 style='margin-top: 0; margin-bottom: 1.5rem; font-weight: 600;'>Formulario de Registro</h3>", unsafe_allow_html=True)
    
    # We use Streamlit form component
    with st.form("insert_lead_form", clear_on_submit=True):
        col_form_1, col_form_2 = st.columns(2)
        
        with col_form_1:
            lead_name = st.text_input("Nombre Completo *", placeholder="Ej. Juan Pérez")
            lead_email = st.text_input("Correo Electrónico *", placeholder="Ej. juan.perez@empresa.com")
            lead_phone = st.text_input("Número de Teléfono", placeholder="Ej. +34 600 000 000")
            
        with col_form_2:
            lead_category = st.selectbox(
                "Categoría / Canal *",
                ["Contacto Comercial", "Soporte Técnico", "Consulta General", "Alianzas", "Otro"]
            )
            lead_source = st.selectbox(
                "Origen del Lead",
                ["Sitio Web", "Campaña de Ads", "Recomendación", "Redes Sociales", "Evento Presencial"]
            )
            lead_notes = st.text_area("Mensaje / Notas Adicionales", placeholder="Escribe detalles adicionales sobre el contacto aquí...", height=70)
            
        st.markdown("<p style='font-size: 0.8rem; color: #9ca3af;'>* Campos obligatorios</p>", unsafe_allow_html=True)
        
        # Center-aligned submit button
        submit_col_1, submit_col_2, submit_col_3 = st.columns([1.5, 1, 1.5])
        with submit_col_2:
            submit_btn = st.form_submit_button("Guardar Datos", use_container_width=True)
            
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Handle Form Submission
    if submit_btn:
        if not lead_name.strip() or not lead_email.strip():
            st.error("Por favor completa los campos obligatorios (*): Nombre y Correo Electrónico.")
        else:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # Structure the data row to append
            # Columns: Timestamp, Nombre, Email, Teléfono, Categoría, Origen, Mensaje, Registrado Por (Usuario Autenticado)
            data_row = [
                timestamp,
                lead_name.strip(),
                lead_email.strip(),
                lead_phone.strip(),
                lead_category,
                lead_source,
                lead_notes.strip(),
                user_email  # Accountability link: Who submitted the data?
            ]
            
            with st.spinner("Guardando registro en la hoja de cálculo..."):
                if is_demo:
                    # Simulated success
                    st.success("🎉 ¡Formulario simulado con éxito!")
                    st.json({
                        "Mensaje": "Modo demostración activo. Datos estructurados para el Sheet:",
                        "Fila a Insertar": data_row
                    })
                else:
                    # Real integration
                    success = append_to_sheet(data_row)
                    if success:
                        st.success("🎉 ¡Datos guardados exitosamente en Google Sheets!")
                        st.balloons()
                    else:
                        st.error("No se pudo completar el registro. Por favor verifica las credenciales de tu Cuenta de Servicio Google y los permisos del Sheet.")

# ----------------- MAIN NAVIGATION ROUTER -----------------
def main():
    # Force reload of env vars
    load_dotenv(override=True)
    
    # If configurations are complete, prevent demo-mode users from staying logged in
    if st.session_state.get("logged_in") and st.session_state.get("user_info", {}).get("email") == "demo@example.com" and not is_config_incomplete():
        st.session_state["logged_in"] = False
        st.session_state["user_info"] = None
        st.query_params.clear()
        st.rerun()

    # If the user requested to see the setup wizard specifically and config is still incomplete
    if st.session_state.get("show_wizard") and is_config_incomplete():
        show_config_wizard()
        if st.button("← Volver a Pantalla de Login", key="back_to_login"):
            st.session_state["show_wizard"] = False
            st.rerun()
    # If configurations are incomplete and we are not logged in, show wizard by default
    elif is_config_incomplete() and not st.session_state["logged_in"]:
        show_config_wizard()
    # If logged in, show the application dashboard
    elif st.session_state["logged_in"]:
        show_dashboard()
    # Otherwise, show the premium login screen
    else:
        show_login_page()


if __name__ == "__main__":
    main()
