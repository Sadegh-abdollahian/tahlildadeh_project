from django.contrib import admin
from .models import Film, Comment, Actor, Genre

# Register your models here.

admin.site.register(Actor)

admin.site.register(Genre)


@admin.register(Film)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "english_name",
        "year_of_manufacture",
        "slug",
        "made_in",
        "legal_age",
        "film_time",
        "score",
        "get_actors",
        "get_genres",
        "story",
        "about_movie",
        "thumbnail",
        "trailer",
        "videofile",
    )
    search_fields = ("title",)
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("name", "body", "movie", "created_on", "active")
    list_filter = ("active", "created_on")
    search_fields = ("name", "email", "body")
    actions = ["approve_comments"]

    def approve_comments(self, request, queryset):
        queryset.update(active=True)
