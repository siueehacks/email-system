import smtplib
import os
import sys

import pandas as pd
from dotenv import load_dotenv

load_dotenv()

def parse_csv(filename: str):
    """Parse an input csv for the needed fields

    Args:
        filename (str): name of input csv

    Returns:
        Dataframe: dataframe with only the needed fields
    """
    df = pd.read_csv(filename)
    df = df[['First Name', 'Last Name', 'Email (use university provided email)']]
    df['Email'] = df['Email (use university provided email)']
    return df

def get_sheet_info() -> list[tuple[str, str]]:
    """Get the information from the google sheet

    Returns:
        list[tuple[str, str]]: list of tuples containing the email and name
    """
    

    return None
    

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

def send_email(to: str, name: str = 'Hacker'):
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

def main():
    if len(sys.argv) != 2:
        print("Usage: script.py <csv file>")
        sys.exit(1)

    df = parse_csv(sys.argv[1])
    for _, row in df.iterrows():
        send_email(row['Email'], row['First Name'])

if __name__ == "__main__":
    main()