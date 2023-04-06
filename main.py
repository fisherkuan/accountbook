from __future__ import print_function

from pathlib import Path

import gspread
import pandas as pd
import pandas_gbq as pdgbq
from google.auth.transport.requests import Request
from google.oauth2 import service_account
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow


def get_creds(from_service_account_file=False) -> Credentials:
    SCOPES = [
        "https://www.googleapis.com/auth/cloud-platform",
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]
    KEY_PATH = Path("credentials/service-account-key.json")
    TOKEN_PATH = Path("credentials/user-token.json")

    if from_service_account_file:
        creds = service_account.Credentials.from_service_account_file(
            KEY_PATH, scopes=SCOPES
        )
        return creds
    
    creds = None
    if TOKEN_PATH.exists():
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials/credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_PATH, "w") as token:
            token.write(creds.to_json())
    return creds


def sheets_agent(auth_from_service_account_file=False):
    return gspread.authorize(get_creds(auth_from_service_account_file))


def query_bigquery(
    query, project_id="kuan-wu-accounting", auth_from_service_account_file=False
) -> pd.DataFrame:
    pdgbq.context.credentials = get_creds(auth_from_service_account_file)
    return pd.read_gbq(query, project_id)


if __name__ == "__main__":
    sheet1_a1 = sheets_agent(auth_from_service_account_file=True).open("mysheet1").sheet1
    query = "SELECT * FROM `kuan-wu-accounting.data.fisher-kbc` LIMIT 1000"

    print(sheet1_a1.get("A1:B8"))
    # sheet1_a1.update('A1', [[1, 2], [3, 4]])
    # sheet1_a1.update('B25', "it's down there somewhere, let me take another look.")
    print(query_bigquery(query=query, auth_from_service_account_file=True))
