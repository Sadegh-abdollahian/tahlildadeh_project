from rest_framework import serializers
from movies.models import Movie, Genre, Actor


class MoviesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = "__all__"


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = "__all__"


class ActorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Actor
        fields = "__all__"
