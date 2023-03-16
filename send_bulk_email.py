import sys
import os
import smtplib
from typing import List
from email.mime.text import MIMEText


from jinja2 import Environment, FileSystemLoader

from helpers.sheets import get_sheet_info, parse_for_data_and_style

from dotenv import load_dotenv

load_dotenv()

def generate_email_body():
    """Generate the body of the email using a Jinja template"""
    discord_link = os.getenv("DISCORD_LINK")

    environment = Environment(loader=FileSystemLoader("templates/"))
    template = environment.get_template(sys.argv[1])
    body = template.render(discord_link=discord_link)
    return body


def send_emails(to: List[str]) -> None:
    """
    Send an emails to multiple recipients

    Args:
        to (str): email address of recipient
        name (str, optional): name of recipient. Defaults to 'Hacker'.
    """
    # Make sure the email is RFC conformant
    message = MIMEText(generate_email_body(), "html")
    message["From"] = f'eHacks 2023 Team <{os.getenv("SENDER_EMAIL")}>'
    message["To"] = "eHacks 2023 Hackers"
    message["Subject"] = "eHacks 2023 Exit Survey"

    msg_full = message.as_string()

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as connection:
        email_address = os.getenv("SENDER_EMAIL")
        email_password = os.getenv("PASSWORD")
        test_email = os.getenv("TEST_EMAIL")
        connection.login(email_address, email_password)
        connection.sendmail(
            from_addr=email_address,
            to_addrs=[*to, test_email],  # Add myself as a BCC for testing purposes
            msg=msg_full,
        )

    print("Emails sent successfully!")


def send_bulk_email():
    """Send the acceptance emails to all of the hackers"""
    sheet_info = get_sheet_info("Form Responses 1", return_style=True)
    sheet_info = parse_for_data_and_style(sheet_info[0], sheet_info[1])

    emails = []
    for email, _, color in sheet_info:
        # Value is hardcoded for now, but should improve this in the future
        emails.append(email)
    send_emails(emails)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python send_bulk_email.py <template file>")
        sys.exit(1)

    send_bulk_email()
