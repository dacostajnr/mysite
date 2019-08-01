from django import template
register=template.Library()
from ..models import Post
from django.db.models import Count

from django.utils.safestring import mark_safe
import markdown

@register.simple_tag
def total_posts(): #we are defining a tag caled total_posts
    return Post.published.count()

#inclusion tags have to return a dictionary of values
#that is used as the context to render the specified template
@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts=Post.published.order_by('-publish')[:count]
    return {'latest_posts':latest_posts}


@register.assignment_tag
def get_most_commented_posts(count=1):
	return Post.published.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]

@register.filter(name='markdown')
def markdown_format(text):
	return mark_safe(markdown.markdown(text))