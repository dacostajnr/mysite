from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from .models import Post
class LatestPostsFeed(Feed):
	title = 'My blog'
	link  = '/blog/'
	description = 'New posts of my blog'

	def items(self):  #This method retrieves the objects to be included in the feed
		return Post.published.all()[:5]

	def item_title(self,item):
		return item.title
	def item_description(self,item):  #Build the descrption of the blog post with the first 30 words
		return truncatewords(item.body,30)