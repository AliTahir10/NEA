from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import *
from .forms import *
from .decorators import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.utils.timezone import datetime
import sqlite3,os
# Create your views here. this allows each page to have a name which can be called upon 

def store(request):
	products = Product.objects.all().exclude(name='Custom') # fetching all products from the models file
	if request.POST.get('priceasc'):
		products = Product.objects.all().order_by('minprice').exclude(name='Custom')#sorts by price

	elif request.POST.get('pricedesc'):
		products = Product.objects.all().order_by('-minprice').exclude(name='Custom')

	elif request.POST.get('nameasc'):
		products = Product.objects.all().order_by('name').exclude(name='Custom')#sprts by name

	elif request.POST.get('namedesc'):
		products = Product.objects.all().order_by('-name').exclude(name='Custom')

	elif request.POST.get('Search'):#only when search form has been submitted then this code runs
		Search = request.POST.get('Search')
		if Search is not None:
			Search = Search.title() # capitalises all the letters of the search to make it the same as what it is saved as in the database
			ids = Tag.objects.filter(name=Search).values('id').first()
			if ids is not None:
				ids = ids['id']
			products = Product.objects.all().filter(producttag__tag=ids)
			if ids is None:
    				products =  Product.objects.all().exclude(name='Custom')
    			

	#have it so that there is another class tags with a many to many field so that many tags can be chosen yay
	
	context = {'products': products} #context allows us to pass objects to the store template
	return render(request, 'store/store.html', context)

def enquire(request):
	form = Enquire()
	if request.method == "POST":#only runs when form has been submitted
		form = Enquire(request.POST,request.FILES)#retrieveing all the data from the form
		if form.is_valid():
			instance = form.save(commit=False)
			instance.user = request.user
			instance.save()#saves the form to the database
			return redirect('home')
			

	context = {'form': form}
	return render(request, 'store/enquire.html', context)


@admin_only#imported the decorator so only the admin user can use it
def admn(request):
	context = {}
	return render(request, 'store/admn.html', context)

def home(request):
    context = {}
    return render(request, 'store/home.html', context)

def availability(request):
	blocks = Block.objects.filter(count__gte=5,).exclude(date__lte= datetime.now())
	# queries all dates where count is 5 or greater and excludes any dates that have passed
	context = {'blocks':blocks}
	return render(request, 'store/availability.html', context)

def orders(request):
	users = request.user
	ordersl = Order.objects.filter(user=users)
	requests = Request.objects.filter(user=users,status="Rejected")
	
	
	context = {'ordersl':ordersl,'requests':requests}
	return render(request, 'store/orders.html', context)

def login(request):
	if request.method =="POST":
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(username=username, password=password)
		
		if user is not None:
			login(request, user)
			return redirect('home')
		else:
			messages.info(request, 'invalid details')
	context = {'messages':messages}
	return render(request, 'registration/login.html', context)

def register(request):
	if request.method == "POST": # #allows form to be sent put into the user database
		form = Createuser(request.POST)
		if form.is_valid():
			form.save()
			username = request.POST.get('username')
			fname = form.cleaned_data.get('first_name')
			lname = form.cleaned_data.get('last_name')
			email = form.cleaned_data.get('email')
			messages.success(request, 'Account was created for ' + fname)
			#success message tells user that they have logged in 
			return redirect('login')
			# sends user to login page to log in to website
	else:
		form = Createuser()


	context = {'form': form}
	return render(request, 'store/register.html', context)

def admins(request):
	requests = Request.objects.filter(status='Pending')
		
	context = {'requests': requests}
	return render(request,'store/admins.html', context)

def updates(request, pk):
	updates = Request.objects.get(id=pk)
	form = Update(instance=updates)

	if request.method =='POST':
		form = Update(request.POST,instance=updates)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('user')
			name = form.cleaned_data.get('name')
			date = request.POST.get('date')
			customisation = request.POST.get('Customisation')
			paymethod = request.POST.get('paymethod')
			picture = request.POST.get('picture')
			price = request.POST.get('price')
			choice = form.cleaned_data.get('status')
			emails = User.objects.get(username=username)
			email = emails.email


			if 	choice == 'Accepted':
				order = Order(name=name,user=username,customisation=customisation,price=price,paymethod=paymethod,date=date,picture=picture)
				message = ('Thank you for your enquiry. We would like to confirm your order for the',date,'\nThe address for collection is 123 london road.\n\nSee You Soon!')
				order.save()
				send_mail(
					'Order Confirmation', #subject
					'Thank you for your enquiry. Your order has been confirmed.Please log in to view more information in regards to your order.\nKind Regards,\nAsifa Nazir\nCEO of Simply Sweet By Asifa', #message
					'simplysweettest@gmail.com', #from email
					[email],#to email
				)
				empty = Block.objects.filter(date__exact=date).count()
				if empty == 0:
					block = Block(date=date,count=1)
					block.save()
				else:
					empties = Block.objects.get(date=date)
					number = empties.count
					empties.count = number + 1
					empties.save(update_fields=['count'])

			if choice == 'Rejected':
				send_mail(
					'Order Update',
					'Thank you for your Enquiry. Unfortunately we were not able to accept your order.\n Kind Regards,\nAsifa Nazir\nCEO of Simply Sweet By Asifa',
					'simplysweettest@gmail.com',
					[email],
				)

			
			return redirect('/admins')

	
	context = {'updates':updates,'form':form}
	return render(request, 'store/Updates.html', context)

# make it so that if accept is pressed it takes you to the another page with the prefilled order which you then save no accept or reject you just make it accepted then email sent to show acceptance and then if reject then give reject email by querying the form data
def block(request):
	form = blockday()
	if request.method == "POST":
		form = blockday(request.POST,request.FILES)
		if form.is_valid():
			date = request.POST.get('date')
			empty = Block.objects.filter(date__exact=date).count()
			if empty == 0:
				block = Block(date=date,count=5)
				block.save()
				return redirect('availability')
			else:
				empties = Block.objects.get(date=date)
				empties.count = 5
				empties.save(update_fields=['count'])
				return redirect('availability')
			messages.success(request, 'The following day will be blocked:'+date)

	context = {'form':form}
	return render(request, 'store/block.html', context)

def free(request):
	blocks = Block.objects.filter(count__gte=5,).exclude(date__lte= datetime.now())
	form = blockday()
	if request.method == "POST":
		form = blockday(request.POST,request.FILES)
		if form.is_valid():
			date = request.POST.get('date')
			empty = Block.objects.filter(date__exact=date).count()
			if empty != 0:
				empties = Block.objects.get(date=date)
				empties.count = 0
				empties.save(update_fields=['count'])
			messages.success(request, 'The following day will be free')
	context = {'blocks':blocks,'form':form}
	return render(request, 'store/free.html', context)

def product(request):
	form = Createproduct()
	if request.method == "POST":
		form = Createproduct(request.POST,request.FILES)
		if form.is_valid():
			form.save()
			return redirect('store')
			

	context = {'form': form}
	return render(request, 'store/product.html',context)

def tag(request):
	form = tags()
	if request.method =="POST":
		form = tags(request.POST,request.FILES)
	if form.is_valid():
		form.save()
		messages.success(request, 'tag has been made')
	context = {'form':form}
	return render(request, 'store/tag.html',context)


def info(request, pk):
	product  = Product.objects.get(id=pk)

	context = {'product':product}
	return render(request,'store/info.html',context)