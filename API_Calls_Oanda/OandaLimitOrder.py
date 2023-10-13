import os
import oandapyV20
from oandapyV20 import API
from oandapyV20.exceptions import V20Error
from oandapyV20.endpoints.orders import OrderCreate

# Load access token from .env file
from dotenv import load_dotenv
load_dotenv()

access_token = os.getenv("OANDA_ACCESS_TOKEN")
account_id = os.getenv("OANDA_ACCOUNT_ID")

# Create an instance of the API class
api = API(access_token=access_token)

# Define the parameters for the limit order
params = {
  "order": {
    "price": "2590",
    # "stopLossOnFill": {
    #   "timeInForce": "GTC",
    #   "price": "2550"
    # },
    "timeInForce": "GTC",
    "instrument": "XAU_CAD",
    "units": "10",
    "type": "LIMIT",
    "positionFill": "DEFAULT"
  }
}

# Create the limit order
try:
    r = OrderCreate(accountID=account_id, data=params)
    response = api.request(r)
    print(response)
except V20Error as e:
    print("Error: {}".format(e))

