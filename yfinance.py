from datetime import datetime, timedelta
from yahoo_fin import stock_info as si
import pandas as pd
import json
import os
import sys

with open('config.json') as f:
    config = json.load(f)
price_folder_path = config['price_path']

def get_price_data(symbol, start_date_str, end_date_str):
	start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
	end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

	data = si.get_data(symbol, start_date, end_date)
	stock_data = data[["open", "close", "low", "high", "volume"]]

	if not os.path.exists(price_folder_path):
		os.makedirs(price_folder_path)
	csv_filename = f"price-{symbol}.csv"
	csv_path = os.path.join(price_folder_path, csv_filename)
	stock_data.to_csv(csv_path, index=True, header=True, index_label="date")

def main():
	symbol = sys.argv[1]
	start_date = sys.argv[2]
	end_date = sys.argv[3]
	print(f"Running get_price_data w/ inputs ({symbol}, {start_date}, {end_date})...")
	get_price_data(symbol, start_date, end_date)

if __name__ == "__main__":
	main()