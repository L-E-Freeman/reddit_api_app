from django.urls import path

from . import views

urlpatterns = [
    path('', views.get_top_level_comments, name='showcomments'),
]