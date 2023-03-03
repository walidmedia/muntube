from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
import datetime
from datetime import timedelta
from datetime import datetime as dt


### Custom User Model Used Here

class UserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of username.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


#### This is User Profile
class User(AbstractUser):
    user_gender = (
        ('Male', 'Male'),
        ('Female', 'Female')
    )
    username = models.CharField(_('Username'), max_length=100, default='', unique=True)
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200, null=True)
    gender = models.CharField(max_length=10, default='', choices=user_gender)
    date_of_birth = models.DateField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    photo = models.ImageField(upload_to='users', default="/static/images/profile1.jpg", null=True, blank=True)
    country = models.CharField(max_length=256, null=True)
    bio = models.TextField(default='', blank=True)
    id_youtube_ch = models.CharField(max_length=24, null=True,default="")
    Active_don = models.BooleanField(default=False)
    stripe_account_id = models.CharField(max_length=255, blank=True, null=True)
    stripe_account_holder_name = models.CharField(max_length=255, blank=True, null=True)
    stripe_account_number = models.CharField(max_length=255, blank=True, null=True)
    stripe_routing_number = models.CharField(max_length=255, blank=True, null=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username']

    objects = UserManager()

    def get_default_photo(self):
        return "/static/images/profile1.jpg"
    def __str__(self):
        return self.username

#### User Abonnement
class UserAbonn(models.Model):
    chaine = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    abonnements = models.ManyToManyField(User, related_name='abonnements', blank=True)


    """if not self.chaine:
        return "Anonymous"
    return self.chaine.username"""

    def total_abonnés(self):
        return self.abonnements.count()


class playlist(models.Model):
    user_playlist = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    nom_playlist = models.CharField(max_length=128,default=False)
    miniature_playlist = models.FileField(upload_to='playlist_img',null=True,blank=True)
    desc_playlist = models.CharField(max_length=512,default=False, blank=True)
    def __str__(self):
        return '%s - %s' % (self.nom_playlist, self.user_playlist)

#### This is user settings
class UserSetting(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)
    account_verified = models.BooleanField(default=False)
    verified_code = models.CharField(max_length=100, default='', blank=True)
    verification_expires = models.DateField(default=dt.now().date() + timedelta(days=settings.VERIFY_EXPIRE_DAYS))
    code_expired = models.BooleanField(default=False)
    recieve_email_notice = models.BooleanField(default=True)


#### User Payment History
class PayHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class AdsVideo(models.Model):
    CONTENT_TYPE_CHOICES = (
        ('video', 'Video'),
        ('image', 'Image'),
    )

    title = models.CharField(max_length=255, db_index=True)
    detail = models.TextField(blank=True)
    content_type = models.CharField(max_length=5, choices=CONTENT_TYPE_CHOICES, default='video')
    video = models.FileField(null=True, blank=True, upload_to='videosAds')
    image = models.ImageField(null=True, blank=True, upload_to='imagevidAds')
    subtitle = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.title




