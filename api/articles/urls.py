from django.urls import path, include
from . import views

urlpatterns = [
    path('api/articles', views.ArticleListCreate.as_view(), name='article-list-create'),
    path('api/articles/<str:slug>', views.ArticleRetrieve.as_view(), name='article-retrieve'),

    path('api/articles/<str:slug>/comments', views.CommentListCreate.as_view(), name='comment-list-create'),
]
