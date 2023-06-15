from datetime import datetime, timedelta
from yahoo_fin import stock_info as si
import pandas as pd
import json
import os

with open('config.json') as f:
    config = json.load(f)
price_folder_path = config['price_path']

# Define the stock symbol and the date range
symbol = "TSLA"
end_date = datetime.now().date()
start_date = end_date - timedelta(days=30)

# Retrieve the stock data using yahoo_fin
data = si.get_data(symbol, start_date, end_date)

# Extract the desired columns
stock_data = data[["open", "close", "low", "high", "volume"]]

if not os.path.exists(price_folder_path):
	os.makedirs(price_folder_path)
csv_filename = f"price-{symbol}.csv"
csv_path = os.path.join(price_folder_path, csv_filename)

# Write the stock_data DataFrame to a CSV file
stock_data.to_csv(csv_path, index=True, header=True, index_label="date")