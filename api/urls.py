from django.urls import path, include

urlpatterns = [
    path("", include('api.users.v1.urls')),
]
