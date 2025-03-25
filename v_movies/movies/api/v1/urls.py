from django.urls import path, include
from .views import MovieViewset, GenreViewSet, ActorViewSet, SerieViewset
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"movies", MovieViewset)
router.register(r"genres", GenreViewSet)
router.register(r"actors", ActorViewSet)
router.register(r"series", SerieViewset)

urlpatterns = [
    path("", include(router.urls)),
]
