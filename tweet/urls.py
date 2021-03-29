from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'tweets', views.TweetViewSet)
router.register(r'users', views.UserViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls))
]


# urlpatterns = [
#     path('', TweetListView.as_view(), name='home'),
#     path('about/', about, name='about'),
#     path('tweet/new/', TweetView.as_view(), name='tweet'),
#     path('tweet/<int:pk>/', TweetDetailView.as_view(), name='tweet-detail'),
#     path('user/<str:username>', UserTweetListView.as_view(), name='user-tweets'),
#     path('tweet/<int:pk>/delete/', TweetDeleteView.as_view(), name='tweet-delete'),
#     path('user/<str:username>/following', FollowingListView.as_view(), name='user-following'),
#     path('user/<str:username>/followers', FollowersListView.as_view(), name='user-followers'),
#     path('tweet/<int:tweet_id>/preference/<int:user_preference>', tweet_preference, name='tweet_preference'),
# ]