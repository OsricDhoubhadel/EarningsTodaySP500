import pandas as pd
from datetime import datetime, date
import requests, dotenv, os, time

dotenv.load_dotenv()
api_key = os.getenv("ALPHA_VANTAGE_API_KEY")

def get_earnings_data(symbol, api_key, sleeptime=0):
    """Use AlphaVantage API to get earnings data for a given symbol"""
    # Pause sleeptime seconds between API calls
    time.sleep(sleeptime)
    url = f"https://www.alphavantage.co/query?function=EARNINGS&symbol={symbol}&apikey={api_key}"

    # Make the API request
    data = requests.get(url).json()
    # print(data)

    # Create a DataFrame from the quarterlyEarnings data
    df = pd.DataFrame(data["quarterlyEarnings"])

    # Get today's date in "YYYY-MM-DD" format
    today_date = date.today().isoformat()

    # Filter the DataFrame for today's date
    today_data = df[df["fiscalDateEnding"] == today_date]

    if not today_data.empty:
        reported_eps = today_data.iloc[0]["reportedEPS"]
        surprise = today_data.iloc[0]["surprise"]
        surprise_percentage = today_data.iloc[0]["surprisePercentage"]
        return reported_eps, surprise, surprise_percentage
    else:
        return None, None, None

def get_today_earnings_data(csv_file_path):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file_path)

    # Convert the 'ReportDate' column to datetime format
    df["ReportDate"] = pd.to_datetime(df["ReportDate"])

    # Get the current date
    current_date = datetime.now().date()

    # Filter rows where 'ReportDate' is equal to the current date
    today_data = df[df["ReportDate"].dt.date == current_date]

    # Select only the desired columns
    result_df = today_data[["Symbol", "Name", "Estimate", "Currency"]]

    return result_df

# Call the function and print the returned DataFrame
result_df = get_today_earnings_data("../DataExamples/filtered_earnings_calendar.csv")

# Map get_earnings_data function to the result_df with a 15 second pause between API calls. Note: AlphaVantage API only allows 5 calls per minute or 100 calls per day.
result_df["ReportedEPS"], result_df["Surprise"], result_df["SurprisePercentage"] = zip(
    *result_df["Symbol"].apply(lambda symbol: get_earnings_data(symbol, api_key, 15))
)
print(result_df)

# Filter the result_df for rows where the SurprisePercentage is greater than 0 and sort the DataFrame by the SurprisePercentage column in descending order
result_df = result_df[result_df["SurprisePercentage"] > 0]
result_df = result_df.sort_values("SurprisePercentage", ascending=False)

print(result_df)

# Save the result_df to a CSV file in the DataExamples folder
result_df.to_csv("../DataExamples/todays_earnings.csv", index=False)