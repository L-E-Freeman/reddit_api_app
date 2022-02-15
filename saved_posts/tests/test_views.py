from django.test import TestCase
from django.test import RequestFactory
from django.urls import reverse
from reddit_api_app.settings import get_secret
from saved_posts.views import authenticate_api, get_saved_posts

from unittest import mock
import praw
import json
import os
from pathlib import Path

class APIAuthenticationTests(TestCase):
    """Tests for PRAW authentication."""

    def setUp(self):
        self.factory = RequestFactory()

    def test_api_authenticated(self):
        """If API is authenticated properly, response should return the
        Reddit username used to authenticate."""
        
        reddit = authenticate_api(self.factory)
        response = reddit.user.me()
    
        self.assertEqual(response, get_secret("REDDIT_USERNAME"))

class ViewTests(TestCase):
    """Tests for views."""
    
    def setUp(self): 
        self.factory = RequestFactory()

    def test_get_saved_posts(self):
        pass

    def test_store_saved_posts(self, mocked_function):
        pass
        


    
    
