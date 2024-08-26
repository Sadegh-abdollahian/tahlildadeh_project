from django.shortcuts import render, get_object_or_404
from .models import Film, Actor, Genre
from taggit.models import Tag


# Create your views here.
def movie_list(request, actor_slug=None, tag_slug=None, genre_slug=None, **kwargs):
    movies = Film.objects.all()
    if actor_slug:
        actor = get_object_or_404(Actor, slug=actor_slug)
        movies = movies.filter(actors=actor)

    if genre_slug:
        genre = get_object_or_404(Genre, slug=genre_slug)
        movies = movies.filter(genres=genre)

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        movies = movies.filter(tags=tag)

    return render(request, "movies/index.html", {"movies": movies})


def movie_detail(request, slug):
    movie = get_object_or_404(Film, slug=slug)

    return render(request, "movies/single.html", {"movie": movie})
