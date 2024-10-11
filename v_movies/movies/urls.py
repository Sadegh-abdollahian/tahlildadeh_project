from django.urls import path, re_path, include
from .views import FilmsListView, movie_detail

app_name = "movies"

urlpatterns = [
    path("", FilmsListView.as_view(), name="movie_list"),
    path("actor/<slug:actor_slug>/", FilmsListView.as_view(), name="actor_list"),
    re_path(
        r"^genre/(?P<genre_slug>[-\w]+)/", FilmsListView.as_view(), name="genre_list"
    ),
    re_path(r"^movie/(?P<slug>[-\w]+)/$", movie_detail, name="movie_detail"),
    path("api/v1/", include("movies.api.v1.urls")),
]
