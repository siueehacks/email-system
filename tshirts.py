"""Will want to break this out into another repo"""

from __future__ import print_function

import os.path
import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv

from helpers.utils import get_creds

load_dotenv()

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = os.getenv("SHEET_ID")
SAMPLE_RANGE_NAME = "Form Responses 1!L:L"


def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = get_creds()

    try:
        service = build("sheets", "v4", credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = (
            sheet.values()
            .get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME)
            .execute()
        )
        values = result.get("values", [])

        if not values:
            print("No data found.")
            return

        shirt_dict = {}
        for row in values[1:]:
            if row[0] in shirt_dict:
                shirt_dict[row[0]] += 1
            else:
                shirt_dict[row[0]] = 1
        
        print(shirt_dict)

    except HttpError as err:
        print(err)


if __name__ == "__main__":
    main()
