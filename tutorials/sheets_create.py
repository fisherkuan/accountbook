from __future__ import print_function

from googleapiclient.errors import HttpError
from __init__ import sheets_service


def create(title):
    # pylint: disable=maybe-no-member
    try:
        service = sheets_service()
        spreadsheet = {
            'properties': {
                'title': title
            }
        }
        spreadsheet = service.spreadsheets().create(body=spreadsheet,
                                                    fields='spreadsheetId') \
            .execute()
        print(f"Spreadsheet ID: {(spreadsheet.get('spreadsheetId'))}")
        return spreadsheet.get('spreadsheetId')
    except HttpError as error:
        print(f"An error occurred: {error}")
        return error


if __name__ == '__main__':
    # Pass: title
    create("mysheet1")