from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Tweet


class TweetSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Tweet
        fields = ['url', 'id', 'author', 'content', 'likes']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    tweets = serializers.HyperlinkedRelatedField(many=True, view_name='tweet-detail', read_only=True)

    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'tweets']


