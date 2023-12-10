from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from .serializers import PostSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Post

@api_view(['GET'])
def post_search(request):
    query = None
    results = []

    # Use request.GET instead of request.data for query parameters
    if 'query' in request.GET:
            query = request.GET['query']
            # Annotate and filter the queryset for search
            search_vector = SearchVector('title', 'body')
            search_query = SearchQuery(query)
            results = Post.objects.annotate(
                search = search_vector,
                rank = SearchRank(search_vector, search_query)
            ).filter(search=search_query).order_by('rank')

            post_serializer = PostSerializer(results, many=True)
            return Response(post_serializer.data)
    else: #return empty response
          return Response(results)
    

# filter post by category


