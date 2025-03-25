from django.urls import path, re_path, include

app_name = "movies"

urlpatterns = [
    path("api/v1/", include("movies.api.v1.urls")),
]
