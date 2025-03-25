from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from movies.models import Movie, Genre, Actor, Serie
from subscription.models import Subscriptions
from .serializers import (
    MoviesSerializer,
    GenreSerializer,
    ActorSerializer,
    SerialSerializer,
    SerieEpisode,
)
from rest_framework.response import Response
from django.utils import timezone
from rest_framework.throttling import UserRateThrottle
from .permissions import IsAdminUserOrReadOnly


class MovieViewset(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MoviesSerializer
    throttle_classes = [UserRateThrottle]
    permission_classes = [IsAdminUserOrReadOnly]
    lookup_field = "slug"

    def get_object(self):
        """
        Custom method to retrieve a Movie object using a slug
        """
        slug = self.kwargs.get("slug")
        queryset = self.filter_queryset(self.get_queryset())
        obj = get_object_or_404(queryset, slug__iexact=slug)
        user = self.request.user
        # Allow access to non-premium movies for all users (authenticated and anonymous)
        if not obj.is_perimium:
            return obj

        # For premium movies, check if the user is authenticated
        if not user.is_authenticated:
            raise PermissionDenied("You must be logged in to access premium content.")

        # Check if the authenticated user has an active subscription
        if not Subscriptions.objects.filter(
            user=user, subscription_end_timestamp__gte=timezone.now()
        ).exists():
            raise PermissionDenied("You do not have an active subscription.")

        return obj

    @action(detail=True, methods=["get"])
    def actors(self, request, slug=None):
        """
        Custom method to retrieve actors of a specific movie
        """
        movie = self.get_object()
        actors = movie.actors.all()
        serializer = ActorSerializer(actors, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def genres(self, request, slug=None):
        movie = self.get_object()
        genres = movie.genres.all()
        serializer = GenreSerializer(genres, many=True)
        return Response(serializer.data)


class SerieViewset(viewsets.ModelViewSet):
    queryset = Serie.objects.all()
    serializer_class = SerialSerializer
    permission_classes = [IsAdminUserOrReadOnly]
    lookup_field = "slug"

    def get_object(self):
        """
        Custom method to retrieve a Movie object using a slug
        """
        slug = self.kwargs.get("slug")
        queryset = self.filter_queryset(self.get_queryset())
        obj = get_object_or_404(queryset, slug__iexact=slug)
        user = self.request.user
        # Allow access to non-premium series for all users (authenticated and anonymous)
        if not obj.is_perimium:
            return obj

        # For premium movies, check if the user is authenticated
        if not user.is_authenticated:
            raise PermissionDenied("You must be logged in to access premium content.")

        # Check if the authenticated user has an active subscription
        if not Subscriptions.objects.filter(
            user=user, subscription_end_timestamp__gte=timezone.now()
        ).exists():
            raise PermissionDenied("You do not have an active subscription.")

        return obj

    @action(detail=True, methods=["get"])
    def actors(self, request, slug=None):
        """
        Custom method to retrieve actors of a specific movie
        """
        serie = self.get_object()
        actors = serie.actors.all()
        serializer = ActorSerializer(actors, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def genres(self, request, slug=None):
        serie = self.get_object()
        genres = serie.genres.all()
        serializer = GenreSerializer(genres, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def serie_episodes(self, request, slug=None):
        serie = self.get_object()
        episodes = serie.serie.all()
        serializer = SerieEpisode(episodes, many=True)
        return Response(serializer.data)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = []


class ActorViewSet(viewsets.ModelViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer
    permission_classes = []
