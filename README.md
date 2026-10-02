A Python script that pulls the latest entries from CISA's Known Exploited Vulnerabilities (KEV) catalog, filters for those added in the last 7 days, saves them to an Excel report, and emails the report automatically.

## How It Works

1. Downloads the KEV catalog (JSON) from the [CISA feed](https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json).
2. Keeps only vulnerabilities whose `dateAdded` falls within the past 7 days.
3. Writes the results to `vulnerability_report.xlsx` using pandas.
4. Emails the spreadsheet as an attachment over Gmail SMTP.
5. Repeats on a schedule (Mondays at 08:30) while the script is running.

## Requirements

- Python 3.8+
- A Gmail account with an [App Password](2-Step Verification must be enabled)

Install dependencies:

```bash
pip install schedule
```
