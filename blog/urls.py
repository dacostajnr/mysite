from django.conf.urls import url
from . import views
from .feeds import LatestPostsFeed

urlpatterns=[

		#---------------------------------------
		#Using class based views
		#url(r'^$',views.PostListView.as_view(),name='post_list'),

		#---------------------------------------


		#/blog/
		url(r'^$',views.post_list,name='post_list'),
	
		#/blog/2017/09/21/my-first-post
		 url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<post>[-\w]+)/$',views.post_detail,name='post_detail'),

		 #/blog/1/share
		 url(r'^(?P<post_id>\d+)/share/$',views.post_share,name='post_share'),

		 #/blog/tag/jazz
		 url(r'^tag/(?P<tag_slug>[-\w]+)/$',views.post_list,name='post_list_by_tag'),

		 #/blog/feed
		 url(r'^feed/$',LatestPostsFeed(),name='post_feed'),
			
]