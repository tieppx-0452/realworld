from rest_framework import filters

class FilterArticle(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        tag_query = request.GET.get('tag', None)
        author_query = request.GET.get('author', None)
        favorited_by_query = request.GET.get('favorited', None)
        if tag_query is not None:
            queryset = queryset.filter(article_tags__tag__name=tag_query)
        if author_query is not None:
            queryset = queryset.filter(author__username=author_query)
        if favorited_by_query is not None:
            queryset = queryset.filter(favorited_by__username=favorited_by_query)
        return queryset.distinct()
