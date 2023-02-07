import smtplib
import os

from dotenv import load_dotenv

load_dotenv()


def generate_email_body(name: str):
    email = f"""
Hello {name}!

Thank you for registering for ehacks 2023. You're registration is confirmed.

Please join our discord: https://discord.gg/V9NaW4e5yv

Best Regards,
eHacks Team
"""
    return email

def send_email():
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as connection:
        email_address = os.getenv("USERNAME")
        email_password = os.getenv("PASSWORD")
        connection.login(email_address, email_password)
        connection.sendmail(
            from_addr=email_address,
            to_addrs=["michael.x.french@gmail.com", "mifrenc@siue.edu"],
            msg=f"subject:eHacks 2023 Confirmation \n\n {generate_email_body('Michael')}",
        )
