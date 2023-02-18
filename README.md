# email-system

This is a set of scripts to aid in the eHacks planning process.

The send_accept_email.py script will pull the sheet down directly from google sheets based on the SHEET_ID environment variable. The script will then send an acceptance email to every person in the google sheet that's row was colored white. (While making use of this script, make sure you are updating the row colors in the google sheet whenever you accept or deny an applicant).

The tshirts.py script will count the number of t-shirts needed in each size based off of the google sheets numbers

## Instructions to Run

At the moment, this repository consists of two different scripts. I plan to make this the starting point for a Registration API.

To set up for both of the scripts, install the necessary dependencies:

```bash
pip install -r requirements.txt
```

All scripts make use of the Google Sheets API

To use the Google Sheets API, you will have to go into the Google Console and configure your project to use the sheets by following the instructions here: https://developers.google.com/sheets/api/quickstart/python

### Running script.py

For script.py to work, you most add a .env file, or environment variables with these names and values:

```bash
SENDER_EMAIL=<Your Full Email>
PASSWORD=<App Password Generated by Google>
TEST_EMAIL=<Email to be BCC\'ed in all emails>
DISCORD_LINK=<Link to Discord that wil appear in email>
```

App Passwords can be viewed a generated here: https://myaccount.google.com/apppasswords

### Running tshirts.py

For tshirts.py to work, you must add a .env file or environment variables with these names and values:

```bash
SHEET_ID=<The ID of the Google Sheet You Want To Manage>
```

You will need to manually change which column you will want to retrieve data from in the code, if the t-shirt data is located in a different column.
