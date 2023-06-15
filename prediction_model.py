import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import LSTM, Dense
import json
import os
import sys
import csv
import time


with open('config.json') as f:
    config = json.load(f)
news_fp = config['news_path']
price_fp = config['price_path']
experiment_results_fp = config['experiment_results_path']

def run_prediction(window_size, train_ratio, lstm_units):
	print(f"Running prediction(window_size={window_size}, train_ratio={train_ratio}, lstm_units={lstm_units})")
	# Load stock price data and news sentiment
	price_data = pd.read_csv(os.path.join(price_fp, 'price-TSLA.csv'))  # Assuming CSV file with 'Date' and 'Price' columns
	sentiment_data = pd.read_csv(os.path.join(news_fp, 'news-clean-TSLA.csv'))  # Assuming CSV file with 'Date' and 'Sentiment' columns

	# Merge all relevant data based on the date
	merged_data = pd.merge(price_data, sentiment_data, on='date', how='inner')

	# Prepare input features and target variable
	features = merged_data[['open', 'close', 'volume', 'high', 'low', 'weighted_sentiment']].values
	target = merged_data['close'].shift(-1).values[:-1]  # Shifting target variable by 1 days for price direction prediction

	# Scale the features
	scaler = MinMaxScaler(feature_range=(0, 1))
	scaled_features = scaler.fit_transform(features)

	input_sequences = []
	output_targets = []
	for i in range(len(scaled_features) - window_size - 1):
		input_sequences.append(scaled_features[i:i+window_size])
		output_targets.append(target[i+window_size])

	input_sequences = np.array(input_sequences)
	output_targets = np.array(output_targets)

	# Split the data into training and test sets
	train_size = int(train_ratio * len(scaled_features))
	train_features = input_sequences[:train_size]
	train_target = output_targets[:train_size]
	test_features = input_sequences[train_size:]
	print(f"(train,test) features: ({len(train_features)},{len(test_features)})")
	test_target = output_targets[train_size:]

	model = Sequential()
	model.add(LSTM(lstm_units, input_shape=(window_size, train_features.shape[2])))
	model.add(Dense(1)) # number of predictions per target
	model.compile(loss='mean_squared_error', optimizer='adam')

	# Train the model
	model.fit(train_features, train_target, epochs=10, batch_size=16, verbose=2)

	# Predict on the test set
	predictions = model.predict(test_features)
	scaler.fit(merged_data[['close']])
	scaled_predictions = scaler.inverse_transform(predictions)
	predicted_prices = scaled_predictions.flatten()
	predicted_direction = np.where(predicted_prices > test_target, 1, -1)
	evaluation_results = model.evaluate(test_features, test_target)
	print("(prediction, target):")
	for i in range(0, len(scaled_predictions)):
		print(f"\t({scaled_predictions[i][0]}, {test_target[i]})")
	print("Eval Results:", evaluation_results)
	return evaluation_results

def main():
	min_eval_result = sys.maxsize
	min_eval_params = [None] * 3
	window_size_min = 1
	window_size_max = 61
	window_size_step = 2
	train_ratio_int_min = 7
	train_ratio_int_max = 8
	train_ratio_int_step = 1
	lstm_units_min = 50
	lstm_units_max = 51
	lstm_units_step = 1

	if not os.path.exists(experiment_results_fp):
		os.makedirs(experiment_results_fp)
	ts_ms = int(time.time() * 1000)
	csv_filename = f"window_size-{ts_ms}.csv"
	csv_path = os.path.join(experiment_results_fp, csv_filename)
	file_exists = os.path.isfile(csv_path)
	file_is_empty = not file_exists or os.stat(csv_path).st_size == 0
	fieldnames = ["window_size", "train_ratio", "lstm_units", "eval_result"]
	with open(csv_path, "w", newline="") as csvfile:
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
		if file_is_empty:
			writer.writeheader()
		
		for window_size in range(window_size_min, window_size_max, window_size_step):
			for train_int in range(train_ratio_int_min, train_ratio_int_max, train_ratio_int_step):
				train_ratio = train_int/10
				for lstm_units in range(lstm_units_min, lstm_units_max, lstm_units_step):
					res = run_prediction(window_size, train_ratio, lstm_units)
					result_row = {
						"window_size": window_size,
						"train_ratio": train_ratio,
						"lstm_units": lstm_units,
						"eval_result": res
					}
					writer.writerow(result_row)
					if res < min_eval_result:
						min_eval_result = res
						min_eval_params[0] = window_size
						min_eval_params[1] = train_ratio
						min_eval_params[2] = lstm_units
	print(f'Best fitting model: (window_size={window_size}, train_ratio={train_ratio}, lstm_units={lstm_units}) => result: {min_eval_result}')

if __name__ == "__main__":
	main()



