from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
	name = models.CharField(max_length=128, unique=True)
	views = models.IntegerField(default=0)
	likes = models.IntegerField(default=0)
	slug = models.SlugField(default='')

	class Meta:
		verbose_name_plural = "Categories"
	
	def save(self, *args, **kwargs):
		self.slug = slugify(self.name)
		super(Category, self).save(*args, **kwargs)
	

	def __unicode__(self):
		return self.name

class Page(models.Model):
	category = models.ForeignKey(Category)
	title = models.CharField(max_length=128)
	url = models.URLField()
	views = models.IntegerField(default=0)

	def __unicode__(self):
		return self.title

# Model for extending defaul django user class
# We are going to just use one-To-One field that way we do not inherit it directly
class UserProfile(models.Model):
	# This line is required to link UserProfile with User model instance
	user = models.OneToOneField(User)

	#The additional attributes needed for UserProfile
	website = models.URLField(blank=True)
	picture = models.ImageField(upload_to='profile_images', blank=True)

	# Override the __unicode__() method to return out something meaningful like Java toString()
	def __unicode__(self):
		return self.user.username
