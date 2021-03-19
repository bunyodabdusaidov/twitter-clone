from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Tweet(models.Model):
    content = models.TextField(max_length=150)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)

    def __str__(self):
        return self.content[:5]

    @property
    def number_of_comments(self):
        return Comment.objects.filter(commented_to=self).count()


class Comment(models.Model):
    content = models.TextField(max_length=150)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    commented_to = models.ForeignKey(Tweet, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)


class Preference(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)
    value = models.IntegerField()
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{str(self.user)} : {str(self.tweet)}: {str(self.value)}"

    class Meta:
        unique_together = ('user', 'tweet', 'value')
