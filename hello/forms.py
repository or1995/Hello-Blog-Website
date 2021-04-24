from django import forms
from .models import Post, Category, Comment, Carousel, Reply

'''
CATEGORY_CHOICES =()
listCat = list(CATEGORY_CHOICES)

c = Category.objects.all()
for category in c:
	listCat.append((category.id, category.title))

CATEGORY_CHOICES = tuple(listCat)
'''

class PostForm(forms.ModelForm):  # <-- the ModelForm part is import for image upload
	postimage = forms.ImageField(required=False, widget=forms.FileInput)

	#category = forms.ChoiceField(label='Category', choices=CATEGORY_CHOICES)

	class Meta:
		model = Post
		fields = ['title','content','category','postimage']

class CategoryForm(forms.ModelForm):
	#title = forms.CharField(max_length=100)
	#description = forms.CharField(widget=forms.Textarea)

	class Meta:
		model = Category
		fields = ['title','description','profileimage','backgroundimage']


class CarouselForm(forms.ModelForm):

	class Meta:
		model = Carousel
		fields = ['title','description','carlink','carouselimage']


class CommentForm(forms.ModelForm):
	content = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Add a Comment'}))

	class Meta:
		model = Comment
		fields= ['content']	


class SearchForm(forms.Form):
	search = forms.CharField(required=False)
