from django.urls import path

from . import views

urlpatterns = [
    path('', views.get_saved_posts, name='showposts'),
]