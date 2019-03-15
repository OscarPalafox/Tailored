from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from datetime import date

class UserProfile(models.Model):
	user = models.OneToOneField(User)

	picture = models.ImageField(upload_to = "profile_images", blank = True)
	postcode = models.CharField(max_length = 8)
	rating = models.IntegerField(default = 0)
	phone = models.IntegerField(default = 0)

	def __str__(self):
		return self.user.username


class Category(models.Model):
	title = models.CharField(max_length = 128, unique = True, primary_key = True)

	class Meta:
		verbose_name_plural = "categories"
	
	def __str__(self):
		return self.title


class Section (models.Model):
	title = models.CharField(max_length = 128, unique = True, primary_key = True)

	def __str__(self):
		return self.title


class Item(models.Model):
	itemID = models.IntegerField(primary_key = True)
	name = models.CharField(max_length = 128)
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
		return self.name

class Review(models.Model):
	reviewID = models.IntegerField(primary_key = True)
	buyerID = models.ForeignKey(UserProfile)
	itemID = models.ForeignKey(Item)
	rating = models.CharField(max_length=1, validators=[RegexValidator(r'^\d{0,6}$')])
	review = models.TextField(blank = True)
	datePosted = models.DateField(default = date.today)

	def __str__(self):
		return self.reviewID