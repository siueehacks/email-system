import smtplib
import os

from dotenv import load_dotenv

load_dotenv()

with smtplib.SMTP_SSL('smtp.gmail.com', 465) as connection:  
    email_address = os.getenv('USERNAME')
    email_password = os.getenv('PASSWORD')
    connection.login(email_address, email_password )
    connection.sendmail(from_addr=email_address, to_addrs=['michael.x.french@gmail.com', 'mifrenc@siue.edu'], 
    msg="subject:hi \n\n this is my message")