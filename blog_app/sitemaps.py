from django.contrib.sitemaps import Sitemap
from .models import Post


class PostSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def item(self):
        return Post.objects.filter(status='published')

    def lastmod(self, obj):
        return obj.updated
