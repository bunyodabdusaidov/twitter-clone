from django.contrib.auth.models import User
from rest_framework import serializers

from tweet.models import Tweet


class TweetSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Tweet
        fields = ['url', 'id', 'author', 'content']


class TweetLikeSerializer(serializers.Serializer):
    def __init__(self, **kwargs):
        self.liked = True
        super(TweetLikeSerializer, self).__init__(**kwargs)

    def create(self, validated_data):
        raise NotImplementedError

    def update(self, instance, validated_data):
        user = self.context['request'].user
        likes = instance.liked.filter(author=user)
        if likes:
            likes.delete()
            self.liked = False

            return instance

        instance.liked.create(author=user)
        return instance


class TweetCommentSerializer(serializers.Serializer):
    def create(self, validated_data):
        user = self.context['request'].user
        comments = self.instance.commented.filter(author=user)


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
