import smtplib
import os
from email.mime.text import MIMEText

from dotenv import load_dotenv
from googleapiclient.discovery import build
from jinja2 import Environment, FileSystemLoader

from helpers.utils import get_creds

load_dotenv()


def get_sheet_info() -> list[tuple[str, str, dict]]:
    """Get the information from the google sheet

    Returns:
        list[tuple[str, str]]: list of tuples containing the email and name
    """
    creds = get_creds()
    sheet_id = os.getenv("SHEET_ID")
    service = build("sheets", "v4", credentials=creds)
    sheet = service.spreadsheets()

    # This call gets the data from the sheet
    result = (
        sheet.values().get(spreadsheetId=sheet_id, range="Form Responses 1").execute()
    )
    values = result.get("values")
    values = values[1:]

    # This gets the styling of all of the rows within the sheet
    grid_data = sheet.get(spreadsheetId=sheet_id, includeGridData=True).execute()
    grid_data = grid_data["sheets"][0]["data"][0]["rowData"][1:]

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


def generate_email_body(name: str):
    """Generate the body of the email using a Jinja template"""
    discord_link = os.getenv("DISCORD_LINK")

    environment = Environment(loader=FileSystemLoader("templates/"))
    template = environment.get_template("acceptance.html")
    body = template.render(name=name, discord_link=discord_link)
    return body


def send_email(to: str, name: str = "Hacker") -> None:
    """
    Send an email to a single recipient

    Args:
        to (str): email address of recipient
        name (str, optional): name of recipient. Defaults to 'Hacker'.
    """
    # Make sure the email is RFC conformant
    message = MIMEText(generate_email_body(name), 'html')
    message['From'] = f'eHacks 2023 Team <{os.getenv("SENDER_EMAIL")}>'
    message['To'] = to
    message['Subject'] = "eHacks 2023 Confirmation"

    msg_full = message.as_string()

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as connection:
        email_address = os.getenv("SENDER_EMAIL")
        email_password = os.getenv("PASSWORD")
        test_email = os.getenv("TEST_EMAIL")
        connection.login(email_address, email_password)
        connection.sendmail(
            from_addr=email_address,
            to_addrs=[to, test_email],  # Add myself as a BCC for testing purposes
            msg=msg_full,
        )


def send_acceptance_emails() -> None:
    """Send the acceptance emails to all of the hackers"""
    sheet_info = get_sheet_info()
    for email, name, color in sheet_info:
        # If the color is white, send an email to the person
        if color["red"] == 1 and color["green"] == 1 and color["blue"] == 1:
            send_email(email, name)


def main():
    send_acceptance_emails()


if __name__ == "__main__":
    main()