import pandas as pd
from datetime import datetime

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
print(result_df)
