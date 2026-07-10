from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
import csv
import os

app = FastAPI()

FILE_NAME = "alerts_log.csv"

# ✅ Define exact structure
class Alert(BaseModel):
    event_id: int
    frequency: int
    payload_size: int
    failed_logins: int


@app.get("/")
def home():
    return {"message": "Server is running"}


@app.post("/alert")
def receive_alert(alert: Alert):
    file_exists = os.path.isfile(FILE_NAME)

    with open(FILE_NAME, mode="a", newline="") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow(["Timestamp", "Event_ID", "Frequency", "Payload_Size", "Failed_Logins"])

        writer.writerow([
            datetime.now(),
            alert.event_id,
            alert.frequency,
            alert.payload_size,
            alert.failed_logins
        ])

    print("✅ Received:", alert)

    return {"status": "logged"}