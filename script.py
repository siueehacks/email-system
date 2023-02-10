import smtplib
import os

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

    # Included my email so I can see the email sent
    df = pd.concat([df, pd.DataFrame({'First Name': ['Michael'], 'Last Name': ['French'], 'Email': ['mifrenc@siue.edu']})])
    return df

def generate_email_body(name: str):
    email = f"""
Hello {name}!

Thank you for registering for {{ehacks}} 2023. You're registration is confirmed. We are excited to have you join us for the event! We will be sending you more information about the event prior to the start date.

Please join our discord to meet your fellow hackers and stay up to date: https://discord.gg/V9NaW4e5yv

Best Regards,
eHacks Team
"""
    return email

def send_email(to: str, name: str = 'Hacker'):
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as connection:
        email_address = os.getenv("USERNAME")
        email_password = os.getenv("PASSWORD")
        connection.login(email_address, email_password)
        connection.sendmail(
            from_addr=email_address,
            to_addrs=[to],
            msg=f"subject:eHacks 2023 Confirmation \n\n {generate_email_body(name)}",
        )

def main():
    df = parse_csv("test.csv")
    for _, row in df.iterrows():
        send_email(row['Email'], row['First Name'])

if __name__ == "__main__":
    main()