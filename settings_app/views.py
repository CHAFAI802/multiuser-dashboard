from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

def settings_home(request):
    return render(request, "settings/home.html")

def profile_settings(request):
    return render(request, "settings/profile.html")

def notification_settings(request):
    return render(request, "settings/notifications.html")
