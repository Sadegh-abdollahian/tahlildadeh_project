from django.contrib import admin
from .models import (
    Movie,
    SerieComments,
    MovieComments,
    Actor,
    Genre,
    Serie,
    SerieEpisode,
)


class MoviesActoresInline(admin.StackedInline):
    model = Movie.actors.through
    extra = 3


class MoviesGenresInline(admin.StackedInline):
    model = Movie.genres.through
    extra = 3


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ["full_name", "slug", "position"]
    prepopulated_fields = {"slug": ("full_name",)}


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ["title", "slug", "position"]
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "english_title",
        "year_of_manufacture",
        "slug",
        "country",
        "legal_age",
        "duraction",
        "score",
        "get_actors",
        "get_genres",
        "thumbnail",
        "trailer",
        "videofile",
        "is_perimium",
    )
    search_fields = ("title",)
    prepopulated_fields = {"slug": ("title",)}
    inlines = [MoviesActoresInline, MoviesGenresInline]


@admin.register(Serie)
class SerieAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "english_title",
        "year_of_manufacture",
        "slug",
        "is_perimium",
        "country",
        "legal_age",
        "score",
        "get_genres",
        "thumbnail",
        "trailer",
    )
    search_fields = ("title",)
    prepopulated_fields = {"slug": ("title",)}


@admin.register(SerieEpisode)
class SerieEpisodeAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "number_of_episode",
        "videofile",
        "download_link_480",
        "download_link_720",
        "download_link_1080",
        "season",
        "publish",
        "created_on",
        "updated",
    )


@admin.register(SerieComments)
class SerieCommentsAdmin(admin.ModelAdmin):
    list_display = ("name", "body", "serie", "created_on", "is_active")
    list_filter = ("is_active", "created_on")
    search_fields = ("name", "email", "body")
    actions = ["approve_comments"]

    def approve_comments(self, request, queryset):
        queryset.update(is_active=True)


@admin.register(MovieComments)
class MovieCommentsAdmin(admin.ModelAdmin):
    list_display = ("name", "body", "movie", "created_on", "is_active")
    list_filter = ("is_active", "created_on")
    search_fields = ("name", "email", "body")
    actions = ["approve_comments"]

    def approve_comments(self, request, queryset):
        queryset.update(is_active=True)
