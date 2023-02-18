import smtplib
import os
import sys
import json
from enum import Enum

import pandas as pd
from dotenv import load_dotenv
from googleapiclient.discovery import build

from helpers.utils import get_creds

load_dotenv()

def get_sheet_info() -> list[tuple[str, str, dict]]:
    """Get the information from the google sheet

    Returns:
        list[tuple[str, str]]: list of tuples containing the email and name
    """
    creds = get_creds()
    sheet_id = os.getenv("SHEET_ID")
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()

    # This call gets the data from the sheet
    result = (
        sheet.values()
        .get(spreadsheetId=sheet_id, range="Form Responses 1")
        .execute()
    )
    values = result.get("values")
    values = values[1:]

    # This gets the styling of all of the rows within the sheet
    grid_data = sheet.get(spreadsheetId=sheet_id, includeGridData=True).execute()
    grid_data = grid_data['sheets'][0]['data'][0]['rowData'][1:]

    if not values:
        print("No data found.")
        return

    # Parse the sheet data into a list of tuples
    return_info = []
    for i, row_data in enumerate(values):
        row_style = grid_data[i]
        color = row_style['values'][0]['effectiveFormat']['backgroundColor']
        email = row_data[3]
        name = row_data[1]
        return_info.append((email, name, color))

    return return_info
    

def generate_email_body(name: str):
    discord_link = os.getenv("DISCORD_LINK")
    email = f"""
Hello {name}!

Thank you for registering for {{ehacks}} 2023. You're registration is confirmed. We are excited to have you join us for the event! We will be sending you more information about the event prior to the start date.

Please join our discord to meet your fellow hackers and stay up to date. It will be our main form of communication and we will be releasing any important announcements regarding the event through Discord: {discord_link}

Best Regards,
eHacks Team
"""
    return email

def send_email(to: str, name: str = 'Hacker') -> None:
    """
    Send an email to a single recipient

    Args:
        to (str): email address of recipient
        name (str, optional): name of recipient. Defaults to 'Hacker'.
    """
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as connection:
        email_address = os.getenv("SENDER_EMAIL")
        email_password = os.getenv("PASSWORD")
        test_email = os.getenv("TEST_EMAIL")
        connection.login(email_address, email_password)
        connection.sendmail(
            from_addr=email_address,
            to_addrs=[to, test_email],   # Add myself as a BCC for testing purposes
            msg=f"From: {email_address}\r\nTo: {to}\r\nsubject:eHacks 2023 Confirmation \n\n {generate_email_body(name)}",
        )

def send_acceptance_emails() -> None:
    """Send the acceptance emails to all of the hackers
    """
    sheet_info = get_sheet_info()
    for email, name, color in sheet_info:

        # If the color is white, send an email to the person
        if color['red'] == 1 and color['green'] == 1 and color['blue'] == 1:
            send_email(email, name)


def main():
    send_acceptance_emails()

if __name__ == "__main__":
    main()