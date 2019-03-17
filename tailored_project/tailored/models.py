from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from datetime import date
from django.template.defaultfilters import slugify

# Make email field unique along all users
User._meta.get_field('email')._unique = True

class UserProfile(models.Model):
	"""Class representing a user profile."""
	# This line links UserProfile to a User model instance
	user = models.OneToOneField(User)

	# Additional attributes we wish to include
	picture = models.ImageField(upload_to = "profile_images", blank = True)
	postcode = models.CharField(max_length = 8)
	rating = models.IntegerField(default = 0)
	phone = models.CharField(max_length = 8, validators = [RegexValidator(r'^\d{0,10}$')], blank = True)

	def __str__(self):
		return self.user.username


class Category(models.Model):
	"""Class representing a category."""

	title = models.CharField(max_length = 128, unique = True, primary_key = True)

	
	slug = models.SlugField()
	def save(self, *args, **kwargs):
		self.slug = slugify(self.title)
		super(Category, self).save(*args, **kwargs)
	
	
	class Meta:
		verbose_name_plural = "categories"
	
	def __str__(self):
		return self.title


class Section (models.Model):
	"""Class representing a section"""

	title = models.CharField(max_length = 128, unique = True, primary_key = True)

	def __str__(self):
		return self.title


class Item(models.Model):
	"""Class representing an item."""

	itemID = models.IntegerField(primary_key = True)
	title = models.CharField(max_length = 128, unique = False)
	price = models.IntegerField(default = 0)
	

	category = models.ForeignKey(Category)
	section = models.ForeignKey(Section)

	itemPic = models.ImageField(upload_to = "item_images", blank = True)
	
	description = models.TextField(blank = True)
	datePosted = models.DateField(default = date.today)
	
	sold = models.BooleanField(default = False)
	dailyVisits = models.IntegerField(default = 0)
	size = models.CharField(max_length = 128)

	def __str__(self):
		return self.title

class Review(models.Model):
	"""Class representing a review."""
	reviewID = models.IntegerField(primary_key = True)
	buyerID = models.ForeignKey(UserProfile)
	itemID = models.ForeignKey(Item)
	rating = models.CharField(max_length = 1, validators = [RegexValidator(r'^\d{0,6}$')])
	review = models.TextField(blank = True)
	datePosted = models.DateField(default = date.today)

	def __str__(self):
		return self.reviewID