#urls for APP VIDEO COLLECTION/URLS.PY

from django.urls import path
from .import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add', views.add, name='add_video'),
    path('video_list', views.video_list, name='video_list')
]