from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.request import Request
from rest_framework.response import Response
from movies.models import Movie, Genre, Actor
from taggit.models import Tag
from .serializers import MoviesSerializer, GenreSerializer, ActorSerializer


class MoviesListApiView(generics.ListCreateAPIView):
    def get_queryset(self):
        movies = Movie.objects.all()
        actor_slug = self.kwargs.get("actor_slug")
        genre_slug = self.kwargs.get("genre_slug")
        tag_slug = self.kwargs.get("tag_slug")

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

    serializer_class = MoviesSerializer


class MovieDetailApiView(generics.ListAPIView):
    def get_queryset(self):
        movies = Movie.objects.all()
        slug = self.kwargs.get("slug")

        if slug:
            movies = movies.filter(slug=slug)

        return movies

    serializer_class = MoviesSerializer
    permission_classes = []


class PremiumMovieDetailApiView(generics.ListAPIView):
    pass

class GenreDetailApiView(generics.ListCreateAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class ActorDetailApiView(generics.ListCreateAPIView):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer
