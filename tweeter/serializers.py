from rest_framework import serializers
from .models import Tweet
from .models import TwitterUser


class TwitterUserSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='api:twitteruser-detail'
    )
    tweets = serializers.HyperlinkedRelatedField(
        view_name='api:tweet-detail',
        queryset=Tweet.objects.all(),
        many=True
    )

    class Meta:
        model = TwitterUser
        fields = (
            'user_id',
            'name',
            'username',
            'location',
            'url',
            'description',
            'is_protected',
            'is_verified',
            'followers',
            'friends',
            'listed',
            'favourites',
            'statuses',
            'creation_date',
            'profile_image_url',
            'language',
            'tweets'
        )


class TweetSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='api:tweet-detail')
    twitter_user = serializers.HyperlinkedRelatedField(
        view_name='api:twitteruser-detail',
        queryset=TwitterUser.objects.all(),
        many=False
    )

    class Meta:
        model = Tweet
        fields = '__all__'
