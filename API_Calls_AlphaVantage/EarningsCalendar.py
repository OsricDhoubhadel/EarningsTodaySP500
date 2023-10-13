import csv
import requests
import dotenv
import os

dotenv.load_dotenv()

ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
HORIZON = "3month"
FUNCTION = "EARNINGS_CALENDAR"

# API call Alpha Vantage and save data to CSV
CSV_URL = f"https://www.alphavantage.co/query?function={FUNCTION}&horizon={HORIZON}&apikey={ALPHA_VANTAGE_API_KEY}&datatype=csv"

     requests.Session() as s:
    download = s.get(CSV_URL)
    decoded_content = download.content.decode("utf-8")
    cr = csv.reader(decoded_content.splitlines(), delimiter=",")
    my_list = list(cr)
    with open(
        os.path.join("..", "DataExamples", "earnings_calendar.csv"), "w", newline=""
    ) as f:
        writer = csv.writer(f)
        writer.writerows(my_list)
    for row in my_list:
        print(row)
