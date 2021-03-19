from django.urls import path
from .views import (
    TweetListView,
    TweetDetailView,
    TweetView,
    TweetDeleteView,
    UserTweetListView,
    FollowingListView,
    FollowersListView,
    about,
    tweetpreference,
)

urlpatterns = [
    path('', TweetListView.as_view(), name='home'),
    path('about/', about, name='about'),
    path('tweet/new/', TweetView.as_view(), name='tweet'),
    path('tweet/<int:pk>/', TweetDetailView.as_view(), name='tweet-detail'),
    path('user/<str:username>', UserTweetListView.as_view(), name='user-tweets'),
    path('tweet/<int:pk>/delete/', TweetDeleteView.as_view(), name='tweet-delete'),
    path('user/<str:username>/following', FollowingListView.as_view(), name='user-following'),
    path('user/<str:username>/followers', FollowersListView.as_view(), name='user-followers'),
    path('tweet/<int:tweetid>/preference/<int:userpreference>', tweetpreference, name='tweetpreference'),
]