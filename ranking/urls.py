from django.urls import path
from .views import *

# 歌曲排行
urlpatterns = [
    path('', rankingView, name='ranking')
]