from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect
from .forms import LoginForm, SignUpForm
from .models import User
from django.contrib.auth import login as Login_process , logout, authenticate
from django.contrib import messages
from membre.models import Video, Notification, Channel


def index(request):
    notifs = Notification.objects.filter(recipient_id=request.user.id)

    trending_video = Video.objects.all()

    paginator = Paginator(trending_video, 2)

    page = request.GET.get('page')

    videos = paginator.get_page(page)

    return render(request, 'home.html', {'videos': videos,'trending_video' : trending_video, 'notifs': notifs, })


def profile(request):
    notifs = Notification.objects.filter(recipient_id=request.user.id)

    context = {
        'notifs': notifs,
    }
    return render(request, 'membre/profile.html', context)

def register(request):
    msg = None
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user=form.save()
            channel = Channel.objects.create(
                name=user.username,
                owner=user
            )
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


