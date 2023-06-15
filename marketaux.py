import json
import requests
from datetime import datetime, timedelta
import os
import csv


with open('config.json') as f:
    config = json.load(f)
api_key = config['market_aux_api_key']
news_folder_path = config['news_path']

# from_date, to_date follow marketaux api criteria e.g. YYYY-MM-DD
def get_news(ticker, date_str):
	endpoint_url = "https://api.marketaux.com/v1/news/all"
	params = {
    	"symbols": ticker,
    	"api_token": api_key,
    	"language": "en",
    	"filter_entities": "true",
    	"published_on": date_str
	}

	response = requests.get(endpoint_url, params=params)
	if response.status_code == 200:
		news_data = response.json()
		print(f"200 OK - got news data w/ {len(news_data)} articles")
		return news_data["data"]
	else:
	    print("Failed to retrieve news. Status code:", response.status_code)

def write_news_csv(ticker, date_str, news_data): 
	if not os.path.exists(news_folder_path):
		os.makedirs(news_folder_path)
	csv_filename = f"news-{ticker}.csv"
	csv_path = os.path.join(news_folder_path, csv_filename)
	file_exists = os.path.isfile(csv_path)
	file_is_empty = not file_exists or os.stat(csv_path).st_size == 0
	fieldnames = ["uuid", "title", "url", "published_at", "date", "source", "entity_ticker", "entity_match_score", "entity_sentiment_score"]

	with open(csv_path, "a", newline="") as csvfile:
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
		if file_is_empty:
			writer.writeheader()
		for article in news_data:
			entity = article["entities"][0]  # Extract the first entity
			article_row = {
				"uuid": article["uuid"],
				"title": article["title"],
				"url": article["url"],
				"published_at": article["published_at"],
				"published_on": date_str,
				"source": article["source"],
				"entity_ticker": entity["symbol"],
				"entity_match_score": entity["match_score"],
				"entity_sentiment_score": entity["sentiment_score"]
			}
			writer.writerow(article_row)

def write_json(filepath, data):
	with open(filepath, "w") as file:
		json.dump(data, file)

def read_from_json(filepath):
	with open(filepath) as file:
		return json.load(file)

def search_entity(search):
	endpoint_url = "https://api.marketaux.com/v1/entity/search"
	params = {
    	"search": search,
    	"api_token": api_key
	}
	print("api_key:", api_key)
	response = requests.get(endpoint_url, params=params)
	if response.status_code == 200:
		print("200, got: ", response.json()["data"])
	else:
		print("Failed to retrieve news. Status code:", response.status_code)

def get_date_strings_in_range(from_date_str, to_date_str):
	start_date = datetime.strptime(from_date_str, "%Y-%m-%d")
	end_date = datetime.strptime(to_date_str, "%Y-%m-%d")
	current_date = start_date
	date_strings = []
	while current_date <= end_date:
		date_strings.append(current_date.strftime("%Y-%m-%d"))
		current_date += timedelta(days=1)
	return date_strings

def main():
	stonk = "TSLA"
	date_strs = get_date_strings_in_range("2023-05-14", "2023-06-14")
	for date_str in date_strs:
		#news = get_news(stonk, date_str)
		json_path = f"data/raw-news-TSLA-{date_str}.json"
		#write_json(json_path, news)
		news_from_json = read_from_json(json_path)
		write_news_csv(stonk, date_str, news_from_json)

if __name__ == "__main__":
	main()