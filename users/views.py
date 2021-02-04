from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required

# Create your views here.
'''
#my register and login views
def register_view(request):
	# if this is a POST request we need to process the form data
	if request.method == 'POST':
		# create a form instance and populate it with data from the request:
		form = RegisterForm(request.POST)
		# check whether it's valid:
		if form.is_valid():
			# process the data in form.cleaned_data as required
			remail = form.cleaned_data['email']
			rusername = form.cleaned_data['username']
			rpassword1 = form.cleaned_data['password1']
			rpassword2 = form.cleaned_data['password2']
			if rpassword1 != rpassword2 or len(rpassword1) < 8:
				if rpassword1 != rpassword2:
					messages.warning(request, "password doesn't match")
				if len(rpassword1) < 8:
					messages.warning(request, "password is too short")
				return HttpResponseRedirect('../register')
			newuser = Useruser = User.objects.create_user(email=remail, username=rusername, password=rpassword1)
			newuser.save()
			# redirect to a new URL:
			return HttpResponseRedirect('../login')

	# if a GET (or any other method) we'll create a blank form
	else:
		form = RegisterForm()

	return render(request, 'users/register.html', {'form': form})

def login_view(request):
	if request.method == 'POST':
		form = LoginForm(request.POST)

		if form.is_valid():
			lusername = form.cleaned_data['username']
			lpassword = form.cleaned_data['password']
			loginuser = authenticate(request, username=lusername, password=lpassword)
			if loginuser is not None:
				login(request, loginuser)
				return HttpResponseRedirect('/')
			else:
				messages.warning(request, "User is not found")
				return HttpResponseRedirect('../login')
	
	else:
		form = LoginForm()

	return render(request, 'users/login.html', {'form': form})
'''

def register(request):
	# Don't go to the register ,if user is authenticated redirect to index
	if request.user.is_authenticated:
		return redirect('index')
		
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			messages.success(request, f'your account has been created! you are now able to login')
			return redirect('login')
	else:
		form = UserRegisterForm()
	return render(request,'users/register.html',{'form': form})

def logout_view(request):
	logout(request)
	return HttpResponseRedirect('../')

@login_required
def my_Account_settings(request):
	if request.method == 'POST':
		# create a form instance and populate it with data from the request:
		userform = UserUpdateForm(request.POST,instance=request.user)
		profileform = ProfileUpdateForm(request.POST, request.FILES,instance=request.user.profile)

		# check whether it's valid:
		if userform.is_valid() and profileform.is_valid():
			# process the data in form.cleaned_data as required
			cu = request.user
			uusername = userform.cleaned_data['username']
			uemail = userform.cleaned_data['email']
			cu.username = uusername
			cu.email = uemail
			cu.save()

			cp = request.user.profile
			pprofileimage = profileform.cleaned_data['profileimage']
			pbackgroundimage = profileform.cleaned_data['backgroundimage']
			pbio = profileform.cleaned_data['bio']
			cp.profileimage = pprofileimage
			cp.backgroundimage = pbackgroundimage
			cp.bio = pbio
			cp.save()

			# redirect to a new URL:
			return HttpResponseRedirect('../account-settings/')

	# if a GET (or any other method) we'll create a blank form
	else:
		userform = UserUpdateForm(instance=request.user)
		profileform = ProfileUpdateForm(instance=request.user.profile)

	return render(request, 'users/accountsettings.html', {'userform': userform,'profileform': profileform})


