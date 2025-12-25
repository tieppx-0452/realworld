from django.urls import path, include
from . import views

urlpatterns = [
    path('api/articles', views.ArticleListCreate.as_view(), name='article-list-create'),
    path('api/articles/<str:slug>', views.ArticleRetrieve.as_view(), name='article-retrieve'),

    path('api/articles/<str:slug>/comments', views.CommentListCreate.as_view(), name='comment-list-create'),
    path('api/articles/<str:slug>/comments/<int:id>', views.CommentRetrieve.as_view(), name='comment-retrieve'),

    path('api/tags', views.TagList.as_view(), name='tag-list'),
    path('api/articles/<str:slug>/favorite', views.ArticleFavorite.as_view(), name='article-favorite'),
    path('api/articles/feed', views.FeedArticleList.as_view(), name='feed-article-list'),
]
