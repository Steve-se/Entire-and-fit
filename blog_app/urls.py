from django.urls import path
from .views import PostList, PostDetail, category_list, CommentList, CommentDetail, \
author_of_a_post, latest_posts, popular_post, SimilarPost, RepliedCommentList, RepliedCommentDetailView 

from .feed import LatestPostsFeed
from .share_post_view import post_share
from .search_and_filter_views import post_search

app_name = 'blog_app'

urlpatterns = [
    path('posts/', PostList.as_view(), name='list_post'),
    path('posts/<slug:slug>/', PostDetail.as_view(), name='post-detail'),
    path('post/<slug:slug>/similar-posts/', SimilarPost.as_view(), name='similar_post'),
    path('post/<slug:slug>/share-post/', post_share, name='share3_post'),
    path('post/search/', post_search, name='post_search'),

    # Related to comments
    path('post/<slug:slug>/comments/', CommentList.as_view(), name='all_comments'),
    path('post/<slug:slug>/comments/<slug:comment_slug>/', CommentDetail.as_view(), name='comment-detail'),
    path('post/<slug:slug>/comments/<slug:comment_slug>/replied-comments/', RepliedCommentList.as_view(), name='all-replied-comments'), 
    path('post/<slug:slug>/comments/<slug:comment_slug>/replied-comments/<int:pk>/', RepliedCommentDetailView.as_view(), name='all-replied-comments'), 
    

    # the author of a post
    path('post/<slug:slug>/author/', author_of_a_post, name='author_view'),
    # path('author', AuthorListView.as_view(), name='author') ,

    path('category/', category_list, name='category_list'),

    #popular and latest post
    path('latest-posts/', latest_posts, name='latest_post'),
    path('popular-posts/', popular_post, name='popular_post'),

    path('feed/', LatestPostsFeed(), name='post_feed'),

]   
