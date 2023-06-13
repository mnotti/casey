from models.tweet import Tweet
from database import get_session

session = get_session()

tweet = Tweet(
    tweeted_at='2023-06-12 10:00:00',
    user='JohnDoe',
    body='AAPL is a really cool stonk',
    sentiment_score=4.2,
    ticker='AAPL'
)

session.add(tweet)
session.commit()

