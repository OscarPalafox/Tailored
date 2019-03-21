from django.test import TestCase
from tailored.models import Item, Category, Section, Size, UserProfile, Review
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError


class UserProfileMethodTests(TestCase):
	def test_postcode_is_not_only_letters(self):
		'''Test that the database does not store a postcode with only letters.'''
		user_profile = UserProfile(user = User.objects.create_user(username = 'testpostcode',
																	email = 'test@test.com',
																	password = 'test123', 
																	first_name = 'test',
																	last_name = 'postcode'),
									postcode = 'AAA')

		self.assertRaises(ValidationError, user_profile.save)

	def test_postcode_is_not_only_numbers(self):
		'''Test that the database does not store a postcode with only numbers.'''
		user_profile = UserProfile(user = User.objects.create_user(username = 'testpostcode',
																	email = 'test@test.com',
																	password = 'test123', 
																	first_name = 'test',
																	last_name = 'postcode'),
									postcode = '000')

		self.assertRaises(ValidationError, user_profile.save)

	def test_postcode_is_less_than_eight(self):
		'''Test that the database does not store a postcode with more than eight characters.'''
		user_profile = UserProfile(user = User.objects.create_user(username = 'testpostcode',
																	email = 'test@test.com',
																	password = 'test123', 
																	first_name = 'test',
																	last_name = 'postcode'),
									postcode = 'EC2R 9BBH')

		self.assertRaises(ValidationError, user_profile.save)

	def test_postcode_is_valid_without_spaces(self):
		'''Test that a correct postcode without spaces can be saved.'''
		valid_postcode = 'W1D1AN'
		user_profile = UserProfile(user = User.objects.create_user(username = 'testpostcode',
																	email = 'test@test.com',
																	password = 'test123', 
																	first_name = 'test',
																	last_name = 'postcode'),
									postcode = valid_postcode)
		user_profile.save()
		self.assertEqual(user_profile.postcode, valid_postcode)

	def test_postcode_is_valid_with_spaces(self):
		'''Test that a correct postcode with spaces can be saved,'''
		valid_postcode = 'EC2R 8AH'
		user_profile = UserProfile(user = User.objects.create_user(username = 'testpostcode',
																	email = 'test@test.com',
																	password = 'test123', 
																	first_name = 'test',
																	last_name = 'postcode'),
									postcode = valid_postcode)
		user_profile.save()
		self.assertEqual(user_profile.postcode, valid_postcode)

	def test_username_is_unique(self):
		'''Test that the username field is unique.'''
		valid_postcode = 'EC2R 8AH'
		user = User.objects.create_user(username = 'testusername', email = 'test@test.com', password = 'test123',
										first_name = 'test', last_name = 'username')
		
		user_profile1 = UserProfile(user = user, postcode = valid_postcode)
		user_profile1.save()
		
		user_profile2 = UserProfile(user = user, postcode = valid_postcode)
		self.assertRaises(ValidationError, user_profile2.save)

	def test_rating_is_not_smaller_than_zero(self):
		'''Test that the database does not store a negative rating.'''
		valid_postcode = 'EC2R 8AH'
		user_profile = UserProfile(user = User.objects.create_user(username = 'testrating',
																	email = 'test@test.com',
																	password = 'test123', 
																	first_name = 'test',
																	last_name = 'rating'),
									postcode = valid_postcode,
									rating = -1)

		self.assertRaises(ValidationError, user_profile.save)

	def test_rating_is_not_bigger_than_five(self):
		'''Test that the database does not store a higher rating than 5.'''
		valid_postcode = 'EC2R 8AH'
		user_profile = UserProfile(user = User.objects.create_user(username = 'testrating',
																	email = 'test@test.com',
																	password = 'test123', 
																	first_name = 'test',
																	last_name = 'rating'),
									postcode = valid_postcode,
									rating = 6)

		self.assertRaises(ValidationError, user_profile.save)

	def test_rating_is_decimal(self):
		'''Test that the database can store a decimal rating.'''
		valid_postcode = 'EC2R 8AH'
		valid_rating = 2.5
		user_profile = UserProfile(user = User.objects.create_user(username = 'testrating',
																	email = 'test@test.com',
																	password = 'test123', 
																	first_name = 'test',
																	last_name = 'rating'),
									postcode = valid_postcode,
									rating = valid_rating)
		user_profile.save()
		self.assertEqual(valid_rating, user_profile.rating)

	def test_phone_number_is_not_negative(self):
		'''Test that the database does not store a negative phone number.'''
		valid_postcode = 'EC2R 8AH'
		user_profile = UserProfile(user = User.objects.create_user(username = 'testphonenumber',
																	email = 'test@test.com',
																	password = 'test123', 
																	first_name = 'test',
																	last_name = 'phonenumber'),
									postcode = valid_postcode,
									phone = '-02079304832')
		self.assertRaises(ValidationError, user_profile.save)

	def test_phone_number_is_valid(self):
		'''Test that the database stores a valid number.'''
		valid_postcode = 'EC2R 8AH'
		valid_phone_number = '02079304832'
		user_profile = UserProfile(user = User.objects.create_user(username = 'testphonenumber',
																	email = 'test@test.com',
																	password = 'test123', 
																	first_name = 'test',
																	last_name = 'phonenumber'),
									postcode = valid_postcode,
									phone = valid_phone_number)
		user_profile.save()
		self.assertEqual(valid_phone_number, user_profile.phone)

	def test_phone_number_has_no_spaced(self):
		'''Test that the database does not store a spaced phone number.'''
		valid_postcode = 'EC2R 8AH'
		user_profile = UserProfile(user = User.objects.create_user(username = 'testphonenumber',
																	email = 'test@test.com',
																	password = 'test123', 
																	first_name = 'test',
																	last_name = 'phonenumber'),
									postcode = valid_postcode,
									phone = '020 7930 4832')
		self.assertRaises(ValidationError, user_profile.save)


	def test_phone_number_has_no_extension(self):
		'''Test that the database does not store a phone number with +.'''
		valid_postcode = 'EC2R 8AH'
		user_profile = UserProfile(user = User.objects.create_user(username = 'testphonenumber',
																	email = 'test@test.com',
																	password = 'test123', 
																	first_name = 'test',
																	last_name = 'phonenumber'),
									postcode = valid_postcode,
									phone = '+442079304832')
		self.assertRaises(ValidationError, user_profile.save)

	def test_phone_number_has_no_parenthesis(self):
		'''Test that the database does not store a phone number with parenthesis.'''
		valid_postcode = 'EC2R 8AH'
		user_profile = UserProfile(user = User.objects.create_user(username = 'testphonenumber',
																	email = 'test@test.com',
																	password = 'test123', 
																	first_name = 'test',
																	last_name = 'phonenumber'),
									postcode = valid_postcode,
									phone = '(0)2079304832')
		self.assertRaises(ValidationError, user_profile.save)


