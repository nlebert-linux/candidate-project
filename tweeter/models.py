from django.db import models


class TwitterUser(models.Model):
    """
    Description: Data and Meta Information of a Twitter User
    """
    user_id = models.CharField(max_length=256, unique=True)
    name = models.CharField(max_length=256, blank=True, null=True)
    username = models.CharField(max_length=256, blank=True, null=True)
    location = models.CharField(max_length=256, blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    description = models.CharField(max_length=256, blank=True, null=True)
    is_protected = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    followers = models.PositiveIntegerField(default=0)
    friends = models.PositiveIntegerField(default=0)
    listed = models.PositiveIntegerField(default=0)
    favourites = models.PositiveIntegerField(default=0)
    statuses = models.PositiveIntegerField(default=0)
    creation_date = models.DateTimeField()
    profile_image_url = models.URLField(blank=True, null=True)
    language = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        verbose_name = 'Twitter User'
        verbose_name_plural = 'Twitter Users'

    def __str__(self):
        return self.user_id


class Tweet(models.Model):
    """
    Description: Data and Meta Information of a Tweet
    """
    creation_date = models.DateTimeField(blank=True, null=True)
    tweet_id = models.CharField(max_length=256)
    content = models.CharField(max_length=200)
    source = models.CharField(max_length=256, blank=True, null=True)
    retweet_count = models.PositiveIntegerField(default=0)
    favorite_count = models.PositiveIntegerField(default=0)
    twitter_user = models.ForeignKey(
        TwitterUser,
        blank=True,
        null=True,
        related_name='tweets',
        on_delete=models.SET_NULL)

    class Meta:
        verbose_name = 'Tweet'
        verbose_name_plural = 'Tweets'

    def __str__(self):
        return self.tweet_id
