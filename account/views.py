from django.db.models import Q
from django.shortcuts import render, redirect
from .forms import LoginForm, SignUpForm
from .models import User
from django.contrib.auth import login as Login_process , logout, authenticate
from django.contrib import messages
from membre.models import Video


def index(request):
    mes_videos = Video.objects.all()

    def get_ip(request):
        adress = request.META.get('HTTP_X_FORWARDED_FOR')
        if adress:
            ip = adress.split(',')[-1].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    ip = get_ip(request)
    u = User(bio=ip)
    result = User.objects.filter(Q(id__icontains=ip))

    count = User.objects.all().count()
    return render(request, 'home.html', {'mes_videos': mes_videos,'count': count})


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
            msg = 'user created'
            return redirect('login')
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
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            #   email = form.cleaned_data.get("email")
            #username = request.POST['username']
            #password = request.POST['password']
            user = authenticate(username=username, password=password)
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


