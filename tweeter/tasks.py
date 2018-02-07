import json
from birdview.celery import app
from django.conf import settings
from .models import Tweet
from .models import TwitterUser

from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import arrow


@app.task(name='run_stream')
def run_stream():

    class MyListener(StreamListener):
        def on_data(self, data):
            process_tweet.delay(data)
            return True

        def on_error(self, status):
            print(status)
            return True

    auth = OAuthHandler(
        settings.TWEETER_CONSUMER_KEY,
        settings.TWEETER_CONSUMER_SECRET
    )
    auth.set_access_token(
        settings.TWEETER_ACCESS_TOKEN,
        settings.TWEETER_ACCESS_TOKEN_SECRET
    )

    twitter_stream = Stream(auth, MyListener())
    twitter_stream.filter(track=['#python', '#google'], async=True)


@app.task(name='tweepy_stream')
def process_tweet(data=None):
    tweet = json.loads(data)

    # grab users and related tweets to see if we already have them or not
    # Since we are streaming all this data, there isn't any real way to sort
    # by users / tweets. Unfortunately, this is going to slow us down.
    #
    # Possible fix: put a unique constraint on identifying attributes,
    # and let the database worry about whether they exist or not. Let the task
    # fail if they already exist. That might help with scaling issues.
    all_users = TwitterUser.objects.values('user_id').all()
    if tweet['user']['id'] not in all_users:
        user, created = TwitterUser.objects.update_or_create(
            user_id=tweet['user']['id'],
            name=tweet['user']['name'],
            username=tweet['user']['screen_name'],
            location=tweet['user']['location'],
            url=tweet['user']['url'],
            description=tweet['user']['description'],
            is_protected=tweet['user']['protected'],
            is_verified=tweet['user']['verified'],
            followers=tweet['user']['followers_count'],
            friends=tweet['user']['friends_count'],
            listed=tweet['user']['listed_count'],
            statuses=tweet['user']['listed_count'],
            favourites=tweet['user']['favourites_count'],
            creation_date=arrow.get(tweet['user']['created_at'], 'ddd MMM D hh:mm:ss Z YYYY').datetime,
            profile_image_url=tweet['user']['profile_image_url'],
            language=tweet['user']['lang']
        )

    all_tweets = Tweet.objects.values('tweet_id').all()
    if tweet['id'] not in all_tweets:
        Tweet.objects.update_or_create(
            creation_date=arrow.get(tweet['created_at'], 'ddd MMM D hh:mm:ss Z YYYY').datetime,
            tweet_id=tweet['id'],
            content=tweet['text'],
            source=tweet['source'],
            retweet_count=tweet['retweet_count'],
            favorite_count=tweet['favorite_count'],
            twitter_user=user
        )
