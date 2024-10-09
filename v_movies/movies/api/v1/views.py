from django.views.generic import ListView
from movies.models import Movie, Actor, Genre
from django.shortcuts import get_object_or_404
from .serializers import MoviesSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

# class FilmsListView(ListView):
#     model = Movie

#     def get_queryset(self):
#         movies = Movie.objects.all()
#         actor_slug = self.kwargs.get('actor_slug')
#         genre_slug = self.kwargs.get('genre_slug') 
#         tag_slug = self.kwargs.get('tag_slug')

#         if actor_slug:
#             actor = get_object_or_404(Actor, slug=actor_slug)
#             movies = movies.filter(actors=actor)

#         if genre_slug:
#             genre = get_object_or_404(Genre, slug=genre_slug)
#             movies = movies.filter(genres=genre)

#         if tag_slug:
#             tag = get_object_or_404(Tag, slug=tag_slug)
#             movies = movies.filter(tags=tag)

#         return movies

@api_view(["get", "post"])
def movies_list_api_view(request):
    if request.method == "GET":
        movies = Movie.objects.all()
        serialiaser = MoviesSerializer(movies, many=True)
        return Response(serialiaser.data, status=status.HTTP_200_OK)
    else:
        serialiaser = MoviesSerializer(data=request.data)
        if serialiaser.is_valid():
            serialiaser.save()
            return Response(serialiaser.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serialiaser.errors, status=status.HTTP_400_BAD_REQUEST)
