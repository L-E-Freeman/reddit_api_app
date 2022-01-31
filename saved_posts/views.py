from urllib import request
import requests
import os
import json
from pathlib import Path
import logging
import praw

from saved_posts.models import SavedPost, TopLevelComment
from reddit_api_app.settings import get_secret
from django.views.generic.list import ListView

from django.shortcuts import render


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

def get_top_level_comments(request):
    """Get top level comments from each of the users saved posts."""

    get_saved_posts(request)
    reddit = authenticate_api(request)
    all_posts = SavedPost.objects.all()

    for post in all_posts:
        # Create submission instance to get comments
        submission = reddit.submission(url=post.post_link)
        submission.comments.replace_more(limit=0)
        # Check if post has correct number of comments attached
        if post.toplevelcomment_set.all().count() != post.number_comments:
            for comment in submission.comments:
                # If comment does not already exist, save comment, else pass.
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

class IndexView(ListView):
    """Returns index list of saved posts."""

    # Update post list.
    get_saved_posts(request)

    model = SavedPost
    template_name = 'saved_posts/index.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return SavedPost.objects.all()
    
