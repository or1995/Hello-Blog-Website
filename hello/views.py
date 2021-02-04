from django.shortcuts import get_object_or_404, render, redirect
from django.core.paginator import Paginator
from django.http import Http404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse
from django.views import generic
from django.contrib.auth.models import User
from .models import Post, Category, Comment, Carousel, Reply
from users.models import Profile as ProfileModel
from datetime import date
from .forms import PostForm, CategoryForm, CommentForm, CarouselForm
from datetime import datetime,date


# Create your views here.
class IndexView(generic.ListView):
	model = Post
	template_name= 'hello/index.html'
	context_object_name = 'latestposts'
	paginate_by = 8

	def get_queryset(self):
		return Post.objects.order_by('-pub_date__year','-pub_date__month','-pub_date__day','-likes','-pub_date__hour','-pub_date__minute')

	def get_context_data(self, **kwargs):
		context = super(IndexView, self).get_context_data(**kwargs)
		context['carouselpages'] = Carousel.objects.all().order_by('id')
		return context


class FollowsView(generic.ListView):
	model = Post
	template_name= 'hello/follows.html'
	context_object_name = 'latestposts'
	paginate_by = 8

	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

	def get_queryset(self):
		return Post.objects.filter(author__profile__followers__user = User.objects.get(username=self.request.user)).order_by('-pub_date__year','-pub_date__month','-pub_date__day','-likes','-pub_date__hour','-pub_date__minute')


@login_required
def likepost(request, post_id):
	current_user = request.user
	currentpost = Post.objects.get(id=post_id)
	likes = Post.objects.filter(likedusers = current_user).filter(id=post_id).first()
	if likes:
		currentpost.likedusers.remove(current_user)
		currentpost.likes = currentpost.likes - 1
		currentpost.save()
		return redirect('index')
	else:
		currentpost.likedusers.add(current_user)
		currentpost.likes = currentpost.likes + 1
		currentpost.save()
		return redirect('index')


@login_required
def followprofile(request, profile_id):
	current_profile = ProfileModel.objects.get(user=request.user)
	followprofile = ProfileModel.objects.get(id=profile_id)
	if current_profile == followprofile:
		raise Http404 
	follow = ProfileModel.objects.filter(followers = current_profile).filter(id=profile_id).first()
	if follow:
		followprofile.followers.remove(current_profile)
		followprofile.save()
		return redirect('index')
	else:
		followprofile.followers.add(current_profile)
		followprofile.save()
		return redirect('index')


class Favposts(generic.ListView):
	paginate_by = 8
	model = Post
	template_name= 'hello/LikedPosts.html'
	context_object_name = 'likedposts'

	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

	#kwargs used to get the part of the url you type in the brackets in urls
	def get_queryset(self):
		return Post.objects.filter(likedusers = self.request.user)


@login_required
def likecomment(request, comment_id):
	current_user = request.user
	currentcomment = Comment.objects.get(id=comment_id)
	likes = Comment.objects.filter(likedusers = current_user).filter(id=comment_id).first()
	if likes:
		currentcomment.likedusers.remove(current_user)
		currentcomment.likes = currentcomment.likes - 1
		currentcomment.save()
		return redirect('index')
	else:
		currentcomment.likedusers.add(current_user)
		currentcomment.likes = currentcomment.likes + 1
		currentcomment.save()
		return redirect('index')


@login_required
def likereply(request, reply_id):
	current_user = request.user
	currentreply = Reply.objects.get(id=reply_id)
	likes = Reply.objects.filter(likedusers = current_user).filter(id=reply_id).first()
	if likes:
		currentreply.likedusers.remove(current_user)
		currentreply.likes = currentreply.likes - 1
		currentreply.save()
		return redirect('index')
	else:
		currentreply.likedusers.add(current_user)
		currentreply.likes = currentreply.likes + 1
		currentreply.save()
		return redirect('index')


