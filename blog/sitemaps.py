from django.contrib.sitemaps import Sitemap
from .models import Post

class PostSitemap(Sitemap):
	changefreq='weekly'
	priority=0.9   #maximum is 1
	def items(self): #This method returns the queryset of objects to include in the sitemap
		return Post.published.all()   #By default,django calls the get_absolute url of the object to retrieve its url
	def lastmod(self,obj):
		return obj.publish


	