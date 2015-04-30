from django.shortcuts import render, redirect
from django.http import HttpResponse
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from datetime import datetime
from rango.bing_search import run_query


def index(request):

	context_dict = {}
	
	#Query the database for a list of All Categories
	#Order the categories by no. likes in descending order.
	#Retrive the top 5 only - or all if less than 5
	#Place the list in our context_dict dictionary which will be passed to template engine
	
	category_list = Category.objects.order_by('-likes')[:5]
	context_dict['categories'] = category_list

    #Query the database for pages
    #Ordered by top 5 pages
    #place the page list in context dictionary to display pages
	page_list = Page.objects.order_by('-views')[:5]
	context_dict['pages'] = page_list

	#Get the number of visits to the site from session based coockies
	visits = request.session.get('visits')
	if not visits:
		visits = 1
	reset_last_visit_time = False
	
	last_visit = request.session.get('last_visit')
	if last_visit:
		last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")

		if (datetime.now() - last_visit_time).seconds > 0:
			#Increment the visits
			visits = visits + 1
			reset_last_visit_time = True
	else:
		reset_last_visit_time = True

	if reset_last_visit_time:
		request.session['last_visit'] = str(datetime.now())
		request.session['visits'] = visits

	context_dict['visits'] = visits

	response = render(request, 'rango/index.html', context_dict)

	return response
	

    
def about(request):
	context_dict = {'aboutmessage': "About xiQaunt under development"}

	return render(request, 'rango/about.html', context_dict)
	'''
	return HttpResponse("Rango about page: \
		  <a href='/rango/''>Index</a>")
	'''

def category(request, category_name_slug):
	# Create a context dictionary which we can pass to the template
	context_dict = {}
	context_dict['result_list'] = None
	context_dict['query'] = None
	if request.method == 'POST':
		query = request.POST['query'].strip()

		if query:
			# Run the BING search function to get the results list
			result_list = run_query(query)

			context_dict['result_list'] = result_list
			context_dict['query'] = query

	try:
		# Can we find a category name slug with the given name?
		# If we can't the .get() method raises a DoseNotExist exception.
		# So the .get() method returns one model instance or raises the exception
		category = Category.objects.get(slug=category_name_slug)
		context_dict['category_name'] = category.name
		context_dict['category_name_slug'] = category.slug

		# Retrive all of the associated pages
		# Note that filter returns >=1 model instance
		pages = Page.objects.filter(category=category).order_by('-views')

		# Add our results list to the template context under name pages.
		context_dict['pages'] = pages
		context_dict['category'] = category

	except Category.DoesNotExist:
		pass

	if not context_dict['query']:
		context_dict['query'] = category.name

	# GO RENDER THE RESPONSE AND RETURN IT TO CLIENT
	return render(request, 'rango/category.html', context_dict)

##### views for ModelForms

# Restrict this view to only logged in users
@login_required
def add_category(request):
	# A HTTP Post?
	if request.method == 'POST':
		form = CategoryForm(request.POST)

		#Have we been provided with a valid form?
		if form.is_valid():
			# Save the new category to the database
			form.save(commit=True)

			# Now call the index() view
			# The user will be shown the homepage
			return index(request)
		else:
			# The supplied form contained errors - just print them to terminal'
			print form.errors
	else:
		# If the request was not a POST, Display the form to enter details
		form = CategoryForm()

	# Bad form (or form details), no form supplied...
	# Render the form with error messages (if any).
	return render(request, 'rango/add_category.html', {'form': form})

# Only registered user can add pages
@login_required
def add_page(request, category_name_slug):

	try:
		cat = Category.objects.get(slug=category_name_slug)
	except Category.DoesNotExist:
		cat = None

	if request.method == 'POST':
		form = PageForm(request.POST)
		if form.is_valid():
			if cat:
				page = form.save(commit=False)
				page.category = cat
				page.views = 0
				page.save()

				#Probably bettween to use redirect here
				return category(request, category_name_slug)
		else:
			print form.errors
	else:
		form = PageForm()

	context_dict = {'form':form, 'category': cat}

	return render(request, 'rango/add_page.html', context_dict)

@login_required
def restricted(request):
	return HttpResponse("Since you are logged in you are able to see it")


# View to handle Bing Search....
def search(request):

	result_list = []

	if request.method == 'POST':
		query = request.POST['query'].strip()

		if query:
			# Run our Bing function to get the results
			result_list = run_query(query)

	return render(request, 'rango/search.html', {'result_list': result_list})

# View to track URL's
def track_url(request):
	page_id = None
	url = '/rango/'
	if request.method == 'GET':
		if 'page_id' in request.GET:
			page_id = request.GET['page_id']
			try:
				page = Page.objects.get(id=page_id)
				page.views = page.views + 1
				page.save()
				url = page.url
			except:
				pass
	return redirect(url)

