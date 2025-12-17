from django.urls import path, include
from . import views

urlpatterns = [
    path('api/articles', views.ArticleListCreate.as_view(), name='article'),
]
