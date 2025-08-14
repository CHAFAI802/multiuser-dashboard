from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def dashboard_home(request):
    return render(request, "dashboard/home.html")

@login_required
def my_profile(request):
    return render(request, "dashboard/profile.html")

