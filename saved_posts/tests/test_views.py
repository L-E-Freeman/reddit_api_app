from django.test import TestCase
from django.test import RequestFactory
from django.urls import reverse
from reddit_api_app.settings import get_secret
from saved_posts.views import get_saved_posts
from .views import *

import praw
import json
import os
from pathlib import Path

class AuthenticationTests(TestCase):
    """Tests for PRAW authentication."""

    def authenticate_user(self):
        """Authenticate user instance"""
        BASE_DIR = Path(__file__).resolve().parent.parent.parent

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

    def test_user_authenticated(self):
        """If user is authenticated properly, response should return the
        Reddit username used to authenticate."""
        
        reddit = self.authenticate_user()
        response = reddit.user.me()
    
        self.assertEqual(response, get_secret("REDDIT_USERNAME"))

class ViewTests(TestCase):
    """Tests for views."""
    
    def setUp(self): 
        self.factory = RequestFactory()

    def test_if_posts_exist_in_db(self):
        """Items pulled by the API should be saved in database."""
        response = get_saved_posts(self.factory)
        