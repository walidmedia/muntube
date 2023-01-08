from django.contrib import admin

# Register your models here.
from membre import models


class VideoAdmin(admin.ModelAdmin):
	list_display=('user','title','detail','vid','img')
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