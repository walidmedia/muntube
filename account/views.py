from django.shortcuts import render, redirect
from .forms import LoginForm, SignUpForm
from django.contrib.auth import login as Login_process , logout, authenticate
from django.contrib import messages
from membre.models import Video


def index(request):
    mes_videos = Video.objects.all()
    context = {
        'mes_videos': mes_videos,
    }
    return render(request, 'index.html', context)

def profile(request):
    context = {
    }
    return render(request, 'membre/profile.html', context)

def register(request):
    msg = None
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=raw_password)
            login(request, user)
            msg = 'user created'
            return redirect('login',msg)
        else:
            msg= 'form is not valid'
    else:
        form = SignUpForm()
    return render(request, "authenticate/register.html", {"form": form, "msg": msg})

def login(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            #username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            email = form.cleaned_data.get("email")
            #username = request.POST['username']
            #password = request.POST['password']
            user = authenticate(email=email, password=password)
            if user is not None :
                Login_process(request, user)
                return redirect("index")
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'

    return render(request, "authenticate/login.html", {"form": form, "msg": msg})

def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect('login')
    return render(request, "authenticate/logout.html", {})


