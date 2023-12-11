from rest_framework import serializers
from .models import Post, Comment, Author, Category, RepliedComment
from markdown import markdown as md

class CategorySerializer(serializers.ModelSerializer):
    num_of_posts_in_this_category = serializers.IntegerField(
        source='total_posts')

    class Meta:
        model = Category
        fields = ['name', 'num_of_posts_in_this_category', 'id']


class PostSerializer(serializers.ModelSerializer):
    # url = serializers.HyperlinkedIdentityField(view_name='post-detail')
    total_comments_on_this_post = serializers.SerializerMethodField()
    body = serializers.SerializerMethodField()
    category = serializers.StringRelatedField()
    author = serializers.StringRelatedField()

    class Meta:
        model = Post
        # fields = '__all__'
        exclude = ['status']

    def get_body(self, obj):
        return md(obj.body)
    
    def get_total_comments_on_this_post(self, obj):
        total_comments = obj.comments.count()
        total_replied_comments = obj.comments.filter(reply_comments__isnull=False).count()
        print(total_replied_comments, '-----------------------------')
        return total_comments + total_replied_comments

# send email ...
class PostshareSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=25)
    email = serializers.EmailField()
    to = serializers.EmailField()
    comments = serializers.CharField(required=False, max_length=1000, style={'base_template':'textarea.html'})  


class AuthorSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = Author
        # fields = '__all__'
        exclude = 'user',

    def get_full_name(self, obj):
        full_name = f"{obj.first_name} {obj.last_name}"
        return full_name


class CommentSerializer(serializers.ModelSerializer):
    total_replied_comments = serializers.SerializerMethodField()
    post = serializers.StringRelatedField()

    class Meta:
        model = Comment
        fields = '__all__'

    def get_total_replied_comments(self, obj):
        total_replies = obj.reply_comments.count()
        return total_replies

class RepliedCommentSerializer(serializers.ModelSerializer):
    comment = serializers.StringRelatedField()
    class Meta:
        model = RepliedComment
        fields = '__all__'


