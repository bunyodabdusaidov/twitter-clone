import sys

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, DeleteView

from tweet.models import Tweet, Comment, Preference
from users.models import Follow
from .forms import NewCommentForm


def is_users(post_user, logged_user):
    return post_user == logged_user


class TweetListView(LoginRequiredMixin, ListView):
    model = Tweet
    template_name = 'tweet/home.html'
    context_object_name = 'tweets'
    ordering = ['-date']

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        all_users = []
        data_counter = Tweet.objects.values('author')\
            .annotate(author_count=Count('author'))\
            .order_by('-date')[:5]

        for aux in data_counter:
            all_users.append(User.objects.filter(pk=aux['author']).first())

        data['preference'] = Preference.objects.all()
        data['all_users'] = all_users
        print(all_users, file=sys.stderr)
        return data

    def get_queryset(self):
        user = self.request.user
        qs = Follow.objects.filter(following=user)
        follows = [user]
        for obj in qs:
            follows.append(obj.followers)
        return Tweet.objects.filter(author__in=follows).order_by('-date')


class UserTweetListView(LoginRequiredMixin, ListView):
    model = Tweet
    template_name = 'tweet/user_tweets.html'
    context_object_name = 'tweets'

    def visible_user(self):
        return get_object_or_404(User, username=self.kwargs.get('username'))

    def get_context_data(self, **kwargs):
        visible_user = self.visible_user()
        logged_user = self.request.user
        print(logged_user.username == '', file=sys.stderr)

        if logged_user.username == '' or logged_user is None:
            can_follow = False
        else:
            can_follow = (Follow.objects.filter(following=logged_user,
                                                followers=visible_user).count() == 0)
        data = super().get_context_data(**kwargs)

        data['user_profile'] = visible_user
        data['can_follow'] = can_follow
        return data

    def get_queryset(self):
        user = self.visible_user()
        return Tweet.objects.filter(author=user).order_by('-date')

    def post(self, request, *args, **kwargs):
        if request.user.id is not None:
            follows_between = Follow.objects.filter(following=request.user,
                                                    followers=self.visible_user())

            if 'follow' in request.POST:
                new_relation = Follow(following=request.user, followers=self.visible_user())
                if follows_between.count() == 0:
                    new_relation.save()
            elif 'unfollow' in request.POST:
                if follows_between.count() > 0:
                    follows_between.delete()

        return self.get(self, request, *args, **kwargs)


class TweetDetailView(DetailView):
    model = Tweet
    template_name = 'tweet/tweet_detail.html'
    context_object_name = 'tweet'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        comments = self.get_object().comment_set.order_by('-date')
        data['comments'] = comments
        data['form'] = NewCommentForm(instance=self.request.user)
        return data

    def post(self, request, *args, **kwargs):
        new_comment = Comment(content=request.POST.get('content'),
                              author=self.request.user,
                              commented_to=self.get_object())
        new_comment.save()

        return self.get(self, request, *args, **kwargs)


class TweetDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Tweet
    template_name = 'tweet/tweet_delete.html'
    context_object_name = 'tweet'
    success_url = '/'

    def test_func(self):
        return is_users(self.get_object().author, self.request.user)


class TweetView(LoginRequiredMixin, CreateView):
    model = Tweet
    fields = ['content']
    template_name = 'tweet/tweet_new.html'
    success_url = '/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['tag_line'] = 'Tweet'
        return data


class FollowingListView(ListView):
    model = Follow
    template_name = 'tweet/follow.html'
    context_object_name = 'follows'

    def visible_user(self):
        return get_object_or_404(User, username=self.kwargs.get('username'))

    def get_queryset(self):
        user = self.visible_user()
        return Follow.objects.filter(following=user).order_by('-date')

    def get_context_data(self, *, object_list=None, **kwargs):
        data = super().get_context_data(**kwargs)
        data['follow'] = 'following'
        return data


class FollowersListView(ListView):
    model = Follow
    template_name = 'tweet/follow.html'
    context_object_name = 'follows'

    def visible_user(self):
        return get_object_or_404(User, username=self.kwargs.get('username'))

    def get_queryset(self):
        user = self.visible_user()
        return Follow.objects.filter(followers=user).order_by('-date')

    def get_context_data(self, *, object_list=None, **kwargs):
        data = super().get_context_data(**kwargs)
        data['follow'] = 'followers'
        return data


def about(request):
    return render(request, 'tweet/about.html', {'title': 'About'})


@login_required
def tweetpreference(request, tweetid, userpreference):
    if request.method == 'POST':
        eachtweet = get_object_or_404(Tweet, id=tweetid)
        obj = ''
        valueobj = ''

        try:
            obj = Preference.objects.get(user=request.user, tweet=eachtweet)
            valueobj  = obj.value  # value of userpreference
            valueobj = int(valueobj)
            userpreference = int(userpreference)

            if valueobj != userpreference:
                obj.delete()
                upref = Preference()
                upref.user = request.user
                upref.tweet = eachtweet
                upref.value = userpreference

                if userpreference == 1 and valueobj != 1:
                    eachtweet.likes += 1
                    eachtweet.dislikes -= 1
                elif userpreference == 2 and valueobj != 2:
                    eachtweet.dislikes += 1
                    eachtweet.likes -= 1

                upref.save()
                eachtweet.save()

                context = {
                    'eachtweet': eachtweet,
                    'tweetid': tweetid
                }
                return redirect('home')

            elif valueobj == userpreference:
                obj.delete()

                if userpreference == 1:
                    eachtweet.likes -= 1
                elif userpreference == 2:
                    eachtweet.dislikes -= 1

                eachtweet.save()
                context = {
                    'eachtweet': eachtweet,
                    'tweetid': tweetid
                }
                return redirect('home')

        except Preference.DoesNotExist:
            upref = Preference()
            upref.user = request.user
            upref.tweet = eachtweet
            upref.value = userpreference
            userpreference = int(userpreference)

            if userpreference == 1:
                eachtweet.likes += 1
            elif userpreference == 2:
                eachtweet.dislikes += 1

            upref.save()
            eachtweet.save()

            context = {
                'eachtweet': eachtweet,
                'tweetid': tweetid
            }

            return redirect('home')

    else:
        eachtweet = get_object_or_404(Tweet, id=tweetid)
        context = {
            'eachtweet': eachtweet,
            'tweetid': tweetid
        }

        return redirect('home')