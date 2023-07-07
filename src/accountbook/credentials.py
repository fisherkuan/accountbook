from google.auth.transport.requests import Request
from google.oauth2 import service_account
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.exceptions import RefreshError
from config import SECRETS


def get_creds(from_service_account_file=False) -> Credentials:
    SCOPES = [
        "https://www.googleapis.com/auth/cloud-platform",
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]
    KEY_PATH = SECRETS / "service-account-key.json"
    TOKEN_PATH = SECRETS / "user-token.json"

    if from_service_account_file:
        creds = service_account.Credentials.from_service_account_file(KEY_PATH, scopes=SCOPES)
        return creds

    creds = None
    if TOKEN_PATH.exists():
        print("Token exists, loading...")
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                print("Refreshing token...")
                creds.refresh(Request())
            except RefreshError:
                print("Token expired, deleting...")
                TOKEN_PATH.unlink()
                get_creds()
        else:
            print("No token, creating...")
            flow = InstalledAppFlow.from_client_secrets_file(SECRETS / "credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_PATH, "w") as token:
            print("Saving token...")
            token.write(creds.to_json())
    return creds


if __name__ == "__main__":
    get_creds()
