import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.tweet import Base, Tweet

class TestTweetModel(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Set up the database connection
        engine = create_engine('sqlite:///:memory:')
        Session = sessionmaker(bind=engine)
        cls.session = Session()

        # Create the tables in the in-memory database
        Base.metadata.create_all(engine)

    @classmethod
    def tearDownClass(cls):
        # Close the database session
        cls.session.close()

    def test_tweet_model(self):
        # Create a new Tweet object
        tweet = Tweet(
            tweeted_at='2023-06-12 10:00:00',
            user='JohnDoe',
            body='Hello, world!',
            sentiment_score=4.2,
            ticker='AAPL'
        )

        # Add the tweet to the session and commit the changes
        self.session.add(tweet)
        self.session.commit()

        # Retrieve the tweet from the session
        retrieved_tweet = self.session.query(Tweet).filter_by(user='JohnDoe').first()

        # Perform assertions to validate the tweet's attributes
        self.assertIsNotNone(retrieved_tweet)
        self.assertEqual(retrieved_tweet.tweeted_at, '2023-06-12 10:00:00')
        self.assertEqual(retrieved_tweet.user, 'JohnDoe')
        self.assertEqual(retrieved_tweet.body, 'Hello, world!')
        self.assertEqual(float(retrieved_tweet.sentiment_score), 4.2)
        self.assertEqual(retrieved_tweet.ticker, 'AAPL')

if __name__ == '__main__':
    unittest.main()

