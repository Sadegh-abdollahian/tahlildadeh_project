from django.urls import path, re_path
from .views import (
    MoviesListApiView,
    MoviesListApiView,
    GenreDetailApiView,
    ActorDetailApiView,
    MovieDetailApiView
)

urlpatterns = [
    path("", MoviesListApiView.as_view(), name="movies"),
    path("genre/", GenreDetailApiView.as_view(), name="genres"),
    path("actor/", ActorDetailApiView.as_view(), name="actors"),
    re_path(
        r"^genre/(?P<genre_slug>[-\w]+)/",
        MoviesListApiView.as_view(),
        name="genre_list",
    ),
    re_path(
        r"^actor/(?P<actor_slug>[-\w]+)/",
        MoviesListApiView.as_view(),
        name="genre_list",
    ),
    re_path(
        r"^movie/(?P<slug>[-\w]+)/$", MovieDetailApiView.as_view(), name="movie_detail"
    ),
]