def fullpost(request, post_id):

	thepost = Post.objects.get(pk=post_id)
	thecomments = Comment.objects.filter(article__id=post_id).order_by('-pub_date')
	thereplys = Reply.objects.filter(comment__article__id=post_id).order_by('-pub_date')

	if request.method == 'POST':
		# create a form instance and populate it with data from the request:
		form = CommentForm(request.POST)
		# check whether it's valid:
		if form.is_valid():
			# process the data in form.cleaned_data as required
			current_user = request.user
			ccontent = form.cleaned_data['content']
			c = Comment(author=current_user, article=thepost, content=ccontent)
			c.save()
			#form.save()
			# redirect to a new URL:
			return redirect(reverse('fullpost', kwargs={'post_id': post_id}))

		if 'reply' in request.POST:
			replyvalue = request.POST['reply']
			commentid = request.POST['commentid']

			current_user = request.user
			currentcomment = Comment.objects.get(pk=commentid)
			r = Reply(author=current_user, comment=currentcomment, content=replyvalue)
			r.save()

			return redirect(reverse('fullpost', kwargs={'post_id': post_id}))


	# if a GET (or any other method) we'll create a blank form
	else:
		form = CommentForm()

	return render(request, 'hello/postdetail.html', {'form': form, 'thepost': thepost, 'thecomments': thecomments, 'thereplys': thereplys})



class Fullcategory(generic.ListView):
	paginate_by = 8
	model = Post
	template_name= 'hello/category.html'
	context_object_name = 'categoryposts'

	#kwargs used to get the part of the url you type in the brackets in urls
	def get_queryset(self):
		return Post.objects.filter(category__title = self.kwargs['category_title']).order_by('-pub_date__year','-pub_date__month','-pub_date__day','-likes','-pub_date__hour','-pub_date__minute')
	
	def get_context_data(self, **kwargs):
		context = super(Fullcategory, self).get_context_data(**kwargs)
		context['currentcategory'] = Category.objects.get(title=self.kwargs['category_title'])
		return context


class Profile(generic.ListView):
	paginate_by = 8
	model = Post
	template_name= 'hello/profile.html'
	context_object_name = 'profileposts'

	#kwargs used to get the part of the url you type in the brackets in urls
	def get_queryset(self):
		return Post.objects.filter(author = self.kwargs['author_id']).order_by('-pub_date__year','-pub_date__month','-pub_date__day','-likes','-pub_date__hour','-pub_date__minute')

	def get_context_data(self, **kwargs):
		context = super(Profile, self).get_context_data(**kwargs)
		context['targeteduser'] = User.objects.get(id=self.kwargs['author_id'])
		context['followersnum'] = User.objects.get(id=self.kwargs['author_id']).profile.followers.all().count()
		likes = Post.objects.filter(author = self.kwargs['author_id'])
		likessum = 0
		for like in likes:
			likessum = likessum + like.likes
		context['likesnum'] = likessum
		return context


class MyProfile(generic.ListView):
	paginate_by = 8
	model = Post
	template_name= 'hello/myprofile.html'
	context_object_name = 'profileposts'

	#kwargs used to get the part of the url you type in the brackets in urls
	def get_queryset(self):
		return Post.objects.filter(author = self.request.user).order_by('-pub_date__year','-pub_date__month','-pub_date__day','-likes','-pub_date__hour','-pub_date__minute')

	def get_context_data(self, **kwargs):
		context = super(MyProfile, self).get_context_data(**kwargs)
		context['targeteduser'] = self.request.user
		context['targeteduser'] = User.objects.get(id=self.request.user.id)
		context['followersnum'] = User.objects.get(id=self.request.user.id).profile.followers.all().count()
		likes = Post.objects.filter(author = self.request.user.id)
		likessum = 0
		for like in likes:
			likessum = likessum + like.likes
		context['likesnum'] = likessum
		return context

		
@login_required
def create_post(request):
	# if this is a POST request we need to process the form data
	if request.method == 'POST':
		# create a form instance and populate it with data from the request:
		form = PostForm(request.POST, request.FILES)
		# check whether it's valid:
		if form.is_valid():
			# process the data in form.cleaned_data as required
			current_user = request.user
			ptitle = form.cleaned_data['title']
			pcontent = form.cleaned_data['content']
			pcategory = form.cleaned_data['category']
			pimage = form.cleaned_data['postimage']
			p = Post(title=ptitle, content=pcontent, pub_date=datetime.now(), author=current_user, category=pcategory, postimage=pimage)
			p.save()
			#form.save()
			# redirect to a new URL:
			return HttpResponseRedirect('/')

	# if a GET (or any other method) we'll create a blank form
	else:
		form = PostForm()

	return render(request, 'hello/createpost.html', {'form': form})

