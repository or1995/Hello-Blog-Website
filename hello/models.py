import datetime
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from PIL import Image

# Create your models here.
class Category(models.Model):
	title = models.CharField(max_length=200, unique=True)
	description = models.CharField(max_length=200)
	profileimage = models.ImageField(default='Cpdefault.png', upload_to='cat_pics')
	backgroundimage = models.ImageField(default='Cbdefault.png', upload_to='cat_pics')

	def  __str__(self):
		return self.title

	def save(self, *args, **kwargs):
		super(Category, self).save(*args, **kwargs)

		img = Image.open(self.profileimage.path)
		img2 = Image.open(self.backgroundimage.path)

		if img.height > 1000 or img.width > 1000:
			output_size = (1000,1000)
			img.thumbnail(output_size)
		img.save(self.profileimage.path, quality=70)
		img2.save(self.backgroundimage.path, quality=70)


class Post(models.Model):
	title = models.CharField(max_length=200)
	content = models.TextField(max_length=1000)
	pub_date = models.DateTimeField('date published', auto_now_add=True)
	author = models.ForeignKey(User, related_name='postauthoruser' , on_delete=models.CASCADE)
	category = models.ForeignKey(Category, on_delete=models.CASCADE)
	postimage = models.ImageField( upload_to='post_pics', blank=True)
	likes = models.IntegerField(default=0)
	likedusers = models.ManyToManyField(User, related_name='postlikerusers')

	def  __str__(self):
		return self.title

	def was_published_recently(self):
		return self.pub_date >= timezone.now() - datetime.timedelta(days=30)

	def save(self, *args, **kwargs):
		super(Post, self).save(*args, **kwargs)
		if self.postimage:
			img = Image.open(self.postimage.path)
			img.save(self.postimage.path, quality=70)


class Comment(models.Model):
	author = models.ForeignKey(User, related_name='commentauthoruser', on_delete=models.CASCADE)
	article = models.ForeignKey(Post, on_delete=models.CASCADE)
	content = models.TextField(max_length=1000)
	pub_date = models.DateTimeField('date published', auto_now_add=True)
	likes = models.IntegerField(default=0)
	likedusers = models.ManyToManyField(User, related_name='commentlikerusers')

class Reply(models.Model):
	author = models.ForeignKey(User, related_name='replyauthoruser', on_delete=models.CASCADE)
	comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
	content = models.TextField(max_length=1000)
	pub_date = models.DateTimeField('date published', auto_now_add=True)
	likes = models.IntegerField(default=0)
	likedusers = models.ManyToManyField(User, related_name='replylikerusers')

class Carousel(models.Model):
	title = models.CharField(max_length=200)
	description = models.CharField(max_length=200)
	carouselimage = models.ImageField(default='Cbdefault.png', upload_to='carousel_pics')
	carlink= models.CharField(max_length=200, blank=True)

	def  __str__(self):
		return self.title

	def save(self, *args, **kwargs):
		super(Carousel, self).save(*args, **kwargs)
		if self.carouselimage:
			img = Image.open(self.carouselimage.path)
			img.save(self.carouselimage.path, quality=70)