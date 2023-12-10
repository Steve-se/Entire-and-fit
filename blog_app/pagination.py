from rest_framework.pagination import PageNumberPagination

class CommentPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'size'
    # max_page_size = 15

class RepliedCommentPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'size'
    # max_page_size = 15

class PostPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'size'
    # max_page_size = 15


    

