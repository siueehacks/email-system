import os

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

df["Full Name"] = df["First Name"] + " " + df["Last Name"]
df["Bus"] = df["SIUE Students: Bus ride request"].apply(
    lambda x: "Yes"
    if x == "I am an SIUE student and will request a bus ride to the T-Rex Center"
    else "No"
)
df["School"] = df["What school do you currently attend? If you're no longer a student, what school / university did you most recently graduate from?"]

df = df[[ "Full Name", "School", "Bus" ]]
df = df.loc[df["Bus"] == "Yes"]

df.to_csv("bus.csv", index=False)
