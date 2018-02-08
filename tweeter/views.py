from django.shortcuts import render
from rest_framework import viewsets
from .serializers import TweetSerializer
from .serializers import TwitterUserSerializer
from .models import Tweet
from .models import TwitterUser


# Create your views here.
class TwitterUserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API Endpoint that allows users to be viewed or edited.
    """
    queryset = TwitterUser.objects.all().order_by('user_id')
    serializer_class = TwitterUserSerializer
    filter_fields = ('is_protected', 'is_verified')


class TweetViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint allowing tweets to be viewed or edited.
    """
    queryset = Tweet.objects.all().order_by('tweet_id')
    serializer_class = TweetSerializer
    filter_fields = ('source', )
