from rest_framework import serializers
from movies.models import Movie, Genre, Actor, Serie, SerieEpisode
from subscription.models import Subscriptions
from django.utils import timezone


class MoviesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = "__all__"
        lookup_field = "slug"
        extra_kwargs = {"url": {"lookup_field": "slug"}}

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get("request")
        user = request.user if request else None

        if not instance.is_perimium:
            # Non-premium movies are accessible to all users
            return representation

        if not user or not user.is_authenticated:
            # Remove video-related fields for anonymous users
            representation.pop("videofile", None)
            representation.pop("download_link_480", None)
            representation.pop("download_link_720", None)
            representation.pop("download_link_1080", None)
        elif not Subscriptions.objects.filter(
            user=user, subscription_end_timestamp__gte=timezone.now()
        ).exists():
            # Remove video-related fields for authenticated users without an active subscription
            representation.pop("videofile", None)
            representation.pop("download_link_480", None)
            representation.pop("download_link_720", None)
            representation.pop("download_link_1080", None)

        return representation


class SerialSerializer(serializers.ModelSerializer):

    class Meta:
        model = Serie
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get("request")
        user = request.user if request else None

        if not instance.is_perimium:
            # Non-premium series are accessible to all users
            return representation

        if not user or not user.is_authenticated:
            # Remove video-related fields for anonymous users
            representation.pop("serie", None)
        elif not Subscriptions.objects.filter(
            user=user, subscription_end_timestamp__gte=timezone.now()
        ).exists():
            # Remove video-related fields for authenticated users without an active subscription
            representation.pop("serie", None)

        return representation


class SerieEpisode(serializers.ModelSerializer):

    class Meta:
        model = SerieEpisode
        fields = "__all__"


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = "__all__"


class ActorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Actor
        fields = "__all__"
