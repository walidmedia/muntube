from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
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


@login_required
def update_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)

    if request.method == 'POST':
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.gender = request.POST.get('gender')
        user.country = request.POST.get('country')
        user.bio = request.POST.get('bio')
        user.id_youtube_ch = request.POST.get('id_youtube_ch')
        user.Active_don = request.POST.get('Active_don') == 'on'

        if request.FILES.get('photo'):
            user.photo = request.FILES['photo']

        user.save()

        messages.success(request, 'User profile updated successfully.')
        return redirect('user_profile', user_id=user_id)
    else:
        return render(request, 'membre/account.html', {'user': user})
def save_user(request):
    if request.method == 'POST':
        id_user = request.POST.get('id_user')
        img = request.POST.get('img')
        firstName = request.POST.get('firstName')
        lastName = request.POST.get('lastName')
        Pseudonyme = request.POST.get('Pseudonyme')
        email = request.POST.get('email')
        pays = request.POST.get('pays')
        bio = request.POST.get('bio')
        phoneNumber = request.POST.get('phoneNumber')
        id_ytb = request.POST.get('id_ytb')

        # Create a new User object and save it
        user = User.objects.create_user(username, email, password)
        user.save()

        return HttpResponse('User saved successfully')
    else:
        return render(request, 'membre/account.html')

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