@login_required
def update_post(request, post_id):
	# ensure the user who made the post is the one editing it
	test = get_object_or_404(Post,pk=post_id)
	if test.author.id != request.user.id:
		raise Http404
	# if this is a POST request we need to process the form data
	if request.method == 'POST':
		# create a form instance and populate it with data from the request:
		form = PostForm(request.POST, request.FILES, instance=Post.objects.get(pk = post_id))
		# check whether it's valid:
		if form.is_valid():
			# process the data in form.cleaned_data as required
			current_user = request.user
			ptitle = form.cleaned_data['title']
			pcontent = form.cleaned_data['content']
			pcategory = form.cleaned_data['category']
			pimage = form.cleaned_data['postimage']
			p = Post.objects.get(pk = post_id)
			p.title = ptitle
			p.content = pcontent
			p.pub_date=datetime.now()
			p.author=current_user
			p.category=pcategory
			p.postimage=pimage
			p.save()
			# redirect to a new URL:
			return HttpResponseRedirect('/')

	# if a GET (or any other method) we'll create a blank form
	else:
		form = PostForm(instance=Post.objects.get(pk = post_id))

	return render(request, 'hello/editpost.html', {'form': form})

@staff_member_required
def add_category(request):
	if request.method == 'POST':
		# create a form instance and populate it with data from the request:
		form = CategoryForm(request.POST, request.FILES)
		# check whether it's valid:
		if form.is_valid():
			# process the data in form.cleaned_data as required
			ctitle = form.cleaned_data['title']
			cdescription = form.cleaned_data['description']
			cpimage = form.cleaned_data['profileimage']
			cbimage = form.cleaned_data['backgroundimage']
			p = Category(title=ctitle, description=cdescription, profileimage=cpimage, backgroundimage=cbimage)
			p.save()
			# redirect to a new URL:
			return HttpResponseRedirect('/')

	# if a GET (or any other method) we'll create a blank form
	else:
		form = CategoryForm()

	return render(request, 'hello/addcategory.html', {'form': form})

@staff_member_required
def edit_category(request, category_id):
	if request.method == 'POST':
		# create a form instance and populate it with data from the request:
		form = CategoryForm(request.POST, request.FILES, instance=Category.objects.get(pk = category_id))
		# check whether it's valid:
		if form.is_valid():
			# process the data in form.cleaned_data as required
			ctitle = form.cleaned_data['title']
			cdescription = form.cleaned_data['description']
			cpimage = form.cleaned_data['profileimage']
			cbimage = form.cleaned_data['backgroundimage']
			c = Category.objects.get(pk = category_id)
			c.title = ctitle
			c.description = cdescription
			c.profileimage = cpimage
			c.backgroundimage = cbimage
			c.save()
			# redirect to a new URL:
			return HttpResponseRedirect('/')

	# if a GET (or any other method) we'll create a blank form
	else:
		form = CategoryForm(instance=Category.objects.get(pk = category_id))

	return render(request, 'hello/editcategory.html', {'form': form})


@staff_member_required
def edit_carousel(request, carousel_id):
	if request.method == 'POST':
		# create a form instance and populate it with data from the request:
		form = CarouselForm(request.POST, request.FILES, instance=Carousel.objects.get(pk = carousel_id))
		# check whether it's valid:
		if form.is_valid():
			# process the data in form.cleaned_data as required
			cartitle = form.cleaned_data['title']
			cardescription = form.cleaned_data['description']
			carimage = form.cleaned_data['carouselimage']
			c = Carousel.objects.get(pk = carousel_id)
			c.title = cartitle
			c.description = cardescription
			c.carouselimage = carimage
			c.save()
			# redirect to a new URL:
			return HttpResponseRedirect('/')

	# if a GET (or any other method) we'll create a blank form
	else:
		form = CarouselForm(instance=Carousel.objects.get(pk = carousel_id))

	return render(request, 'hello/editcarousel.html', {'form': form})


