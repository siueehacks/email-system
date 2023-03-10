import smtplib
import os
from email.mime.text import MIMEText

from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader

from helpers.sheets import get_sheet_info, parse_for_data_and_style

load_dotenv()


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
    message = MIMEText(generate_email_body(name), "html")
    message["From"] = f'eHacks 2023 Team <{os.getenv("SENDER_EMAIL")}>'
    message["To"] = to
    message["Subject"] = "eHacks 2023 Confirmation"

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
    sheet_info = get_sheet_info("Form Responses 1", return_style=True)
    sheet_info = parse_for_data_and_style(sheet_info[0], sheet_info[1])
    for email, name, color in sheet_info:
        # If the color is white, send an email to the person
        if color["red"] == 1 and color["green"] == 1 and color["blue"] == 1:
            send_email(email, name)


def main():
    send_acceptance_emails()


if __name__ == "__main__":
    main()
