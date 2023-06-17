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


train_ratio = 0.7
with open('config.json') as f:
    config = json.load(f)
news_fp = config['news_path']
price_fp = config['price_path']
experiment_results_fp = config['experiment_results_path']

price_data = pd.read_csv(os.path.join(price_fp, 'price-TSLA.csv'))  # Assuming CSV file with 'Date' and 'Price' columns
sentiment_data = pd.read_csv(os.path.join(news_fp, 'news-clean-TSLA.csv'))  # Assuming CSV file with 'Date' and 'Sentiment' columns

# Merge all relevant data based on the date
merged_data = pd.merge(price_data, sentiment_data, on='date', how='inner')
merged_data['price_direction'] = np.where(merged_data['close'].shift(-1) > merged_data['close'], 1, -1)

features = merged_data[['open', 'close', 'volume', 'high', 'low', 'weighted_sentiment']].values[:-1]
pd_target = merged_data['price_direction'].values[:-1]

scaler = MinMaxScaler(feature_range=(0, 1))
scaled_features = scaler.fit_transform(features)

train_size = int(train_ratio * len(scaled_features))
train_features = scaled_features[:train_size]
test_features = scaled_features[train_size:]

pd_train_target = pd_target[:train_size]
pd_test_target = pd_target[train_size:]

pd_model = Sequential()
pd_model.add(Dense(1, activation='sigmoid'))
pd_model.compile(loss='binary_crossentropy', optimizer='adam')
pd_model.fit(train_features, pd_train_target, epochs=10, batch_size=16, verbose=2)

pd_predictions = pd_model.predict(test_features)

print("pd_predictions", pd_predictions)
pd_eval_res = pd_model.evaluate(test_features, pd_test_target)
for i in range(0, len(pd_predictions)):
    print(f"\t({pd_predictions[i][0]}, {pd_test_target[i]})")
print("pd_eval", pd_eval_res)