@staff_member_required
def add_carousel(request):
	if request.method == 'POST':
		# create a form instance and populate it with data from the request:
		form = CarouselForm(request.POST, request.FILES)
		# check whether it's valid:
		if form.is_valid():
			# process the data in form.cleaned_data as required
			cartitle = form.cleaned_data['title']
			cardescription = form.cleaned_data['description']
			carimage = form.cleaned_data['carouselimage']
			p = Carousel(title=cartitle, description=cardescription, carouselimage=carimage)
			p.save()
			# redirect to a new URL:
			return HttpResponseRedirect('/')

	# if a GET (or any other method) we'll create a blank form
	else:
		form = CarouselForm()

	return render(request, 'hello/addcarousel.html', {'form': form})


@staff_member_required
def delete_carousel(request, carousel_id):
	context = {
		'carousel': Carousel.objects.get(pk=carousel_id)
	}
	if request.method == 'POST':
		c = Carousel.objects.get(pk=carousel_id)
		c.delete()

		allcar = Carousel.objects.all()
		idnum = 0
		for page in allcar:
			idnum = idnum + 1
			page.id = idnum
			page.save()
		return HttpResponseRedirect('/')

	return render(request, 'hello/deletecarousel.html',context)


@staff_member_required
def staff_Settings(request):
	return render(request, 'hello/staff.html')

@staff_member_required
def category_settings(request):
	return render(request, 'hello/categoriessettings.html')


@staff_member_required
def carousel_settings(request):
	carouselpages = Carousel.objects.all().order_by('id')
	context = {
		'carouselpages': carouselpages
	}
	return render(request, 'hello/carouselsettings.html',context)


@staff_member_required
def delete_category(request, category_id):
	context = {
		'category': Category.objects.get(pk=category_id)
	}
	if request.method == 'POST':
		c = Category.objects.get(pk=category_id)
		c.delete()
		return HttpResponseRedirect('/')

	return render(request, 'hello/deletecategory.html',context)


def search(request):
	if request.method == 'POST':
		if request.POST['searchterm']:
			searchterm = request.POST['searchterm']
		else:
			searchterm = ''
		return HttpResponseRedirect(reverse('searchresults',  kwargs={'searchterm': searchterm}))


class SearchResults(generic.ListView):
	paginate_by = 8
	model = Post
	template_name= 'hello/searchresults.html'
	context_object_name = 'searchedposts'

	#kwargs used to get the part of the url you type in the brackets in urls
	def get_queryset(self):
		return Post.objects.filter(content__contains = self.kwargs['searchterm'])

	def get_context_data(self, **kwargs):
		context = super(SearchResults, self).get_context_data(**kwargs)
		context['targeteduser'] = self.request.user
		return context


def search_results(request, searchterm):
	latestposts = Post.objects.filter(content__contains = searchterm)[:5]
	latestusers = User.objects.filter(username__contains = searchterm)[:5]
	postsnum = Post.objects.filter(content__contains = searchterm).count()
	usersnum = User.objects.filter(username__contains = searchterm).count()

	return render(request, 'hello/searchresults.html',{'searchterm' : searchterm, 'latestposts': latestposts, 'latestusers': latestusers, 'postsnum': postsnum, 'usersnum': usersnum})


class MoreSearchPosts(generic.ListView):
	paginate_by = 8
	model = Post
	template_name= 'hello/moresearchedposts.html'
	context_object_name = 'searchedposts'

	#kwargs used to get the part of the url you type in the brackets in urls
	def get_queryset(self):
		return Post.objects.filter(content__contains = self.kwargs['searchterm'])


class MoreSearchUsers(generic.ListView):
	paginate_by = 8
	model = User
	template_name= 'hello/moresearchedusers.html'
	context_object_name = 'searchedusers'

	#kwargs used to get the part of the url you type in the brackets in urls
	def get_queryset(self):
		return User.objects.filter(username__contains = self.kwargs['searchterm'])