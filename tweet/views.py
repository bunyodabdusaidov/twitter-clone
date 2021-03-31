from django.contrib.auth.models import User
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from tweet.models import Tweet
from .serializers import TweetSerializer, UserSerializer, TweetLikeSerializer, TweetCommentSerializer
from .permissions import IsOwnerOrReadOnly


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class TweetViewSet(viewsets.ModelViewSet):
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(methods=['POST'], detail=True, url_name='like', serializer_class=TweetLikeSerializer)
    def like(self, request, pk=None):
        tweet = self.get_object()
        serializer = self.get_serializer_class()(instance=tweet, data={},
                                                 context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_201_CREATED if serializer.liked else
                        status.HTTP_204_NO_CONTENT)

    @action(methods=['POST'], detail=True, url_name='comment', serializer_class=TweetCommentSerializer)
    def comment(self, request, pk=None):
        tweet = self.get_object()
        serializer = self.get_serializer_class()(instance=tweet, data=request.data,
                                                 context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
