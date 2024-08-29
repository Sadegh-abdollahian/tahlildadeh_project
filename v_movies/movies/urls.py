from django.urls import path, re_path
from .views import films_list, movie_detail

app_name = "movies"

urlpatterns = [
    path("", films_list, name="movie_list"),
    path("actor/<slug:actor_slug>/", films_list, name="actor_list"),
    re_path(r"^genre/(?P<genre_slug>[-\w]+)/", films_list, name="genre_list"),
    re_path(r"^movie/(?P<slug>[-\w]+)/$", movie_detail, name="movie_detail")
]
