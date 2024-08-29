from django.contrib import admin
from .models import Movie, SerialComments, MovieComments, Actor, Genre, Serial, SerialEpisode

# Register your models here.

admin.site.register(Actor)

admin.site.register(Genre)


@admin.register(Movie)
class PostAdmin(admin.ModelAdmin):
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
        "story",
        "about_movie",
        "thumbnail",
        "trailer",
        "videofile",
        "is_perimium",
        "download_link_480",
        "download_link_720",
        "download_link_1080",
    )
    search_fields = ("title",)
    prepopulated_fields = {"slug": ("title",)}

@admin.register(Serial)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "english_title",
        "year_of_manufacture",
        "slug",
        "country",
        "legal_age",
        "score",
        "get_actors",
        "get_genres",
        "story",
        "about_movie",
        "thumbnail",
        "trailer",
        "is_perimium",
    )
    search_fields = ("title",)
    prepopulated_fields = {"slug": ("title",)}

@admin.register(SerialEpisode)
class SerialEpisodeAdmin(admin.ModelAdmin):
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
        "serial",
    )


@admin.register(SerialComments)
class SerialCommentsAdmin(admin.ModelAdmin):
    list_display = ("name", "body", "movie", "created_on", "active")
    list_filter = ("active", "created_on")
    search_fields = ("name", "email", "body")
    actions = ["approve_comments"]

    def approve_comments(self, request, queryset):
        queryset.update(active=True)

@admin.register(MovieComments)
class MovieCommentsAdmin(admin.ModelAdmin):
    list_display = ("name", "body", "movie", "created_on", "active")
    list_filter = ("active", "created_on")
    search_fields = ("name", "email", "body")
    actions = ["approve_comments"]

    def approve_comments(self, request, queryset):
        queryset.update(active=True)
