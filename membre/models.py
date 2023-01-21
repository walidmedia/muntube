from datetime import datetime

from django.db import models
from django.db.models.fields import json
from django.utils.html import mark_safe
from account.models import User, playlist
from django.db.models.signals import post_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer



class Video(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
	title=models.CharField(max_length=150)
	detail=models.TextField()
	vid=models.FileField(blank=True,upload_to='videos')
	miniature=models.ImageField(null=True,blank=True,upload_to='imagevid')
	n_likes=models.ManyToManyField(User, related_name='likes', blank=True)
	n_comments=models.ManyToManyField(User, related_name='comments', blank=True)
	play_lists = models.ForeignKey(playlist,on_delete=models.CASCADE,null=True, blank=True,default=False)
	categorie = models.CharField(max_length=150, blank=True, default=False)
	tags = models.CharField(max_length=150, blank=True,default=False)
	status_video = models.IntegerField(null=True, blank=True, default=0)
	#abonnements=models.ManyToManyField(User, related_name='abonnements', null=True, blank=True)
	link=models.TextField(null=True,blank=True)
	documents=models.FileField(upload_to='filesvideo', null=True, blank=True)
	date_created = models.DateTimeField(default=datetime.today)

	def __str__(self):
		return self.title

	def total_likes(self):
		return self.n_likes.count()

	def total_comments(self):
		return self.n_comments.count()

	def total_playlists(self):
		return self.play_lists.count()

	"""def total_abonnés(self):
		return self.abonnements.count()"""

	def image_tag(self):
		return mark_safe('<img src="%s" width="80" />' % (self.miniature.url))

class comment(models.Model):
	video = models.ForeignKey(Video,related_name='comments',on_delete=models.CASCADE,null=True, blank=True)
	name = models.CharField(max_length=256)
	contenue = models.TextField()
	date_added = models.DateTimeField(default=datetime.today)

	def __str__(self):
		return '%s - %s' % (self.video.title, self.name)



class savedvideo(models.Model):
	video = models.ForeignKey(Video,on_delete=models.CASCADE,null=True, blank=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
	def __str__(self):
		return '%s - %s' % (self.video.title, self.user)

"""class playlists(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
	nom_playlist = models.CharField(max_length=128)
	def __str__(self):
		return '%s - %s' % ( self.nom_playlist, self.user)"""


# Gallery Images
class GalleryVideo(models.Model):
	video=models.ForeignKey(Video, on_delete=models.CASCADE,null=True)
	alt_text=models.CharField(max_length=150)
	vid=models.FileField(upload_to='static/gallery_videos',null=True)

	def __str__(self):
		return self.alt_text

	def image_tag(self):
		return mark_safe('<img src="%s" width="80" />' % (self.img.url))

# Subscription Plans
class SubPlan(models.Model):
	title=models.CharField(max_length=150)
	price=models.IntegerField()
	max_member=models.IntegerField(null=True)
	highlight_status=models.BooleanField(default=False,null=True)
	validity_days=models.IntegerField(null=True)

	def __str__(self):
		return self.title

# Subscription Plans Features
class SubPlanFeature(models.Model):
	# subplan=models.ForeignKey(SubPlan, on_delete=models.CASCADE,null=True)
	subplan=models.ManyToManyField(SubPlan)
	title=models.CharField(max_length=150)

	def __str__(self):
		return self.title


class Banners(models.Model):
	img = models.ImageField(upload_to="banners/")
	alt_text = models.CharField(max_length=150)

	class Meta:
		verbose_name_plural = 'Banners'

	def __str__(self):
		return self.alt_text

	def image_tag(self):
		return mark_safe('<img src="%s" width="80" />' % (self.img.url))


# Create your models here.
class Service(models.Model):
	title = models.CharField(max_length=150)
	detail = models.TextField()
	img = models.ImageField(upload_to='static/services', null=True)

	def __str__(self):
		return self.title

	def image_tag(self):
		return mark_safe('<img src="%s" width="80" />' % (self.img.url))


# Pages
class Page(models.Model):
	title = models.CharField(max_length=200)
	detail = models.TextField()

	def __str__(self):
		return self.title


# FAQ
class Faq(models.Model):
	quest = models.TextField()
	ans = models.TextField()

	def __str__(self):
		return self.quest


# Enquiry Model
class Enquiry(models.Model):
	full_name = models.CharField(max_length=150)
	email = models.CharField(max_length=150)
	detail = models.TextField()
	send_time = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.full_name


# Package Discounts
class PlanDiscount(models.Model):
	subplan = models.ForeignKey(SubPlan, on_delete=models.CASCADE, null=True)
	total_months = models.IntegerField()
	total_discount = models.IntegerField()

	def __str__(self):
		return str(self.total_months)


# Subscriber
class Subscriber(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	mobile = models.CharField(max_length=20)
	address = models.TextField()
	img = models.ImageField(upload_to='static/subs', null=True)

	def __str__(self):
		return str(self.user)

	def image_tag(self):
		if self.img:
			return mark_safe('<img src="%s" width="80" />' % (self.img.url))
		else:
			return 'no-image'


@receiver(post_save, sender=User)
def create_subscriber(sender, instance, created, **kwrags):
	if created:
		Subscriber.objects.create(user=instance)


# Subscription
class Subscription(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	plan = models.ForeignKey(SubPlan, on_delete=models.CASCADE, null=True)
	price = models.CharField(max_length=50)
	reg_date = models.DateField(auto_now_add=True, null=True)


# Trainer
class Trainer(models.Model):
	full_name = models.CharField(max_length=100)
	username = models.CharField(max_length=100, null=True)
	pwd = models.CharField(max_length=50, null=True)
	mobile = models.CharField(max_length=100)
	address = models.TextField()
	is_active = models.BooleanField(default=False)
	detail = models.TextField()
	img = models.ImageField(upload_to='static/trainers')
	salary = models.IntegerField(default=0)

	facebook = models.CharField(max_length=200, null=True)
	twitter = models.CharField(max_length=200, null=True)
	pinterest = models.CharField(max_length=200, null=True)
	youtube = models.CharField(max_length=200, null=True)

	def __str__(self):
		return str(self.full_name)

	def image_tag(self):
		if self.img:
			return mark_safe('<img src="%s" width="80" />' % (self.img.url))
		else:
			return 'no-image'


# Notifications Json Response Via Ajax
class Notify(models.Model):
	notify_detail = models.TextField()
	read_by_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
	read_by_trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE, null=True, blank=True)

	def __str__(self):
		return str(self.notify_detail)


# Markas Read Notification By User
class NotifUserStatus(models.Model):
	notif = models.ForeignKey(Notify, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	status = models.BooleanField(default=False)

	class Meta:
		verbose_name_plural = 'Notification Status'


# Assign Subscriber to Trainer
class AssignSubscriber(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)

	def __str__(self):
		return str(self.user)


# Trainer Achivements
class TrainerAchivement(models.Model):
	trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)
	title = models.CharField(max_length=100)
	detail = models.TextField()
	img = models.ImageField(upload_to='static/trainers_achivements')

	def __str__(self):
		return str(self.title)

	def image_tag(self):
		if self.img:
			return mark_safe('<img src="%s" width="80" />' % (self.img.url))
		else:
			return 'no-image'


# TrainerSalary Model
class TrainerSalary(models.Model):
	trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)
	amt = models.IntegerField()
	amt_date = models.DateField()
	remarks = models.TextField(blank=True)

	class Meta:
		verbose_name_plural = 'Trainer Salary'

	def __str__(self):
		return str(self.trainer.full_name)


# Trainer Notifications
class TrainerNotification(models.Model):
	notif_msg = models.TextField()

	def __str__(self):
		return str(self.notif_msg)

	def save(self, *args, **kwargs):
		super(TrainerNotification, self).save(*args, **kwargs)
		channel_layer = get_channel_layer()
		notif = self.notif_msg
		total = TrainerNotification.objects.all().count()
		async_to_sync(channel_layer.group_send)(
			'noti_group_name', {
				'type': 'send_notification',
				'value': json.dumps({'notif': notif, 'total': total})
			}
		)


# Markas Read Notification By Trainer
class NotifTrainerStatus(models.Model):
	notif = models.ForeignKey(TrainerNotification, on_delete=models.CASCADE)
	trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)
	status = models.BooleanField(default=False)

	class Meta:
		verbose_name_plural = 'Trainer Notification Status'


# SubscriberMsg
class TrainerMsg(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE, null=True)
	message = models.TextField()

	class Meta:
		verbose_name_plural = 'Messages For Trainer'


# Reports
class TrainerSubscriberReport(models.Model):
	report_for_trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE, null=True,
										   related_name='report_for_trainer')
	report_for_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='report_for_user')
	report_from_trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE, null=True,
											related_name='report_from_trainer', blank=True)
	report_from_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='report_from_user',
										 blank=True)
	report_msg = models.TextField()


class AppSetting(models.Model):
	logo_img = models.ImageField(upload_to='static/app_logos')

	def image_tag(self):
		return mark_safe('<img src="%s" width="80" />' % (self.logo_img.url))