from django.urls import path
from .views import index, refresh_session

urlpatterns = [
    path('', index, name='index'),
    path('refresh_session/', refresh_session, name='refresh_session'),
]
