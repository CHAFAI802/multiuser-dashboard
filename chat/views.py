from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def chat_home(request):
    return render(request, "chat/home.html")

@login_required
def private_chat(request, username):
    return render(request, "chat/private.html", {"username": username})

