from django.db import models
from django.contrib.auth.models import User # importing a user model which has attributes such as username, password, email etc
import uuid # used to create a unique id for each of the tables/classes
from django.db.models.signals import post_save
from django.conf import settings
from multiselectfield import MultiSelectField
# Create your models here.

class Tag(models.Model):
	name = models.CharField(max_length=200, null=True,blank=True,unique=True)

	def __str__(self):
		return self.name


class Product(models.Model):
	CATEGORY = (		# allows the category attribute have a set choice range which have been listed
				('Cake','Cake'), # first computer variable is listed, then the actual choice
				('Cupcakes','Cupcakes'),
				('DS','Dessert Shots'),
				('Cakesicles','Cakesicles'),
	)
	
	name = models.CharField(max_length=200, null=True, unique=True)
	category = models.CharField(max_length=50, null=True, choices=CATEGORY)
	minprice = models.FloatField(null=True)
	Maxprice = models.FloatField(null=True)
	picture = models.ImageField()
	description = models.CharField(max_length=1000, null=True)
	
	def __str__(self):
		return self.name

class Producttag(models.Model):
	tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
	product = models.ForeignKey(Product, on_delete=models.CASCADE)

	def __str__(self):
		name = str(self.product)
		return name

class Order(models.Model):
	TYPE = (		
				('Cash','Cash'), 
				('Card','Card'),
	)
	# payment method could be one of two types and is specified
	name = models.ForeignKey(Product,on_delete=models.CASCADE, null=True)
	user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	customisation = models.CharField(max_length=1000, null=True)
	price = models.FloatField(null=True)
	paymethod = models.CharField(max_length=500, null=True, choices=TYPE )
	date = models.DateField(auto_now=False, auto_now_add=False)
	picture = models.ImageField(null=True)

#on_delete used to keep referential integrity and if that foreign key deleted then it kept as null
	def __str__(self):
		name = str(self.user)
		return name

		
class Request(models.Model):
		CATEGORY = (
						('Accepted','Accepted'),
						('Pending','Pending'),
						('Rejected','Rejected'),
		)
		TYPE = (		
				('Cash','Cash'), 
				('Card','Card'),
	)	
		user = models.ForeignKey(User, on_delete=models.SET_NULL,null=True, default=None)
		price = models.IntegerField(null=True)
		date = models.DateField(auto_now=False, auto_now_add=False)
		name = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True,default=None)
		Customisation = models.CharField(max_length=1000, null=True)
		status = models.CharField(max_length=50, null=True, choices=CATEGORY,default='Pending')
		paymethod = models.CharField(max_length=50, null=True, choices=TYPE)
		picture = models.ImageField(null=True)

		def __str__ (self):
			name = str(self.user)
			return name

class Block(models.Model):
	date = models.DateField(auto_now=False, auto_now_add=False)
	count = models.IntegerField(null=True)

	def __str__ (self):
		date = str(self.date)
		return date