@login_required
def like_category(request):

	cat_id = None
	#print ">>>>> like_category: ", cat_id
	if request.method == 'GET':
		cat_id = request.GET['category_id']

	likes = 0
	if cat_id:
		cat = Category.objects.get(id=int(cat_id))
		if cat:
			likes = cat.likes + 1
			cat.likes = likes
			cat.save()
	return HttpResponse(likes)

## Helper frunction for suggestings categories
def get_category_list(max_results=0, starts_with=''):

	cat_list = []
	if starts_with:
		# Note isstartswith is case insensitive if we need case sensitive we should use startswith
		#print ">>>> Inside get_category_list ...: ", starts_with
		cat_list = Category.objects.filter(name__istartswith=starts_with)

	#print ">>>> Inside get_category_list ...: ", cat_list

	if max_results > 0:
		if len(cat_list) > max_results:
			cat_list = cat_list[:max_results]

	return cat_list

def suggest_category(request):
	cat_list = []
	starts_with = ''
	if request.method == 'GET':
		starts_with = request.GET['suggestion']

	#print ">>> Inside suggest_category: ", starts_with

	cat_list = get_category_list(8, starts_with)

	#print ">>> Inside suggest_category$$$$$: ", cat_list

	return render(request, 'rango/cats.html', {'cats': cat_list})

## View for adding page
@login_required
def auto_add_page(request):
	cat_id= None
	url = None
	title = None
	context_dict = {}
	
	if request.method == 'GET':
		cat_id = request.GET['category_id']
		url = request.GET['url']
		title = request.GET['title']
		print ">>>> Successfull in entering auto_add_page", cat_id, url, title
		if cat_id:
			category = Category.objects.get(id=int(cat_id))
			p = Page.objects.get_or_create(category=category, title=title, url=url)

			pages = Page.objects.filter(category=category).order_by('-views')

			# Adds our result list to the template context under pages
			context_dict['pages'] = pages

	return render(request, 'rango/page_list.html', context_dict)


## Views for registring users..
'''
def register(request):

	# A boolean value telling the template whether user is registered or not
	registered = False

	#If it's a HTTP Post, we'r interested in processing form
	if request.method ==  'POST':
		#Attempt to grab info from raw form information
		#Note that we make use of both UserForm and UserProfileForm
		user_form = UserForm(data=request.POST)
		profile_form = UserProfileForm(data=request.POST)

		#if the two forms are valid....
		if user_form.is_valid() and profile_form.is_valid():
			# Save the user form data to the database.
			user = user_form.save()

			#Now we hash the password with the set_password method
			# Once hashed, we can update the user object
			user.set_password(user.password)
			user.save()

			# Now sort out the UserProfile instance
			profile = profile_form.save(commit=False)
			profile.user = user

			# Did the user provide a profile picture?
			# If so, we need to get it from the input form
			if 'picture' in request.FILES:
				profile.picture = request.FILES['picture']

			#Now we save the UserProfile model instance
			profile.save()

			#Update our registered variable to template registration was successfull
			registered = True
		# Invalid form or forms -- mistake or something else?
		# print problems to the terminal
		# They'll also be shown to user.
		else:
			print user_form.errors, profile_form.errors
	# Not a HTTP POST, so we render our form using two ModelForm instance
	# These forms will be blank, ready for user input
	else:
		user_form = UserForm()
		profile_form = UserProfileForm()

	# Render the template depending on the context
	return render(request,
	    'rango/register.html', 
	    {'user_form':user_form, 'profile_form': profile_form, 'registered': registered})



def user_login(request):

	#If the request is a HTTP POST, try to pull out relevant informatiom
	if request.method == 'POST':
		#Gather the username and password provided by the user.
		# This information is obtained from the login form.
		# because the request.POST.get('<variable') returns None
		# while the request.POST('<variable') will raise key error exception
		username = request.POST.get('username')
		password = request.POST.get('password')

		#Use Django's machinery to attempt to see if username/passowrd
		# combination is valid 
		user = authenticate(username=username, password=password)

		#If we have a User Object details are correct.
		# If None (Pythons way of absence of values)
		if user:
			# Is the account active?
			if user.is_active:
				### If the account is valid and active, we can log the user in.
				# We'll send the user back to the homepage
				login(request, user)
				return HttpResponseRedirect('/rango/')
			else:
				# Accout was inactive
				return HttpResponse("Your rango account is disabled")

		else:
			# Bad login details provided
			print "Invalid login details: {0}, {1}".format(username, password)
			return HttpResponse("Invalid login details supplied")
	# The request is not HTTP POST, so display the login form
	# This scenario would most likely be a HTTP GET.
	else:
		# No context variables to pass to the template system, hence the
		# blank dictionary object....
		return render(request, 'rango/login.html', {})


# Use the login_required() decorator for logging out
@login_required
def user_logout(request):
	#Since we know user is logged in we log him out
	logout(request)

	# Take the user back to the homepage.
	return HttpResponseRedirect('/rango/')
'''

