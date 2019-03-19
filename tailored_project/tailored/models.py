from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from datetime import date
from django.core.validators import RegexValidator, MaxValueValidator, MinValueValidator
from uuid import uuid4

class UserProfile(models.Model):
	"""Class representing a user profile."""
	# This line links UserProfile to a User model instance
	user = models.OneToOneField(User)

	# Additional attributes we wish to include
	picture = models.ImageField(upload_to = "profile_images", blank = True)
	postcode = models.CharField(max_length = 8, validators = [RegexValidator(r'^(([gG][iI][rR] {0,}0[aA]{2})|((([a-pr-uwyzA-PR-UWYZ][a-hk-yA-HK-Y]?[0-9][0-9]?)|(([a-pr-uwyzA-PR-UWYZ][0-9][a-hjkstuwA-HJKSTUW])|([a-pr-uwyzA-PR-UWYZ][a-hk-yA-HK-Y][0-9][abehmnprv-yABEHMNPRV-Y]))) {0,}[0-9][abd-hjlnp-uw-zABD-HJLNP-UW-Z]{2}))$')])
	rating = models.IntegerField(default = 0)
	phone = models.CharField(max_length = 8, blank = True, validators = [RegexValidator(r'^[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[-\s\.0-9]*$')])

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


class Section(models.Model):
	"""Class representing a section"""

	title = models.CharField(max_length = 128, unique = True, primary_key = True)

	def __str__(self):
		return self.title


class Size(models.Model):
	title = models.CharField(max_length = 128, primary_key = True)

	def __str__(self):
		return self.title

class Item(models.Model):
	"""Class representing an item."""
	itemID = models.UUIDField(max_length = 128, primary_key = True, default = uuid4, editable = False)

	title = models.CharField(max_length = 128)
	price = models.DecimalField(help_text = "Enter the price: ",
		validators = [MinValueValidator(0)], decimal_places = 2, default = 0, max_digits = 100)

	seller = models.ForeignKey(UserProfile, related_name = 'seller')

	category = models.ForeignKey(Category)
	section = models.ForeignKey(Section)

	picture = models.ImageField(upload_to = "item_images", blank = True)
	
	description = models.TextField(blank = True)
	datePosted = models.DateField(default = date.today)
	
	sold_to = models.ForeignKey(UserProfile, related_name = 'buyer', blank = True, null = True)
	dailyVisits = models.IntegerField(default = 0)
	size = models.ForeignKey(Size)

	def __str__(self):
		return self.title

class Review(models.Model):
	"""Class representing a review."""
	#reviewID = models.AutoField(primary_key = True)
	buyer = models.ForeignKey(UserProfile)
	item = models.ForeignKey(Item)
	rating = models.IntegerField(validators = [MinValueValidator(0), MaxValueValidator(5)])
	review_text = models.TextField(blank = True)
	datePosted = models.DateField(default = date.today)

	def __str__(self):
		return "ID" + str(self.id)