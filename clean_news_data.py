import pandas as pd
import json
import os

with open('config.json') as f:
    config = json.load(f)
news_fp = config['news_path']
pd.set_option("display.max_rows", None)
sentiment_data = pd.read_csv(os.path.join(news_fp, "news-TSLA.csv"))
clean_df = sentiment_data.drop(['title', 'source', 'entity_ticker', 'published_at', 'url', 'uuid'], axis=1)
clean_df['weighted_sentiment'] = clean_df['entity_match_score'] * clean_df['entity_sentiment_score']
clean_df = clean_df.groupby('date')['weighted_sentiment'].sum().reset_index()
print("clean_df:", clean_df)
clean_df.to_csv(os.path.join(news_fp, 'news-clean-TSLA.csv'), index=False)
