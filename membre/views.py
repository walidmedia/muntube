from django.contrib import messages
from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import get_template
from django.http import HttpResponseRedirect
from django.urls import reverse

from ABLACKADABRA import settings
from ABLACKADABRA.settings import AUTH_USER_MODEL
from account.models import User
from .models import Video as vdeo, GalleryVideo, SubPlan, SubPlanFeature, Subscription, comment
import stripe


# Contenu de la chaîne
def upload(request):

	return render(request, 'membre/upload.html')

def addvideo(request):
	if request.method == "POST":
		id = request.POST.get('id')
		video = request.FILES.get('video')
		image = request.FILES.get('image')
		titre = request.POST.get('titre')
		description = request.POST.get('description')
		v = vdeo(user=User.objects.get(id=id),
				 vid=video, miniature=image, detail=description, title=titre)
		v.save()
		size = video.size
		return render(request, 'index.html', {'size': size})
		#return redirect('success_upload',{'size':size})
		"""if video.size > 1000:
			v = vdeo(user=User.objects.get(id=id),
					 vid = video,img = image,detail = description,title = titre)
			v.save()
			return redirect('success_upload')
		else:
			error= "Your File not supported"
			#msg = messages.success(request, 'succéss message')
			return render(request,'membre/mesvideos.html',{'error':error})"""

def success_upload(request):
	mesvideos = vdeo.objects.filter(user_id= request.user.id)
	context={
		'mesvideos' : mesvideos
	}
	return render(request, 'membre/accueilmembre.html', context)

def mesvideos(request):
	mesvideos = vdeo.objects.filter(user_id= request.user.id)
	context={
		'mesvideos' : mesvideos
	}
	return render(request, 'membre/mesvideos.html', context)

def stockage(request):
	context={
	}
	return render(request, 'membre/stockage.html', context)

def machaine(request):
	context={
	}
	return render(request, 'membre/machaine.html', context)

# Show galleries
def Video(request):
	video=Video.objects.all().order_by('-id')
	return render(request, 'gallery.html',{'videos':video})

# Show gallery photos
def Video_detail(request,id):
	video=Video.objects.get(id=id)
	gallery_vids=GalleryVideo.objects.filter(video=video).order_by('-id')
	return render(request, 'gallery_imgs.html',{'gallery_vids':gallery_vids,'video':video})


# Subscription Plans
def stockage(request):
	plans=SubPlan.objects.annotate(total_members=Count('subscription__id')).all().order_by('price')
	dfeatures=SubPlanFeature.objects.all();
	return render(request, 'membre/stockage.html',{'plans':plans,'dfeatures':dfeatures})

# Checkout
def checkout(request,plan_id):
	planDetail=SubPlan.objects.get(pk=plan_id)
	return render(request, 'membre/checkout.html',{'plan':planDetail})

stripe.api_key=settings.STRIPE_SECRET_KEY
def checkout_session(request,plan_id):
	plan=SubPlan.objects.get(pk=plan_id)
	session=stripe.checkout.Session.create(
		payment_method_types=['card'],
		line_items=[{
	      'price_data': {
	        'currency': 'eur',
	        'product_data': {
	          'name': plan.title,
	        },
	        'unit_amount': plan.price*100,
	      },
	      'quantity': 1,
	    }],
	    mode='payment',

	    success_url='http://web-production-f55f.up.railway.app/pay_success?session_id={CHECKOUT_SESSION_ID}',
	    cancel_url='http://web-production-f55f.up.railway.app/pay_cancel',
	    client_reference_id=plan_id
	)
	return redirect(session.url, code=303)

# Success
from django.core.mail import EmailMessage

def pay_success(request):
	session = stripe.checkout.Session.retrieve(request.GET['session_id'])
	plan_id=session.client_reference_id
	plan=SubPlan.objects.get(pk=plan_id)
	user=request.user
	Subscription.objects.create(
		plan=plan,
		user=user,
		price=plan.price
	)
	subject='Order Email'
	html_content=get_template('membre/ordermail.html').render({'title':plan.title})
	from_email='dilaw0895@gmail.com'

	msg = EmailMessage(subject, html_content, from_email, [request.user.email])
	msg.content_subtype = "html"  # Main content is now text/html
	msg.send()


	return render(request, 'membre/success.html')

# Cancel
def pay_cancel(request):
	return render(request, 'membre/cancel.html')

def video(request,id):
	comm = comment.objects.all()
	video = vdeo.objects.filter(id=id)
	all_video = vdeo.objects.all()
	context={
		'video' : video,
		'all_video' : all_video,
		'comm': comm,
	}
	return render(request, 'video.html',context)

def displaycomment(request):
	comm = comment.objects.all()
	context={
		'comm' : comm,
	}
	return render(request, 'video.html',context)

def commenter(request,id):
	if request.method == "POST":
		video = request.POST.get('video')
		sujet = request.POST.get('sujet')
		coment = request.POST.get('commentaire')
		c = comment(video=vdeo.objects.get(id=video),name=sujet,contenue=coment)
		c.save()
		id=id
		return redirect('video',id)

def like_video(request, pk):
	video = get_object_or_404(vdeo,id=request.POST.get('video_id'))
	video.n_likes.add(request.user)
	return HttpResponseRedirect(reverse('video',args=[str(pk)]))

def abonni_video(request, pk):
	abonné = get_object_or_404(vdeo,id=request.POST.get('chaine_id'))
	abonné.abonnements.add(request.user)
	return HttpResponseRedirect(reverse('video',args=[str(pk)]))

def monprofile(request, id):
	profil = User.objects.all()
	#video=Video.objects.all().order_by('-id')
	context = {
		'profil' : profil,
	}
	return render(request, 'membre/account.html',context)
