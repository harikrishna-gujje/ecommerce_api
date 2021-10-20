from django.urls import path
from .views import SimpleApi

urlpatterns = [
    path('', SimpleApi.as_view(), name='home')
]