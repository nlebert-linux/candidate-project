from __future__ import unicode_literals
import logging
import json
import arrow
from django.conf import settings
from django.db.utils import IntegrityError
from celery import shared_task
from birdview.celery import app
from .models import Tweet
from .models import TwitterUser
from tweepy import OAuthHandler
from tweepy import Stream
import time
from tweepy.streaming import StreamListener

logger = logging.getLogger(__name__)


# Create our stream class, handles the twitter sample stream
class BirdSniffer(StreamListener):
    """
    Custom Stream class. Listen to the firehose for 5 minutes,
    then dump tweets into tasks for creation / update.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.time = time.time()
        self.limit = 60 * 5
        self.tweets = []

    def on_status(self, status):
        print(status.text)

    def on_data(self, data):
        # Listen for 5 minutes, then exit.
        while (time.time() - self.time) < self.limit:
            try:
                parse_tweet.delay(data=data)
                return True
            except Exception as e:
                print(e)
                pass

        with open('raw_data.json', 'w', encoding='utf-8') as raw_tweets:
            # Make our file valid json
            raw_tweets.write('[\n')
            raw_tweets.write(','.join(self.tweets))
            raw_tweets.write('\n]')

        return False

    def on_error(self, status):
        print(status)


@app.task(name='run_stream')
def run_stream():
    # Grab our API keys
    consumer_key = settings.TWEETER_CONSUMER_KEY
    consumer_secret = settings.TWEETER_CONSUMER_SECRET
    access_token = settings.TWEETER_ACCESS_TOKEN
    access_token_secret = settings.TWEETER_ACCESS_TOKEN_SECRET

    auth = OAuthHandler(
        consumer_key,
        consumer_secret
    )
    auth.set_access_token(
        access_token,
        access_token_secret
    )

    stream = Stream(auth, BirdSniffer())
    stream.sample(async=True, languages=['en', ])

    return True


@shared_task
def parse_tweet(data=None):
    tweet = json.loads(data)

    # grab users and related tweets to see if we already have them or not
    # Since we are streaming all this data, there isn't any real way to sort
    # by users / tweets. Unfortunately, this is going to slow us down.
    #
    # Possible fix: put a unique constraint on identifying attributes,
    # and let the database worry about whether they exist or not. Let the task
    # fail if they already exist. That might help with scaling issues.
    try:
        user = TwitterUser.objects.get(user_id=tweet['user']['id'])
    except TwitterUser.DoesNotExist as not_exist:
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
        logger.debug("User does not exist: creating.")
    except IntegrityError as duplicate:
        user = TwitterUser.objects.update(
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
        logger.debug("User doesn't exist; trying update_or_create.\n\n{e}".format(e=duplicate))
    except Exception as no_clue:
        logger.critical("User creation / update failed, and I have no idea why!\n{}".format(no_clue))
        return False

    Tweet.objects.update_or_create(
        creation_date=arrow.get(tweet['created_at'], 'ddd MMM D hh:mm:ss Z YYYY').datetime,
        tweet_id=tweet['id'],
        content=tweet['text'],
        source=tweet['source'],
        retweet_count=tweet['retweet_count'],
        favorite_count=tweet['favorite_count'],
        twitter_user=user
    )

    return True
