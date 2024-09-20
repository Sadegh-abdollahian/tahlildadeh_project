from django.shortcuts import render, get_object_or_404
from .models import Movie, Actor, Genre
from .forms import MovieCommentsForm, SerialCommentsForm
from taggit.models import Tag
from django.db.models import Count
from django.views import View
from django.views.generic import ListView
from .mixins import LoginRequiredMixin

# Views
class FilmsListView(LoginRequiredMixin ,ListView):
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


def movie_detail(request, slug):
    # model = Movie
    # template_name = "movies/index.html"
    # context_object_name = 'movies'

    movie = get_object_or_404(Movie, slug=slug)

    comments = movie.comments.filter(active=True)
    new_comment = None  # Comment posted
    if request.method == "POST":
        movie_comment_form = MovieCommentsForm(data=request.POST)
        if movie_comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = movie_comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.movie = movie
            # Save the comment to the database
            new_comment.save()
    else:
        movie_comment_form = MovieCommentsForm()
    tags = movie.tags.all()
    movie_tags_id = movie.tags.values_list("id", flat=True)
    similar_movies = Movie.objects.filter(tags__in=movie_tags_id).exclude(id=movie.id)
    similar_movies = similar_movies.annotate(same_tags=Count("tags")).order_by(
        "-same_tags"
    )[:6]

    return render(
        request,
        "movies/single.html",
        {
            "movie": movie,
            "comments": comments,
            "new_comment": new_comment,
            "movie_comment_form": movie_comment_form,
            "similar_movies": similar_movies,
        },
    )

# Movie 
