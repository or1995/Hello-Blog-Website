from django.db import models 
from django.contrib.auth.models import User
from PIL import Image  

# Create your models here.
class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	profileimage = models.ImageField(default='Pdefault.png', upload_to='profile_pics')
	backgroundimage = models.ImageField(default='Bdefault.png', upload_to='background_pics')
	bio = models.TextField(default='No bio',max_length=1000)
	followers = models.ManyToManyField("self", blank=True, symmetrical=False) # symmetrical=True example is if i follow profile the profile follow me

	def __str__(self):
		return self.user.username;

	def save(self, *args, **kwargs):
		super(Profile, self).save(*args, **kwargs)

		img = Image.open(self.profileimage.path)
		img2 = Image.open(self.backgroundimage.path)

		if img.height > 300 or img.width > 300:
			output_size = (300,300)
			img.thumbnail(output_size)
		img.save(self.profileimage.path, quality=70)
		img2.save(self.backgroundimage.path, quality=70)

