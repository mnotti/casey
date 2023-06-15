import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import LSTM, Dense
import json
import os

with open('config.json') as f:
    config = json.load(f)
news_fp = config['news_path']
price_fp = config['price_path']

# Load stock price data and news sentiment
price_data = pd.read_csv(os.path.join(price_fp, 'price-TSLA.csv'))  # Assuming CSV file with 'Date' and 'Price' columns
sentiment_data = pd.read_csv(os.path.join(news_fp, 'news-clean-TSLA.csv'))  # Assuming CSV file with 'Date' and 'Sentiment' columns

# Merge all relevant data based on the date
merged_data = pd.merge(price_data, sentiment_data, on='date', how='left')
print("merged_data:", merged_data)
merged_data['weighted_sentiment'] = merged_data['weighted_sentiment'].fillna(0)
print("merged_data2:", merged_data)

# Prepare input features and target variable
features = merged_data[['open', 'close', 'volume', 'high', 'low', 'weighted_sentiment']].values
target = merged_data['close'].shift(-1).values[:-1]  # Shifting target variable by 1 days for price direction prediction

# Scale the features
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_features = scaler.fit_transform(features)

window_size = 5
input_sequences = []
output_targets = []
for i in range(len(scaled_features) - window_size - 1):
	input_sequences.append(scaled_features[i:i+window_size])
	output_targets.append(target[i+window_size])

input_sequences = np.array(input_sequences)
output_targets = np.array(output_targets)

# Split the data into training and test sets
train_size = int(0.7 * len(scaled_features))
train_features = input_sequences[:train_size]
print("train_features:", len(train_features))
train_target = output_targets[:train_size]
test_features = input_sequences[train_size:]
print("test_features:", len(test_features))
test_target = output_targets[train_size:]

model = Sequential()
model.add(LSTM(50, input_shape=(window_size, train_features.shape[2])))
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
print("test_target", test_target)
print("test_predictions", scaled_predictions)



evaluation_results = model.evaluate(test_features, test_target)
print("Eval Results:", evaluation_results)
print("Predictions:", predictions)
print("Scaled predictions:", scaled_predictions)
print("Predicted Direction:", predicted_direction)

