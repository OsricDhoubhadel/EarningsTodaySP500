import csv
import requests
import dotenv
import os
from bs4 import BeautifulSoup
import pandas as pd

dotenv.load_dotenv()

api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
horizon = "3month"

def filter_and_save_earnings_data(api_key, horizon):
    FUNCTION = "EARNINGS_CALENDAR"
    
    # Step 1: Download the list of S&P 500 companies from Wikipedia
    WIKIPEDIA_URL = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    response = requests.get(WIKIPEDIA_URL)
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table", {"class": "wikitable"})
    sp500_companies = [row.findAll("td")[0].text.strip() for row in table.findAll("tr")[1:]]
    
    # Step 2: API call to Alpha Vantage
    CSV_URL = f"https://www.alphavantage.co/query?function={FUNCTION}&horizon={horizon}&apikey={api_key}&datatype=csv"
    with requests.Session() as s:
        download = s.get(CSV_URL)
        decoded_content = download.content.decode("utf-8")
        cr = csv.reader(decoded_content.splitlines(), delimiter=",")
        data_list = list(cr)
    
    # Step 3: Filter data based on S&P 500 tickers and convert it to a DataFrame
    filtered_data = [data for data in data_list if data[0] in sp500_companies]
    filtered_df = pd.DataFrame(filtered_data, columns=["symbol", "name", "reportDate", "fiscalDateEnding", "estimate", "currency"])
    
    # Rename columns to match the required header
    filtered_df.rename(columns={
        'symbol': 'Symbol',
        'name': 'Name',
        'reportDate': 'ReportDate',
        'fiscalDateEnding': 'FiscalDateEnding',
        'estimate': 'Estimate',
        'currency': 'Currency'
    }, inplace=True)
    
    # Step 4: Save filtered data to a CSV file
    filtered_df.to_csv("../DataExamples/filtered_earnings_calendar.csv", index=False)
    
    # Print the filtered data
    print(filtered_df)

# Call the function with your API key and horizon
filter_and_save_earnings_data(api_key, horizon)
