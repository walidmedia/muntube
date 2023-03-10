from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from .forms import LoginForm, SignUpForm
from .models import User
from django.contrib.auth import login as Login_process , logout, authenticate
from django.contrib import messages
from membre.models import Video, Notification, Channel

def maintenance(request):
    return render(request, 'maintenance.html')

def index(request):
    notifs = Notification.objects.filter(recipient_id=request.user.id)

    trending_video = Video.objects.all()

    paginator = Paginator(trending_video, 100)

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
    form = SignUpForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get("username")
            email = form.cleaned_data.get("email")
            password1 = form.cleaned_data.get("password1")
            password2 = form.cleaned_data.get("password2")
            if password1 == password2:  # check if the passwords match
                user = form.save()
                channel = Channel.objects.create(
                    name=user.username,
                    owner=user
                )
                msg = 'user created'
                return redirect(reverse('confirm_register', kwargs={'user_id': user.id})) # Pass user ID as URL parameter
            else:
                msg = 'Passwords do not match'
    else:
        form = SignUpForm()
    return render(request, 'authenticate/register.html', {'form': form, 'msg': msg})

def confirm_register(request, user_id):
    user = User.objects.get(id=user_id)
    if request.method == 'POST':
        # Retrieve form data
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        Gender = request.POST.get('Gender')
        Gender = request.POST.get('Gender')
        date_of_birth = request.POST.get('date_of_birth')
        Country = request.POST.get('Country')
        phone_number = request.POST.get('phone_number')

        # Update user object with form data
        user.first_name = first_name
        user.last_name = last_name
        user.gender = Gender
        user.date_of_birth = date_of_birth
        user.country = Country
        user.phone_number = phone_number

        # Save user object to database
        user.save()

        return redirect('login') # Redirect to home page after form submission

    return render(request, 'authenticate/confirm_register.html', {'user': user})

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


