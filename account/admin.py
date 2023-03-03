from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, UserAbonn, AdsVideo

# Register your models here.


admin.site.register(UserAbonn)

class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'first_name', 'last_name', 'gender', 'photo', 'country', 'id_youtube_ch', 'Active_don','stripe_account_id')
    list_filter = ('gender', 'Active_don', 'date_joined','email', 'username', 'first_name', 'last_name', 'photo', 'country', 'id_youtube_ch','stripe_account_id')
    search_fields = ('email', 'username', 'first_name', 'last_name', 'id_youtube_ch','stripe_account_id')
    ordering = ('-date_joined',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'username', 'gender', 'date_of_birth','photo', 'country', 'bio', 'id_youtube_ch', 'Active_don','stripe_account_id')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

admin.site.register(User, CustomUserAdmin)

class AdsVideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'detail', 'content_type', 'subtitle', 'video', 'image')
    list_filter = ('content_type',)
    search_fields = ('title', 'detail', 'subtitle')

admin.site.register(AdsVideo, AdsVideoAdmin)