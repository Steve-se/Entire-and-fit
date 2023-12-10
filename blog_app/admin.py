from django.contrib import admin
from .models import Post, Comment, Author, Category, RepliedComment


admin.site.site_header = "Entire and Fit"
admin.site.site_title = " Entire and Fit"
# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'total_posts')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author','category', 'status', 'publish', )
    list_filter = ('status', 'created', 'publish', 'author')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')

    def category(self, obj):
        return obj.category


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', )
    prepopulated_fields = {'comment_slug': ('comment_body',)}


@admin.register(RepliedComment)
class RepliedCommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created', 'active', 'comment')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email',)
    

admin.site.register(Author)
