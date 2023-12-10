from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from rest_framework.decorators import api_view

from .serializers import PostSerializer, CommentSerializer, AuthorSerializer, CategorySerializer, RepliedCommentSerializer
from django.db.models import Count, Subquery, OuterRef
from .models import Post, Comment, Author, Category, RepliedComment
from rest_framework.generics import GenericAPIView
from rest_framework.generics import get_object_or_404
from .pagination import PostPagination, CommentPagination, RepliedCommentPagination
# from django.shortcuts import get_list_or_404

# Create your views here.


@api_view(["GET"])
def author_of_a_post(request, slug, format=None):
    if request.method == "GET":
        post = Post.objects.get(slug=slug)
        author = post.author
        serializer = AuthorSerializer(author)
        return Response(serializer.data)


class CommentList(GenericAPIView):
    serializer_class = CommentSerializer
    pagination_class = CommentPagination

    """
    This view should list all the comments attached to a particular post
    And also provide check in a way that a user cannot comment twice in a single
    post.
    """
    
    def get_queryset(self):
        return Comment.objects.all()

    def get(self, request, slug, format=None):
        try:
            post = Post.objects.get(slug=slug)
        except Post.DoesNotExist:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

        comments = self.get_queryset().filter(post=post, active=True)
        # paginate the queryset
        page = self.paginate_queryset(comments)
        if page is not None:
            p = page
        else:
            p = comments
        serializer = self.serializer_class(p, many=True)
        return self.get_paginated_response(serializer.data) if page is not None else  Response(serializer.data)

    def post(self, request, slug, format=None):
        """
        A user shouldn't be able to able to add comment twice.
        """
        try:
            post = Post.objects.get(slug=slug)
        except Post.DoesNotExist:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():

            # Run checks
            vd = serializer.validated_data
            email = vd['email']
            name = vd['name']
            comment_body = vd['comment_body']

            if self.get_queryset().filter(email=email, name=name, comment_body=comment_body, post=post).exists():
                return Response({"error": "you already added a comment"})

            serializer.save(post=post)
            message = "Comment successfully added!"
            context = {
                'data': serializer.data,
                'message': message
            }
            return Response(context, status=status.HTTP_201_CREATED)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentDetail(APIView):
    def get_object(self, comment_slug):
        try:
            return Comment.objects.get(comment_slug=comment_slug)
        except Comment.DoesNotExist:
            return Http404

    def get(self, request, comment_slug, slug, format=None):
        post = Post.objects.get(slug=slug)
        comment = self.get_object(comment_slug=comment_slug)

        # check if the comment belongs to the specified post
        if comment.post != post:
            raise Http404
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    def put(self, request, slug, comment_slug, format=None):
        post = Post.objects.get(slug=slug, status='published')
        comment = get_object_or_404(
            Comment, post=post, comment_slug=comment_slug, active=True)
        serializer = CommentSerializer(comment, data=request.data)

        # Check if the person trying to update the comment is the same person that posted it
        if (
            request.data.get('email') != comment.email
            or request.data.get('name') != comment.name
        ):
            return Response({'error': 'Only owners of the comment can update it'}, status=status.HTTP_403_FORBIDDEN)
        if serializer.is_valid():

            serializer.save()
            message = "comment successfully updated"
            context = {
                'data': serializer.data,
                'message': message
            }
            return Response(context, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, slug, comment_slug):
        # if request.user.is_staff:
        post = Post.objects.get(slug=slug)
        comment = get_object_or_404(
            Comment, comment_slug=comment_slug, post=post)
        comment.delete()
        data = {
            'message': " DELETED !"
        }
        return Response(data, status=status.HTTP_204_NO_CONTENT)


