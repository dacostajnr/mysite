# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render,get_object_or_404
from django.core.urlresolvers import reverse
from .models import Post,Comment
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.core.mail import send_mail
from django.db.models import Count
from django.db.models import Q

#----------------[Forms]------------------------------------------------
from .forms import EmailPostForm,CommentForm
#from .forms import CommentForm

#--------------------------------------------------------------------
#Using class based views
# from django.views.generic import ListView
# class PostListView(ListView):
# 	queryset=Post.published.all()
# 	context_object_name='posts'
# 	paginate_by=2
# 	template_name='blog/post/list.html'

#--------------[Taggit]------------------------------------------------
from taggit.models import Tag


#-----------------------------------------------------------------------

# Create your views here.


def post_list(request,tag_slug=None):# tag_slug=None because we dont filter by tags by defautl
	object_list=Post.published.all()
	tag=None
	if tag_slug:
		tag=get_object_or_404(Tag,slug=tag_slug)
		object_list=object_list.filter(tags__in=[tag])
		
	paginator=Paginator(object_list,3) # 2 posts per page
	page=request.GET.get('page')
	try:
		posts=paginator.page(page)
	except PageNotAnInteger:
		#If page is not an integer deliver the first page
		posts=paginator.page(1)
	except EmptyPage:
		#If page is out of range,deliver the first page
		posts=paginator.page(paginator.num_pages)

	#---------------------Querying a search box-------------------------------------------------
	query=request.GET.get('q')
	if query:
		searcher='true'
		no_results=False
		object_list=object_list.filter(Q(body__icontains=query)|Q(title__icontains=query)).distinct()
		#object_list=object_list.filter(Q(body__icontains=query)&Q(title__icontains=query)).distinct()
		number=len(object_list) #Number of search results
		if number==0:
			no_results=True
		paginator=Paginator(object_list,3) # 2 posts per page
		page=request.GET.get('page')
		try:
			posts=paginator.page(page)
		except PageNotAnInteger:
			#If page is not an integer deliver the first page
			posts=paginator.page(1)
		except EmptyPage:
			#If page is out of range,deliver the first page
			posts=paginator.page(paginator.num_pages)
		return render(request,'blog/post/list.html',{'posts':posts,'no_results':no_results,'number':number,'searcher':searcher})
	return render(request,'blog/post/list.html',{'page':page,'posts':posts,'tag':tag})

def post_detail(request,year,month,day,post):
	post=get_object_or_404(Post,slug=post,status='published',
						   publish__year=year,
						   publish__month=month,
						   publish__day=day)
	#List of active comments for this post
	comments=post.comments.filter(active=True)
	if request.method=='POST':
		#A comment was posted
		comment_form = CommentForm(data=request.POST)
		if comment_form.is_valid:
			#Create Comment object but dont save to database yet  -->1.Save form 2.Assign form to post's comment  3.save comment
			new_comment = comment_form.save(commit=False)#he save() method is available for ModelForm but not for Form instances
			#Assign the current post to the comment
			new_comment.post = post
			#Save the comment to the database
			new_comment.save()
	else:
		comment_form=CommentForm()
	post_tags_ids=post.tags.values_list('id',flat=True) # [1,2,3,4] -->ids of tags of post
	similar_posts=Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
	similar_posts=similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','publish')[:4]
	return render(request,'blog/post/detail.html',{'post':post,'comments':comments,'comment_form':comment_form,'similar_posts':similar_posts})


def post_share(request,post_id): #Same view used to display form and also process submitted data
	#Retrieve post by id
	post=get_object_or_404(Post,id=post_id,status='published')
	sent=False
	cd=''

	if request.method=='POST':
		#Form was submitted
		form=EmailPostForm(request.POST)
		if form.is_valid():
			#Form fields passed validation
			cd=form.cleaned_data  # cd ={'name':'dacosta' , 'email':'hack@gmail.com' , 'to':'code.gmail.com' , 'comment':'nice'}
			#... send email
			post_url=request.build_absolute_uri(post.get_absolute_url())

			# Dacosta (slimtrissly@gmail.com) recommends you reading "my first post"
			subject='{} ({}) recommends you reading "{}"'.format(cd['name'],
																 cd['email'],
																 post.title)
			#'Read "my first post" at 127.0.0.1/blog/my-first-post-2017-09-21'
			#'Dacosta's comments: nice post '


			message='Read "{}" at {}\n\n{}\'s comments: {} '.format(post.title,
																	post_url,
																	cd['name'],
																	cd['comments'])
			send_mail(subject,message,'admin@myblog',[cd['to']])
			sent=True
	else:
		form=EmailPostForm()
	return render(request,'blog/post/share.html',{'post':post,'form':form,'sent':sent,'cd':cd})



















