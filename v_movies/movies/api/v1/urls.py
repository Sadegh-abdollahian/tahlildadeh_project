from django.urls import path, re_path, include
from .views import movies_list_api_view

urlpatterns = [
    path("movies/", movies_list_api_view, name="movies_list")
]
