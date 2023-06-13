# models/tweet.py
from sqlalchemy import Column, Integer, String, TIMESTAMP, Numeric
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Tweet(Base):
    __tablename__ = 'tweets'

    id = Column(Integer, primary_key=True)
    tweeted_at = Column(String(50))
    user = Column(String(100))
    body = Column(String(280))
    sentiment_score = Column(Numeric(precision=10, scale=2), nullable=True)
    ticker = Column(String(10), nullable=True)
