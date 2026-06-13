import os
import urllib.parse
import requests
import secrets
import streamlit as st
from dotenv import load_dotenv
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired

# Load env variables
load_dotenv(override=True)

# ─────────────────────────────────────────────────────────
# CSRF state token helpers (itsdangerous, stateless)
# ─────────────────────────────────────────────────────────

def _get_serializer():
    """Returns a URLSafeTimedSerializer using GOOGLE_CLIENT_SECRET as key."""
    load_dotenv(override=True)
    secret = os.environ.get("GOOGLE_CLIENT_SECRET", "")
    if not secret:
        raise ValueError("GOOGLE_CLIENT_SECRET no está configurado en el .env.")
    return URLSafeTimedSerializer(secret, salt="oauth-state")


def generate_signed_state():
    """
    Generates a cryptographically signed, time-stamped state token.
    Uses itsdangerous so the signature is verified server-side without
    needing st.session_state (which resets on redirect).
    """
    nonce = secrets.token_hex(16)
    return _get_serializer().dumps(nonce)


def verify_signed_state(state_str, max_age_seconds=600):
    """
    Verifies the signed state token returned by Google.
    Returns True if valid, False otherwise.
    """
    try:
        _get_serializer().loads(state_str, max_age=max_age_seconds)
        return True
    except SignatureExpired:
        st.error("⚠️ Sesión de inicio expirada (>10 min). Por favor, vuelve a hacer clic en 'Iniciar Sesión con Google'.")
        return False
    except BadSignature:
        st.error("⚠️ Token de estado inválido. Por favor, vuelve a hacer clic en 'Iniciar Sesión con Google'.")
        return False
    except Exception as e:
        st.error(f"⚠️ Error al verificar el estado OAuth: {e}")
        return False


# ─────────────────────────────────────────────────────────
# OAuth2 Flow
# ─────────────────────────────────────────────────────────

def get_auth_url():
    """
    Generates the Google OAuth2 authorization URL with a signed state token.
    """
    load_dotenv(override=True)
    client_id = os.environ.get("GOOGLE_CLIENT_ID")
    redirect_uri = os.environ.get("GOOGLE_REDIRECT_URI", "http://localhost:8501")

    if not client_id:
        return None

    state = generate_signed_state()

    params = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": "openid email profile",
        "state": state,
        "access_type": "online",
        "prompt": "select_account",
    }

    return "https://accounts.google.com/o/oauth2/v2/auth?" + urllib.parse.urlencode(params)


def handle_oauth_callback():
    """
    Detects and processes the OAuth2 redirect from Google.
    Exchanges the authorization code for user info and stores it in session_state.
    """
    load_dotenv(override=True)
    params = st.query_params

    if "code" not in params:
        return False

    code = params["code"]
    returned_state = params.get("state", "")

    # ── Security check ────────────────────────────────────
    if not verify_signed_state(returned_state):
        # Error message already shown inside verify_signed_state
        st.query_params.clear()
        return False

    # ── Token exchange ────────────────────────────────────
    client_id = os.environ.get("GOOGLE_CLIENT_ID")
    client_secret = os.environ.get("GOOGLE_CLIENT_SECRET")
    redirect_uri = os.environ.get("GOOGLE_REDIRECT_URI", "http://localhost:8501")

    if not client_id or not client_secret:
        st.error("Error de configuración: Faltan GOOGLE_CLIENT_ID o GOOGLE_CLIENT_SECRET en el .env.")
        st.query_params.clear()
        return False

    token_url = "https://oauth2.googleapis.com/token"
    token_data = {
        "code": code,
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code",
    }

    try:
        token_res = requests.post(token_url, data=token_data, timeout=10)
        if token_res.status_code != 200:
            st.error(f"Error al intercambiar código con Google: {token_res.text}")
            st.query_params.clear()
            return False

        access_token = token_res.json().get("access_token")

        # ── Fetch user profile ────────────────────────────
        userinfo_res = requests.get(
            "https://www.googleapis.com/oauth2/v3/userinfo",
            headers={"Authorization": f"Bearer {access_token}"},
            timeout=10,
        )

        if userinfo_res.status_code != 200:
            st.error("Error al recuperar el perfil del usuario desde Google.")
            st.query_params.clear()
            return False

        user_info = userinfo_res.json()
        st.session_state["user_info"] = user_info
        st.session_state["logged_in"] = True
        st.query_params.clear()
        st.rerun()
        return True

    except requests.exceptions.Timeout:
        st.error("Tiempo de espera agotado al conectar con Google. Intenta de nuevo.")
    except Exception as e:
        st.error(f"Error inesperado en la autenticación: {e}")

    st.query_params.clear()
    return False
