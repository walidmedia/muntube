from django.urls import path
from . import views
from .views import login, logout_view, register, profile, confirm_register

urlpatterns = [
    #path("", views.homepage, name="homepage"),
    #path("", views.index, name="index"),
    path("", views.maintenance, name="maintenance"),
    path("profile", profile, name="profile"),
    path('login/', login, name='login'),
    path('logout_view/', logout_view, name='logout_view'),
    path('register/', register, name='register'),
    path('confirm_register/<int:user_id>/', confirm_register, name='confirm_register'),
]
