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

result = (
    sheet.values().get(spreadsheetId=sheet_id, range="Form Responses 1").execute()
)

data = result["values"][1:]
headers = result["values"][0]

df = pd.DataFrame(data, columns=headers)

df.to_csv("data.csv", index=False)