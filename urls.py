from django.contrib import admin
from django.urls import path, include
from . import views
from .views import *

urlpatterns = [
    path("test/", CreateDockerImage.as_view(), name="test"),
    path("my-api/", APICreaateDockerImage.as_view(), name="my_api"),
]
