import os
import datetime

from googleapiclient.discovery import build
from dotenv import load_dotenv
import pandas as pd

from helpers.utils import get_creds

load_dotenv()

creds = get_creds()
sheet_id = os.getenv("SHEET_ID")
service = build("sheets", "v4", credentials=creds)
sheet = service.spreadsheets()

result = sheet.values().get(spreadsheetId=sheet_id, range="Form Responses 1").execute()

data = result["values"][1:]
headers = result["values"][0]

df = pd.DataFrame(data, columns=headers)

# Add a priority column. If the participant registered befre 11:59 PM on 2/15/2023, they get priority
df["Priority?"] = df["Timestamp"].apply(
    lambda x: "Yes" if datetime.datetime.strptime(x, "%m/%d/%Y %H:%M:%S") < datetime.datetime(2023, 2, 15, 23, 59, 59) else "No"
)

# Make a full name column
df["Full Name"] = df["First Name"] + " " + df["Last Name"]

# Consolidate the school columns into one
df["School"] = df["What school do you currently attend? If you're no longer a student, what school / university did you most recently graduate from?"]

df = df[
    [
        "Full Name",
        "School",
        "T-shirt size",
        "Priority?"
    ]
]

df.to_csv("nametags.csv", index=False)
