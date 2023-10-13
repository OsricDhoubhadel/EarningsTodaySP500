import pandas as pd
from ta import add_all_ta_features
from ta.utils import dropna
import warnings

# Suppress warnings
warnings.filterwarnings("ignore")

# Load datas
data = pd.read_csv('.\DJIA.csv', sep=',')

# Clean NaN values
data = dropna(data)

# Convert the 'Date' column to a datetime format
data['Date'] = pd.to_datetime(data['Date'], format='%d-%b-%y')

# Set the 'Date' column as the DataFrame index (required for ta library)
data.set_index('Date', inplace=True)

# Remove commas from numeric columns and convert them to float
numeric_cols = ['Open', 'High', 'Low', 'Close', 'Adj Close**', 'Volume']
for col in numeric_cols:
    data[col] = data[col].str.replace(',', '').astype(float)

# Add TA features to your DataFrame and drop NaNs
data = add_all_ta_features(data, open="Open", high="High", low="Low", close="Close", volume="Volume")

# Print all the columns of the DataFrame
print(data.columns)

# Save the DataFrame to a CSV file
data.to_csv('.\DJIA_TA.csv', sep=',', index=True)
