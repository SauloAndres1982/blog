from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions


from .models import Post
from .serializers import PostSerializer
from .pagination import SmallSetPagination, LargeSetPagination, MediumSetPagination

class BlogListView(APIView):
    def get(self, request, format=None):
        if Post.postObjects.all().exists():

            posts = Post.postObjects.all()
            paginator = SmallSetPagination()
            results = paginator.paginate_queryset(posts, request)
            serializer = PostSerializer(results, many=True)

            return paginator.get_paginated_response({'posts':serializer.data})
        
        else:
            Response({"error": "No posts found"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    

class PostDetailView(APIView):
    def get(self, request, post_slug,format=None):
        post = get_object_or_404(Post, slug=post_slug)
        serializer = PostSerializer(post)
        return Response({'post':serializer.data}, status=status.HTTP_200_OK)
