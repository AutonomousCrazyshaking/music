from django.urls import path
from .views import *


urlpatterns = [
    path('<int:id>.html', playView, name='play'),
    path('download/<int:id>.html', downloadView, name='download')
]