class RepliedCommentList(GenericAPIView):
    serializer_class = RepliedCommentSerializer
    pagination_class = RepliedCommentPagination

    def get_queryset(self):
        return RepliedComment.objects.all()

    def get(self, request, comment_slug,  slug,  format=None):
        """
        get the comment by "id" and list all the replied comments under it
        """
        try:
            post = Post.objects.get(slug=slug, status='published')
            comment = get_object_or_404(
                Comment, comment_slug=comment_slug, post=post, active=True)
        except Comment.DoesNotExist:
            return Response({'error': 'comment does not exist'}, status=status.HTTP_404_NOT_FOUND)

        all_replied_comments = self.get_queryset().filter(comment=comment, active=True)
        page = self.paginate_queryset(all_replied_comments)
        if page is not None:
            p = page
        else: 
            p = all_replied_comments
        serializer = self.serializer_class(p, many=True)
        return self.get_paginated_response(serializer.data) if page is not None else Response(serializer.data)

    def post(self, request,  slug, comment_slug, *args, format=None, **kwargs):
        """
        get a comment, and reply under it
        """
        try:
            post = Post.objects.get(slug=slug, status='published')
            comment = get_object_or_404(
                Comment, comment_slug=comment_slug, post=post, active=True)
        except Comment.DoesNotExist:
            return Response({'error': 'comment does not exist'}, status=status.HTTP_404_NOT_FOUND)

        serializer = RepliedCommentSerializer(data=request.data)
        if serializer.is_valid():

            # Check if commenter is trying to duplicate his comment
            vd = serializer.validated_data
            email = vd['email']
            name = vd['name']
            reply_comment_body = vd['reply_comment_body']
            if self.get_queryset().filter(email=email, name=name, reply_comment_body=reply_comment_body, comment=comment).exists():
                return Response({"error": "you already added a comment"})
            serializer.save(comment=comment)
            message = "Comment successfully added !"

            j_data = {
                'data': serializer.data,
                'message': message
            }
            return Response(j_data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RepliedCommentDetailView(APIView):

    def get_object(self, pk):
        try:
            replied_comment = get_object_or_404(
                RepliedComment, pk=pk, active=True)
            return replied_comment
        except RepliedComment.DoesNotExist:
            return Http404

    def get(self, request, pk, slug, comment_slug):
        post = get_object_or_404(Post, slug=slug, status='published')
        comment = get_object_or_404(
            Comment, post=post, active=True, comment_slug=comment_slug)
        
        replied_comment = self.get_object(pk=pk)
        if comment.post != post or replied_comment.comment != comment:
            raise Http404

        serializer = RepliedCommentSerializer(replied_comment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, slug, comment_slug, *args, **kwargs):
        post = Post.objects.get(slug=slug, status='published')
        comment = get_object_or_404(Comment, post=post, comment_slug=comment_slug, active=True)

        reply_comment = get_object_or_404(RepliedComment, pk=pk, comment=comment)
        serializer = RepliedCommentSerializer(reply_comment, data=request.data)

        # Check if the person trying to update the comment is the same person that posted it
        if (
            request.data.get('email') != reply_comment.email
            or request.data.get('name') != reply_comment.name
        ):
            return Response({'error': 'Only owners of the comment can update it'}, status=status.HTTP_403_FORBIDDEN)
        if serializer.is_valid():
            serializer.save()

            message = "comment successfully updated"
            context = {
                'data': serializer.data,
                'message': message
            }
            return Response(context, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, slug, comment_slug):
        post = Post.objects.get(slug=slug)
        comment = get_object_or_404(Comment, comment_slug=comment_slug, post=post)
        reply_comment = get_object_or_404(RepliedComment, pk=pk, comment=comment)
        reply_comment.delete()
        data = {
            'message': " DELETED !"
        }
        return Response(data, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def category_list(request, format=None):
    if request.method == 'GET':
        category = Category.objects.all()
        serializer = CategorySerializer(category, many=True)
        return Response(serializer.data)


class PostList(GenericAPIView):
    """
    if filter by category, else return all the post queryset
    """
    serializer_class = PostSerializer
    pagination_class = PostPagination

    def get_queryset(self):
        return Post.objects.filter(status='published')

    def get(self, request, *args, format=None, **kwargs):
        queryset = self.get_queryset()
        category = request.GET.get('category')

        # Filter the queryset based on the category before pagination
        if category:
            queryset = queryset.filter(category__name=category)

        # Paginate the queryset
        page = self.paginate_queryset(queryset)

        if page is not None:
            posts = page
        else:
            posts= queryset
        serializer = self.serializer_class(posts, many=True)
        return self.get_paginated_response(serializer.data) if page is not None else Response(serializer.data)

class PostDetail(APIView):

    def get_object(self, slug):
        try:
            return Post.objects.get(slug=slug, status='published')
        except Post.DoesNotExist():
            return Http404

    def get(self, request, slug, format=None):
        post = self.get_object(slug=slug)
        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
def latest_posts(request, count=3, format=None):
    """
    get all the posts (not more than five posts) that are recently
    published and return it to the user
    """
    if request.method == 'GET':
        posts = Post.objects.filter(
            status='published').order_by('-publish')[:count]
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)


@api_view(["GET"]) 
def popular_post(request, count=3, format=None):
    """
    return all the published posts that have the most comments
    """

    if request.method == "GET":
        posts = Post.objects.filter(status='published').annotate(
            total_comments=Count('comments')).order_by('-total_comments')[:count]
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SimilarPost(APIView):
    def get(self, request, slug, format=None):
        try:
            post = Post.objects.get(slug=slug, status='published')
        except Post.DoesNotExist:
            return Response({"error": "Post not found"}, status=404)

        # put all the items/queryset's title in a list
        a = post.title
        a_list = a.split()

        # Accumulate similar posts in a list
        similar_posts_list = []
        unique_list = []

        for item in a_list:

            # Filter similar posts based on the title (Case - insensitive)
            similar_posts = Post.objects.filter(
                title__icontains=item,
                category=post.category
            ).exclude(slug=post.slug)[:4]

            similar_posts_list.extend(similar_posts)

        for items in similar_posts_list:
            if items not in unique_list:
                unique_list.append(items)

        serializer = PostSerializer(unique_list, many=True)
        return Response(serializer.data)
