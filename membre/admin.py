from django.contrib import admin

# Register your models here.
from membre import models
from membre.models import Channel, Like


class CommentAdmin(admin.ModelAdmin):
	list_display = ('video','name','contenue','date_added')
	list_filter =('video','name','contenue','date_added')
	search_fields = ('video','name','contenue','date_added')
admin.site.register(models.comment,CommentAdmin)

class VideoAdmin(admin.ModelAdmin):
	list_display=('user','title','detail','vid','miniature','play_lists','total_likes','total_comments')
admin.site.register(models.Video,VideoAdmin)

class GalleryVideoAdmin(admin.ModelAdmin):
	list_display=('alt_text','vid')
admin.site.register(models.GalleryVideo,GalleryVideoAdmin)

class SubPlanAdmin(admin.ModelAdmin):
	list_editable=('highlight_status','max_member')
	list_display=('title','price','max_member','validity_days','highlight_status')
admin.site.register(models.SubPlan,SubPlanAdmin)

class SubPlanFeatureAdmin(admin.ModelAdmin):
	list_display=('title','subplans')
	def subplans(self,obj):
		return " | ".join([sub.title for sub in obj.subplan.all()])
admin.site.register(models.SubPlanFeature,SubPlanFeatureAdmin)

class PlanDiscountAdmin(admin.ModelAdmin):
	list_display=('subplan','total_months','total_discount')
admin.site.register(models.PlanDiscount,PlanDiscountAdmin)

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

class VideoHistoryAdmin(admin.ModelAdmin):
	list_display=('user','video','viewed_at')
admin.site.register(models.VideoHistory,VideoHistoryAdmin)

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