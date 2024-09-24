from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate

from django.shortcuts import render, redirect, get_object_or_404
# Create your view

@login_required
def home(request):
    return render(request, "home.html")

def signin(request):
    if request.user.is_authenticated:
        return redirect('home') 
    if request.method == "GET":
        return render(request, "signin.html", {"form": AuthenticationForm})
    else:
        user = authenticate(
            request,
            username=request.POST["username"],
            password=request.POST["password"],
        )
        if user is None:
            return render(
                request,
                "signin.html",
                {
                    "form": AuthenticationForm,
                    "error": "Username or password is incorrect",
                },
            )
        else:
            login(request, user)
            return redirect("home")

@login_required
def signout(request):
    logout(request)
    return redirect("signin")
