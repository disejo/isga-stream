import os
import re
import json
from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build
import streamlit as st

# Load environment variables on module import
load_dotenv(override=True)

def get_sheets_service():
    """
    Initializes and returns the Google Sheets API client using a service account.
    """
    # Force reload of env vars in case they changed during runtime
    load_dotenv(override=True)
    
    sa_json = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON")
    sa_file = os.environ.get("GOOGLE_SERVICE_ACCOUNT_FILE")
    
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = None
    
    # Check options sequentially for ease of setup
    if sa_json and sa_json.strip():
        try:
            info = json.loads(sa_json)
            creds = service_account.Credentials.from_service_account_info(info, scopes=scopes)
        except Exception as e:
            st.error(f"Error cargando credenciales de GOOGLE_SERVICE_ACCOUNT_JSON: {e}")
            return None
    elif sa_file and os.path.exists(sa_file):
        try:
            creds = service_account.Credentials.from_service_account_file(sa_file, scopes=scopes)
        except Exception as e:
            st.error(f"Error cargando credenciales desde el archivo {sa_file}: {e}")
            return None
    elif os.path.exists("google-credentials.json"):
        try:
            creds = service_account.Credentials.from_service_account_file("google-credentials.json", scopes=scopes)
        except Exception as e:
            st.error(f"Error cargando credenciales desde google-credentials.json: {e}")
            return None
    else:
        st.warning("Credenciales de cuenta de servicio no configuradas. Configure GOOGLE_SERVICE_ACCOUNT_JSON o GOOGLE_SERVICE_ACCOUNT_FILE en su .env.")
        return None
        
    try:
        service = build("sheets", "v4", credentials=creds, cache_discovery=False)
        return service
    except Exception as e:
        st.error(f"Error al inicializar el servicio de Google Sheets API: {e}")
        return None

def append_to_sheet(data_row, sheet_id=None, range_name=None):
    """
    Appends a new row of data to the Google Sheet.
    data_row should be a list of values: [timestamp, name, email, phone, message, user_login_email]
    """
    # Force reload of env vars in case they changed during runtime
    load_dotenv(override=True)
    
    if not sheet_id:
        sheet_id = os.environ.get("GOOGLE_SHEET_ID")
    if not range_name:
        range_name = os.environ.get("GOOGLE_SHEET_RANGE", "Sheet1!A:Z")
        
    if not sheet_id or "TU_HOJA" in sheet_id or not sheet_id.strip():
        st.error("ID de Google Sheet no configurado o inválido (GOOGLE_SHEET_ID).")
        return False
        
    # Extract spreadsheet ID from URL if full URL was provided
    if "/" in sheet_id or "docs.google.com" in sheet_id:
        match = re.search(r"/d/([a-zA-Z0-9-_]+)", sheet_id)
        if match:
            sheet_id = match.group(1)
            
    service = get_sheets_service()
    if not service:
        return False
        
    try:
        body = {
            "values": [data_row]
        }
        result = service.spreadsheets().values().append(
            spreadsheetId=sheet_id,
            range=range_name,
            valueInputOption="USER_ENTERED",
            insertDataOption="INSERT_ROWS",
            body=body
        ).execute()
        return True
    except Exception as e:
        st.error(f"Error al escribir datos en Google Sheets: {e}")
        return False

