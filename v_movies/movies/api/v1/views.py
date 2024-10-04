from django.views.generic import ListView
from movies.models import Movie, Actor, Genre
from django.shortcuts import get_object_or_404

class FilmsListView(ListView):
    model = Movie
    template_name = "movies/index.html"
    context_object_name = 'movies'

    def get_queryset(self):
        movies = Movie.objects.all()
        actor_slug = self.kwargs.get('actor_slug')
        genre_slug = self.kwargs.get('genre_slug') 
        tag_slug = self.kwargs.get('tag_slug')

        if actor_slug:
            actor = get_object_or_404(Actor, slug=actor_slug)
            movies = movies.filter(actors=actor)

        if genre_slug:
            genre = get_object_or_404(Genre, slug=genre_slug)
            movies = movies.filter(genres=genre)

        if tag_slug:
            tag = get_object_or_404(Tag, slug=tag_slug)
            movies = movies.filter(tags=tag)

        return movies
