import requests
import os
import json
from pathlib import Path
import logging
import praw

from reddit_api_app.settings import get_secret

from django.shortcuts import render

import saved_posts


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
    """Get saved posts from the user."""
    reddit = authenticate_api(request)

    user_all_saved_posts = reddit.user.me().saved(limit=None)

    suggestion_post_list = []
    for item in user_all_saved_posts:
        try:
            if item.subreddit == 'MovieSuggestions' or (
                item.subreddit == 'suggestmeabook'):
                suggestion_post_list.append(item.title)
        except AttributeError:
            # Comment, not submission.
            pass

    return render(request, 'saved_posts/show_data.html', {
        'data': suggestion_post_list
        })
