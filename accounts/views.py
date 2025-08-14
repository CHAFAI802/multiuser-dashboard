
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import SignUpForm, LoginForm

# Vue inscription
def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("accounts:login")
    else:
        form = SignUpForm()
    return render(request, "accounts/signup.html", {"form": form})

# Vue connexion
def login_view(request):
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("dashboard:home")
    else:
        form = LoginForm()
    return render(request, "accounts/login.html", {"form": form})

# Vue déconnexion
def logout_view(request):
    logout(request)
    return redirect("accounts:login")
