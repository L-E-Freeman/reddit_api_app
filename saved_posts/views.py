import os
import json
from pathlib import Path
import logging
import praw

from saved_posts.models import SavedPost, TopLevelComment
from reddit_api_app.settings import get_secret

from django.views import generic
from django.shortcuts import render
from django.core import serializers
from django.http import JsonResponse


logger = logging.getLogger("myLogger")
    
def authenticate_api(request):
    """Initializing Reddit object with credentials and returning."""

    # Getting base directory path
    BASE_DIR = Path(__file__).resolve().parent.parent

    # Joining correct file to base directory path and opening
    with open(os.path.join(BASE_DIR, 'secrets.json')) as secrets_file:
        secrets = json.load(secrets_file)

    reddit = praw.Reddit(
        client_id=get_secret("PERSONAL_USE_SCRIPT"),
        client_secret=get_secret("SECRET_TOKEN"),
        password=get_secret("REDDIT_PASSWORD"),
        user_agent="SuggestBotV1.0",
        username=get_secret("REDDIT_USERNAME"),
    )

    return reddit

def get_saved_posts(request):
    """Get saved posts from the authenticated user."""

    reddit = authenticate_api(request)

    user_all_saved_posts = reddit.user.me().saved(limit=None)

    for item in user_all_saved_posts:
        try:
            if item.subreddit == 'MovieSuggestions' or (
                item.subreddit == 'suggestmeabook'):
                # If saved post does not exist
                if not SavedPost.objects.filter(
                    post_title = item.title).exists():
                    sp = SavedPost(
                        post_title = item.title, 
                        number_upvotes = item.score, 
                        number_comments = item.num_comments,
                        post_link = item.url
                    )
                    sp.save()
                else:
                    pass
        except AttributeError:
            # Comment, not submission.
            pass

def compare_saved_posts(request):
    """
    Compare current post list with updated to check for posts
    that might have been saved while app was running and returns them.
    """

    current_posts = SavedPost.objects.all()
    get_saved_posts(request)
    new_posts = SavedPost.objects.all()

    updated_posts = []
    for post in new_posts:
        if post not in current_posts:
            updated_posts.append(post)

    return updated_posts

def get_top_level_comments(request, posts):
    """Get top level comments from each of the users saved posts."""

    reddit = authenticate_api(request)
    posts = posts

    for post in posts:
        # Create submission instance to get comments
        submission = reddit.submission(url=post.post_link)
        submission.comments.replace_more(limit=0)
        # Check if post has correct number of comments attached
        if post.toplevelcomment_set.all().count() != post.number_comments:
            for comment in submission.comments:
                # If comment does not already exist, save comment, else do not
                # add duplicate comment.
                if not TopLevelComment.objects.filter(contents = comment.body):
                    tlc = TopLevelComment(
                        parent_post = post,
                        contents = comment.body, 
                        number_upvotes = comment.score
                    )
                    tlc.save()
                else:
                    pass
        else: 
            pass

class IndexView(generic.ListView):
    """Returns index list of saved posts."""

    model = SavedPost
    template_name = 'saved_posts/index.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return SavedPost.objects.all()
    
class DetailView(generic.DetailView):
    """Displays top level comments from a single post."""
    model = SavedPost
    template_name = 'saved_posts/detail.html'
    context_object_name = 'post'

def return_new_posts(request): 
    """
    Compares queryset of posts - current vs updated. Adds information from new
    posts to a dict and returns as JSON response. Also triggers comment 
    additions for updated posts.
    """
    updated_posts = compare_saved_posts(request)
    get_top_level_comments(request, updated_posts)

    posts_to_add = {}
    for post in updated_posts:
        posts_to_add['post_title'] = post.post_title
        posts_to_add['post_id'] = post.post_id

    return JsonResponse(posts_to_add)
   