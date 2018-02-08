from django.conf.urls import url
from django.conf.urls import include
from rest_framework import routers
from .views import TweetViewSet
from .views import TwitterUserViewSet


router = routers.DefaultRouter()
router.register(r'twitteruser', TwitterUserViewSet)
router.register(r'tweet', TweetViewSet)

app_name = 'tweeter'
urlpatterns = [
    url('^', include(router.urls)),
    url(r'^api_auth/', include('rest_framework.urls', namespace='rest_framework'))
]
