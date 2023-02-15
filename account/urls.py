from django.urls import path
from . import views
from .views import login, logout_view, register, profile, update_user

urlpatterns = [
    #path("", views.homepage, name="homepage"),
    path("", views.index, name="index"),
    path("profile", profile, name="profile"),
    path('login/', login, name='login'),
    path('logout_view/', logout_view, name='logout_view'),
    path('register/', register, name='register'),
    path('update_user/<int:user_id>', update_user, name='update_user'),
]