class CategoryMethodTests(TestCase):
	def test_slug_line_creation(self):
		'''Test that slug field is correctly created.'''
		category = Category(title = 'Test The Slug Creation')
		category.save()
		self.assertEqual(category.slug, 'test-the-slug-creation')

	def test_category_title_is_unique(self):
		'''Test that the title field is unique.'''
		category1 = Category(title = 'Test1')
		category1.save()
		
		category2 = Category(title = 'Test1')
		self.assertRaises(ValidationError, category2.save)

	def test_categories_different_name_different(self):
		'''Test that the categories are different if their title is different.'''
		category1 = Category(title = 'Test1')
		category2 = Category(title = 'Test2')
		self.assertNotEqual(category1, category2)


class SectionMethodTests(TestCase):
	def test_section_title_is_unique(self):
		'''Test that the title field is unique.'''
		section1 = Section(title = 'Test1')
		section1.save()
		
		section2 = Section(title = 'Test1')
		self.assertRaises(ValidationError, section2.save)

	def test_sections_different_name_different(self):
		'''Test that the sections are different if their title is different.'''
		section1 = Section(title = 'Test1')
		section2 = Section(title = 'Test2')
		self.assertNotEqual(section1, section2)


class SizeMethodTests(TestCase):
	def test_size_title_is_unique(self):
		'''Test that the title field is unique.'''
		size1 = Size(title = 'Test1')
		size1.save()
		
		size2 = Size(title = 'Test1')
		self.assertRaises(ValidationError, size2.save)

	def test_size_different_name_different(self):
		'''Test that the sizes are different if their title is different.'''
		size1 = Size(title = 'Test1')
		size2 = Size(title = 'Test2')
		self.assertNotEqual(size1, size2)


