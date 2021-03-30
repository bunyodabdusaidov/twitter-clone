from django.db import models
from django.contrib.auth.models import User


class Tweet(models.Model):
    content = models.TextField(blank=False, max_length=150)
    author = models.ForeignKey(User, related_name='tweets', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    liked = models.ManyToManyField('TweetLike', related_name='tweet_likes')
    comments = models.ManyToManyField('TweetComment', related_name='tweet_comments')

    def __str__(self):
        return self.content

    class Meta:
        ordering = ['date']


class TweetLike(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tweet_likes')
    created_at = models.DateTimeField(auto_now_add=True)


class TweetComment(models.Model):
    comment = models.TextField(max_length=150)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tweet_comments')
    created_at = models.DateTimeField(auto_now_add=True)

#
# class Preference(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)
#     value = models.IntegerField()
#     date = models.DateTimeField(default=timezone.now)
#
#     def __str__(self):
#         return f"{str(self.user)} : {str(self.tweet)}: {str(self.value)}"
#
#     class Meta:
#         unique_together = ('user', 'tweet', 'value')
