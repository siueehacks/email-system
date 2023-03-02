from typing import Any, List, Tuple
import os

from googleapiclient.discovery import build
from dotenv import load_dotenv

from helpers.utils import get_creds

load_dotenv()

def get_sheet_info(range: str, return_style: bool = False) -> Any:
    """Get the information from the google sheet
    NOTE: The header row is removed from the data

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

        return values[1:], grid_data[1:]

    return values[1:]

def parse_for_data_and_style(values: List[List[str]], grid_data: List[dict]) -> List[Tuple[str, str, dict]]:
    """Parse the data and style from the sheet into a list of tuples

    Args:
        values (list[list[str]]): The data from the sheet
        grid_data (list[dict]): The styling of the sheet

    Returns:
        list[tuple[str, str, dict]]: The parsed data
    """
    if not values:
        print("No data found.")
        return

    # Parse the sheet data into a list of tuples
    return_info = []
    for i, row_data in enumerate(values):
        row_style = grid_data[i]
        color = row_style["values"][0]["effectiveFormat"]["backgroundColor"]
        email = row_data[3]
        name = row_data[1]
        return_info.append((email, name, color))

    return return_info