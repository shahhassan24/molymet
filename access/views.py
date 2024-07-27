from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import send_mail
import random
from django.contrib.auth import views as auth_views

from .forms import LoginForm, ResetForm, SecondFactorForm

def send_2FA_email(request, user):
	# Generate a random 6-digit 2FA code
	code = str(random.randint(1000000, 9999999))
	print(code)
	# Store it in the session (You might prefer to store it in the database)
	request.session['2FA_code'] = code

	# Send email with the code
	send_mail(
		'Tu código 2FA',
		f'Tu código de verificación para 2FA es: {code}',
		'no-reply@help.clientis.tech',  # Your sending email
		[user.email],
		fail_silently=False,
	)
	print("Mail sent to", user.email)
	return

def verify_2FA_code(request, user, provided_code):
	stored_code = request.session.get('2FA_code', None)
	print(stored_code)
	# Compare the provided code with the stored code
	if provided_code == stored_code:
		# Remove the code from the session after it's been used
		del request.session['2FA_code']
		return True
	return False

def sign_in(request):
	if request.method == 'GET':
		try: 
			if request.user.is_authenticated:
				return redirect('index')
		except:
			pass

		form = LoginForm()
		return render(request,'access/login.html', {'form': form})
	
	elif request.method == 'POST':
		form = LoginForm(request.POST)
		
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user = authenticate(request, username=username, password=password)
			if user is not None:

				login(request, user)
				return redirect('index')

				# Assuming you've set up a send_2FA_email function
				send_2FA_email(request, user)
				
				# Store username and password temporarily in session for 2FA verification
				request.session['temp_username'] = username
				request.session['temp_password'] = password
				return redirect('second_factor')
			else:
				messages.error(request, f'Email o contraseña incorrecta.')
		return render(request, 'access/login.html', {'form': form})

def sign_out(request):
	logout(request)
	# messages.success(request,f'You have been logged out.')
	return redirect('login')

def reset_password(request):
    return auth_views.PasswordResetView.as_view()(request)

def second_factor(request):
	if request.method == 'POST':
		form = SecondFactorForm(request.POST)

		if form.is_valid():
			second_factor = form.cleaned_data['second_factor']

			# Verify the 2FA code. Placeholder function here
			is_valid_2fa = verify_2FA_code(request, request.user, second_factor)
			print(is_valid_2fa)
			if is_valid_2fa:
				# Get stored username and password from session
				username = request.session.pop('temp_username', None)
				password = request.session.pop('temp_password', None)
				
				user = authenticate(request, username=username, password=password)
				if user:
					login(request, user)
					return redirect('index')

	form = SecondFactorForm()
	return render(request,'access/second_factor.html',{'form': form}) 


