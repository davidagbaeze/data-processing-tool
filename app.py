import json
import requests
from datetime import datetime, timedelta, timezone
import pandas as pd
import time
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import schedule


app_url = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"
response = requests.get(app_url)

parsed_response = json.loads(response.text)

recent_records = []

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "sender@gmail.com"
SENDER_PASSWORD = "APP PASSWORD"
RECIPIENT_EMAIL = "receiver@example.com"


def filter_records():
    now = datetime.now(timezone.utc)
    one_week_ago = now - timedelta(days=7)
    vulnerabilities = parsed_response.get("vulnerabilities", [])

    for vuln in vulnerabilities:
        dateAdded = vuln.get("dateAdded")
        vuln_date = datetime.strptime(
            dateAdded, "%Y-%m-%d").replace(tzinfo=timezone.utc)
        if one_week_ago <= vuln_date <= now:
            recent_records.append(vuln)

    return recent_records


def create_report():
    records = filter_records()
    df = pd.DataFrame(records)

    filename = "vulnerability_report.xlsx"
    df.to_excel(filename, index=False)

    return filename


def email_report():
    report_file = create_report()

    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECIPIENT_EMAIL
    msg["Subject"] = f"Weekly Automated Report - {time.strftime('%Y-%m-%d')}"

    body = """ Dear Duke,
 I trust you are well.
 Please find attached the weekly vulnerability report from CISA.

 Best Regards,
 Python Bot."""
    msg.attach(MIMEText(body, "plain"))

    with open(report_file, "rb") as attachment:
        part = MIMEBase(
            "application", "vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        part.set_payload(attachment.read())

        encoders.encode_base64(part)
        part.add_header("Content-Disposition",
                        f"attachment; filename= {os.path.basename(report_file)}",)
    msg.attach(part)

    print("Connecting to SMTP server...")
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)


email_report()
print(f"Email sent successfully to {RECIPIENT_EMAIL}!")


schedule.every().monday.at("08:30").do(email_report)

print("Weekly Monday email scheduler started. Keep this script running...")

while True:
    schedule.run_pending()
    time.sleep(1)
