from .models import Post
from .serializers import PostshareSerializer
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view


@api_view(['POST'])
def post_share(request, slug, *args, **kwargs):
    post = Post.objects.get(slug=slug, status='published')

    sent = False

    if request.method == 'POST':
        serializer = PostshareSerializer(data=request.data)
        if serializer.is_valid():
            vd = serializer.validated_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{vd['name']} recommends you read {post.title}"
            message = f"Read {post.title} at {post_url}\n\n {vd['name']}\'s comments: {vd['comments']}"
            send_mail(subject, message, 'mrejembistephen@gmail.com', [vd['to']], fail_silently=False)
            
            sent = True

            detail = {
                'detail': 'Email sent successfully',
                'sent': sent
            }

            return Response(detail, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)