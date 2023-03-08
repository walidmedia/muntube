from django.contrib import admin

# Register your models here.
from membre import models
from membre.models import Channel, Like, revendication, Report_comment, Report_video, Category, VideoHistory, SavedLink


class commentAdmin(admin.ModelAdmin):
    list_display = ('video','name', 'contenue', 'date_added', 'parent')
    list_filter = ('video','name', 'contenue', 'date_added', 'parent',)
    search_fields = ('video','name', 'contenue', 'date_added', 'parent')
    ordering = ('-date_added',)

admin.site.register(models.comment, commentAdmin)

class AdminVideo(admin.ModelAdmin):
    list_display = ('title', 'user', 'views', 'likes', 'category', 'play_lists', 'contenue_18')
    search_fields = ('title', 'user__username', 'category__title', 'play_lists__nom_playlist')
    list_filter = ('category', 'play_lists', 'contenue_18', 'date_created')

admin.site.register(models.Video, AdminVideo)

class VideoHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'video', 'viewed_at', 'time_paused')
    list_filter = ('user', 'viewed_at')
    search_fields = ('user__username', 'video__title')
    date_hierarchy = 'viewed_at'

admin.site.register(VideoHistory, VideoHistoryAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
admin.site.register(Category, CategoryAdmin)

admin.site.register(SavedLink)


class SubscriberAdmin(admin.ModelAdmin):
	list_display = ('user', 'image_tag', 'mobile')
admin.site.register(models.Subscriber, SubscriberAdmin)

class SubscriptionAdmin(admin.ModelAdmin):
	list_display=('user','plan','reg_date','price')
admin.site.register(models.Subscription,SubscriptionAdmin)

class SavedVideoAdmin(admin.ModelAdmin):
	list_display=('video','user')
admin.site.register(models.savedvideo,SavedVideoAdmin)

class PlaylistsAdmin(admin.ModelAdmin):
	list_display=('user_playlist','nom_playlist','miniature_playlist')
admin.site.register(models.playlist,PlaylistsAdmin)

class DonAdmin(admin.ModelAdmin):
	list_display=('user_don','to_user_don','video','cout_don','date_don')
	list_filter = ('user_don', 'to_user_don','video','cout_don','date_don')
	search_fields = ('user_don', 'to_user_don','video','cout_don','date_don')
admin.site.register(models.Don,DonAdmin)

class Reclamations_DonAdmin(admin.ModelAdmin):
	list_display=('user_don','to_user_don','video','cout_don','date_don')
	list_filter = ('user_don', 'to_user_don','video','cout_don','date_don')
	search_fields = ('user_don', 'to_user_don','video','cout_don','date_don')
admin.site.register(models.Reclamations_Don,DonAdmin)

class NotificationAdmin(admin.ModelAdmin):
	list_display=('recipient','subject','message','read','timestamp')
admin.site.register(models.Notification,NotificationAdmin)

class ChannelAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'owner','image','cover_image', 'created_at', 'updated_at')
    list_filter = ('owner', 'created_at', 'updated_at')
    search_fields = ('name', 'description', 'owner__username')

admin.site.register(models.Channel, ChannelAdmin)

class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'video', 'created_at')
    list_filter = ('user', 'video', 'created_at')
    search_fields = ('user', 'video', 'created_at')

admin.site.register(models.Like, LikeAdmin)

class Subscription_channelAdmin(admin.ModelAdmin):
    list_display = ('user', 'channel', 'subscribed_at')
    list_filter = ('user', 'channel', 'subscribed_at')
    search_fields = ('user', 'channel', 'subscribed_at')
admin.site.register(models.Subscription_channel, Subscription_channelAdmin)

class Like_commentAdmin(admin.ModelAdmin):
    list_display = ('user', 'commentt', 'created_at')
    list_filter = ('user', 'commentt', 'created_at')
    search_fields = ('user', 'commentt', 'created_at')
admin.site.register(models.Like_comment, Like_commentAdmin)

class RevendicationAdmin(admin.ModelAdmin):
    list_display = ('pseudonyme', 'prenom', 'nom', 'email', 'date', 'pays', 'phone_number', 'message','date_created')
    list_filter = ('date_created', 'pays')
    search_fields = ('pseudonyme', 'email', 'phone_number', 'message')

admin.site.register(revendication, RevendicationAdmin)

class Report_commentAdmin(admin.ModelAdmin):
    list_display = ('id', 'commentt', 'user', 'date_reported')
    list_filter = ('user',)
    search_fields = ('comment__name', 'user__username')

admin.site.register(Report_comment, Report_commentAdmin)

class Report_videoAdmin(admin.ModelAdmin):
    list_display = ('id', 'video', 'reporter', 'reason', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('video__title', 'reporter__username')
    ordering = ('-created_at',)

admin.site.register(Report_video, Report_videoAdmin)