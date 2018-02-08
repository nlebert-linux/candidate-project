from django.contrib import admin

from .models import Tweet
from .models import TwitterUser


# Register your models here.
class TweetInlineAdmin(admin.TabularInline):
    model = Tweet
    extra = 0


@admin.register(TwitterUser)
class TwitterUserAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'name', 'username', 'location', 'followers', 'friends']
    list_filter = ['is_protected', 'is_verified']
    inlines = [TweetInlineAdmin, ]


@admin.register(Tweet)
class TweetAdmin(admin.ModelAdmin):
    pass
