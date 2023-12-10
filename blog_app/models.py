from django.db import models 
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


''''
This application have these models
1. Author
2. Category
3. Post
4. Comment
---reply(ied) comments

'''

class Author(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(verbose_name=_("first name"), max_length=50)
    last_name = models.CharField(verbose_name=_("last name"), max_length=50)
    bio = models.TextField()
    pic = models.ImageField(verbose_name='profile picture', upload_to='images/', default='')
    twitter_handle = models.CharField(verbose_name=_("twitter handle"), max_length=20, blank=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    

class Category(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    total_posts = models.IntegerField(editable=False, verbose_name='num of posts in this category')

    @property
    def total_posts(self):
        return self.posts.filter(status='published').count()

    def __str__(self):
        return f"{self.name}"
    
    class Meta:
        verbose_name_plural = 'Categories'



class Post(models.Model):

    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
        )
    
    title = models.CharField(max_length=250)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts')
    slug = models.SlugField(max_length=250)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='blog_posts')
    body = models.TextField()
    image = models.ImageField(upload_to='images/')
    # thumbnail = models.ImageField(upload_to='images/')
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    class Meta:
        ordering = ('-publish',)
        # db_table = 'Big Steve'

    def __str__(self): 
        return self.title
    
    def get_absolute_url(self):
        return reverse('blog_app:post-detail', args=[str(self.slug)])
    

class BaseComment(models.Model): 
    
    name = models.CharField(max_length=80)
    # parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    email = models.EmailField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)
        abstract = True
    
    
class Comment(BaseComment):
    comment_body = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    comment_slug = models.SlugField(max_length=100)

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'

class RepliedComment(BaseComment):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='reply_comments')
    reply_comment_body = models.TextField()


