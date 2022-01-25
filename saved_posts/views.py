from email import header
import requests
import os
import json
from pathlib import Path
import logging

from reddit_api_app.settings import get_secret

from django.shortcuts import render
from django.http import HttpResponse


logger = logging.getLogger("myLogger")
    
def authenticate(request):
    """Initializing authentication attributes"""
    # Getting base directory path
    BASE_DIR = Path(__file__).resolve().parent.parent

    # Joining correct file to base directory path and opening
    with open(os.path.join(BASE_DIR, 'secrets.json')) as secrets_file:
        secrets = json.load(secrets_file)

    auth = requests.auth.HTTPBasicAuth(
        get_secret("PERSONAL_USE_SCRIPT"), 
        get_secret("SECRET_TOKEN"))
    
    data = {
        'grant_type': 'password', 
        'username': get_secret("REDDIT_USERNAME"),
        'password': get_secret("REDDIT_PASSWORD")
    }

    headers = {'User-Agent':'SuggestBot:v1.0'}

    res = requests.post(
        'https://www.reddit.com/api/v1/access_token', 
        auth=auth, data=data, headers=headers)

    TOKEN = res.json()['access_token']
    
    # ** used for dictionary unpacking. Creates new dictionary and unpacks
    # all key value pairs into the new dictionary.
    headers = {**headers, **{'Authorization': f"bearer {TOKEN}"}}

    return headers

def show_data(request):
    headers = authenticate(request)

    res = requests.get(
        "https://oauth.reddit.com/r/python/hot",
        headers=headers)

    return render(
        request, 'saved_posts/show_data.html', 
        {'data': res.json()})

