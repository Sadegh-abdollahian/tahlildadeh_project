from django.urls import path, include

app_name = "subscription"

urlpatterns = [path("api/v1/", include("subscription.api.v1.urls"))]
