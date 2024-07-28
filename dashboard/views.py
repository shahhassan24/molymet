from django.shortcuts import render
from django.contrib.auth.decorators import login_required



@login_required
def index(request):

	context = {}
	return render(request, 'dashboard/index.html', context)

@login_required
def dashboard_analytics(request):

	context = {}
	return render(request, 'dashboard/dashboard.analytics.html', context)