class ItemMethodTests(TestCase):
	def test_item_price_is_not_negative(self):
		'''Test that the database does not store a negative item price.'''
		valid_postcode = 'EC2R 8AH'
		user_profile = UserProfile(user = User.objects.create_user(username = 'testprice',
																	email = 'test@test.com',
																	password = 'test123', 
																	first_name = 'test',
																	last_name = 'price'),
									postcode = valid_postcode)
		user_profile.save()

		category = Category('Test')
		category.save()
		
		section = Section('Test')
		section.save()
		
		size = Size('Test')
		size.save()

		item = Item(title = 'Test', price = -10, seller = user_profile, category = category, section = section,
					size = size)

		self.assertRaises(ValidationError, item.save)

	def test_item_price_is_decimal(self):
		'''Test that the database can handle decimal prices.'''
		valid_postcode = 'EC2R 8AH'
		user_profile = UserProfile(user = User.objects.create_user(username = 'testprice',
																	email = 'test@test.com',
																	password = 'test123', 
																	first_name = 'test',
																	last_name = 'price'),
									postcode = valid_postcode)
		user_profile.save()

		category = Category('Test')
		category.save()
		
		section = Section('Test')
		section.save()
		
		size = Size('Test')
		size.save()

		# Needs to be a string for the validator to work
		valid_price = '10.30'

		item = Item(title = 'Test', price = valid_price, seller = user_profile, category = category, section = section,
					size = size)
		item.save()

		self.assertEqual(valid_price, str(item.price))

	def test_item_price_is_decimal_correct(self):
		'''Test that the database does not save prices with more than two decimal places.'''
		valid_postcode = 'EC2R 8AH'
		user_profile = UserProfile(user = User.objects.create_user(username = 'testprice',
																	email = 'test@test.com',
																	password = 'test123', 
																	first_name = 'test',
																	last_name = 'price'),
									postcode = valid_postcode)
		user_profile.save()

		category = Category('Test')
		category.save()
		
		section = Section('Test')
		section.save()
		
		size = Size('Test')
		size.save()

		item = Item(title = 'Test', price = '10.301', seller = user_profile, category = category, section = section,
					size = size)
		self.assertRaises(ValidationError, item.save)

	def test_item_daily_visits_is_not_negative(self):
		'''Test that the database does not save negative daily visits.'''
		valid_postcode = 'EC2R 8AH'
		user_profile = UserProfile(user = User.objects.create_user(username = 'testvisits',
																	email = 'test@test.com',
																	password = 'test123', 
																	first_name = 'test',
																	last_name = 'visits'),
									postcode = valid_postcode)
		user_profile.save()

		category = Category('Test')
		category.save()
		
		section = Section('Test')
		section.save()
		
		size = Size('Test')
		size.save()

		valid_price = '10.30'

		item = Item(title = 'Test', price = valid_price, seller = user_profile, category = category, section = section,
					size = size, dailyVisits = -1)
		self.assertRaises(ValidationError, item.save)


class ReviewMethodTests(TestCase):
	def test_review_rating_is_not_negative(self):
		'''Test that the database does not save ratings that are smaller than 0.'''
		valid_postcode = 'EC2R 8AH'
		user_profile = UserProfile(user = User.objects.create_user(username = 'testrating',
																	email = 'test@test.com',
																	password = 'test123', 
																	first_name = 'test',
																	last_name = 'rating'),
									postcode = valid_postcode)
		user_profile.save()

		user_profile2 = UserProfile(user = User.objects.create_user(username = 'testrating2',
																	email = 'test@test.com',
																	password = 'test123', 
																	first_name = 'test',
																	last_name = 'rating'),
									postcode = valid_postcode)
		user_profile2.save()

		category = Category('Test')
		category.save()
		
		section = Section('Test')
		section.save()
		
		size = Size('Test')
		size.save()

		valid_price = '10.30'

		item = Item(title = 'Test', price = valid_price, seller = user_profile, category = category, section = section,
					size = size, sold_to = user_profile2)
		item.save()

		review = Review(item = item, rating = -1)
		self.assertRaises(ValidationError, review.save)

	def test_review_rating_is_smaller_than_5(self):
		'''Test that the database does not save ratings that are higher than 5.'''
		valid_postcode = 'EC2R 8AH'
		user_profile = UserProfile(user = User.objects.create_user(username = 'testrating',
																	email = 'test@test.com',
																	password = 'test123', 
																	first_name = 'test',
																	last_name = 'rating'),
									postcode = valid_postcode)
		user_profile.save()

		user_profile2 = UserProfile(user = User.objects.create_user(username = 'testrating2',
																	email = 'test@test.com',
																	password = 'test123', 
																	first_name = 'test',
																	last_name = 'rating'),
									postcode = valid_postcode)
		user_profile2.save()

		category = Category('Test')
		category.save()
		
		section = Section('Test')
		section.save()
		
		size = Size('Test')
		size.save()

		valid_price = '10.30'

		item = Item(title = 'Test', price = valid_price, seller = user_profile, category = category, section = section,
					size = size, sold_to = user_profile2)
		item.save()

		review = Review(item = item, rating = 6)
		self.assertRaises(ValidationError, review.save)