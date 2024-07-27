from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
	path('', views.sign_in, name='login'),
	path('logout/', views.sign_out, name='logout'),
	# path('reset/password/', views.reset_password, name='forgot_password'),
	path('second-factor/', views.second_factor, name='second_factor'),

	path('password_reset/', views.reset_password, name='password_reset'),
	path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
	path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
	path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

]
