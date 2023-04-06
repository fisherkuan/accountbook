import gspread
import pandas as pd

from .credentials import get_creds


class GoogleSheetsHandler:
    def __init__(self, auth_from_service_account_file=False) -> None:
        self.creds = get_creds(auth_from_service_account_file)
        self.client = gspread.authorize(self.creds)
        
    