from typing import Any
import os

from googleapiclient.discovery import build
from dotenv import load_dotenv

from helpers.utils import get_creds

load_dotenv()

def get_sheet_info(range: str, return_style: bool = False) -> Any:
    """Get the information from the google sheet

    Args:
        range (str): The range of the sheet to get data from
        return_style (bool, optional): Whether to return the styling of the sheet. Defaults to False.

    Returns:
        Any: The data from the sheet
    """
    creds = get_creds()
    sheet_id = os.getenv("SHEET_ID")
    service = build("sheets", "v4", credentials=creds)
    sheet = service.spreadsheets()

    # This call gets the data from the sheet
    result = (
        sheet.values().get(spreadsheetId=sheet_id, range=range).execute()
    )
    values = result.get("values")

    if return_style:
        # This gets the styling of all of the rows within the sheet
        grid_data = sheet.get(spreadsheetId=sheet_id, includeGridData=True).execute()
        grid_data = grid_data["sheets"][0]["data"][0]["rowData"]

        return values, grid_data

    return values