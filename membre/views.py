from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import get_template, render_to_string
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.decorators import method_decorator

from ABLACKADABRA import settings
from ABLACKADABRA.settings import AUTH_USER_MODEL
from account.models import User, UserAbonn, playlist as plist, playlist
from .models import Video as vdeo, GalleryVideo, SubPlan, SubPlanFeature, Subscription, comment, savedvideo
import stripe

# Contenu de la chaîne
@login_required
def upload(request):
	playlists = vdeo.objects.filter(user_id= request.user.id)
	play_lists = plist.objects.filter(user_playlist_id=request.user.id)
	context = {
		'play_lists' : play_lists,
	}
	return render(request, 'membre/upload.html',context)

@login_required
def addvideo(request):
	if request.method == "POST":
		id = request.POST.get('id')
		video = request.FILES.get('video')
		image = request.FILES.get('image')
		titre = request.POST.get('titre')
		description = request.POST.get('description')
		categorie = request.POST.get('categorie')
		play_lists = get_object_or_404(playlist, id=request.POST.get('play_list'))
		tags = request.POST.get('tags')
		status_video = request.POST.get('statut')
		v = vdeo(user=User.objects.get(id=id),
				 vid=video, miniature=image, detail=description, title=titre,categorie=categorie,
				 play_lists=play_lists,tags=tags,status_video=status_video)
		v.save()
		#size = video.size
		#return render(request, 'home.html')
		return redirect('chaine')
		"""if video.size > 1000:
			v = vdeo(user=User.objects.get(id=id),
					 vid = video,img = image,detail = description,title = titre)
			v.save()
			return redirect('success_upload')
		else:
			error= "Your File not supported"
			#msg = messages.success(request, 'succéss message')
			return render(request,'membre/mesvideos.html',{'error':error})"""

@login_required
def AddPlaylist(request):
	if request.method == "POST":
		id_user = get_object_or_404(User, id=request.POST.get('id'))
		playlist = request.POST.get('playlist')
		miniature = request.FILES.get('miniature')
		description = request.POST.get('description')
		play = plist(user_playlist=id_user,
				 nom_playlist=playlist,miniature_playlist=miniature , desc_playlist=description)
		play.save()
		return redirect('chaine')
		#return render(request, 'home.html')

@login_required
def success_upload(request):
	mesvideos = vdeo.objects.filter(user_id= request.user.id)
	context={
		'mesvideos' : mesvideos
	}
	return render(request, 'membre/accueilmembre.html', context)

@login_required
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

@login_required
def chaine(request):
	mesvideos = vdeo.objects.filter(user_id=request.user.id)
	play_lists = plist.objects.filter(user_playlist_id=request.user.id)
	context = {
		'mesvideos': mesvideos,
		'play_lists': play_lists,
	}
	return render(request, 'membre/chaine.html', context)


def machaine(request):
	context={
	}
	return render(request, 'membre/machaine.html', context)

# Show galleries
@login_required
def Video(request):
	video=Video.objects.all().order_by('-id')
	return render(request, 'gallery.html',{'videos':video})

# Show gallery photos
@login_required
def Video_detail(request,id):
	video=Video.objects.get(id=id)
	gallery_vids=GalleryVideo.objects.filter(video=video).order_by('-id')
	return render(request, 'gallery_imgs.html',{'gallery_vids':gallery_vids,'video':video})


# Subscription Plans
@login_required
def stockage(request):
	plans=SubPlan.objects.annotate(total_members=Count('subscription__id')).all().order_by('price')
	dfeatures=SubPlanFeature.objects.all();
	return render(request, 'membre/stockage.html',{'plans':plans,'dfeatures':dfeatures})

# Checkout
@login_required
def checkout(request,plan_id):
	planDetail=SubPlan.objects.get(pk=plan_id)
	return render(request, 'membre/checkout.html',{'plan':planDetail})

stripe.api_key=settings.STRIPE_SECRET_KEY
@login_required
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

	    success_url='http://127.0.0.1:8000/pay_success?session_id={CHECKOUT_SESSION_ID}',
	    cancel_url='http://127.0.0.1:8000/pay_cancel',
	    client_reference_id=plan_id
	)
	return redirect(session.url, code=303)

# Success
from django.core.mail import EmailMessage
@login_required
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
	subject = 'ABLACHADABRA MunTube'
	html_content = get_template('membre/ordermail.html').render({'title': plan.title})
	from_email = 'dilaw0895@gmail.com'

	msg = EmailMessage(subject, html_content, from_email, [request.user.email])
	msg.content_subtype = "html"  # Main content is now text/html
	msg.send()

	return render(request, 'membre/success.html')

# Cancel
@login_required
def pay_cancel(request):
	return render(request, 'membre/cancel.html')


def video(request,id):
	comm = comment.objects.all()
	video = vdeo.objects.filter(id=id)
	all_video = vdeo.objects.all()
	recpmanded_video = vdeo.objects.all().order_by('-n_likes')[:10]
	context={
		'video' : video,
		'all_video' : all_video,
		'comm': comm,
		'recpmanded_video': recpmanded_video,
	}
	return render(request, 'video.html',context)

@login_required
def commenter(request,id):
	if request.method == "POST":
		video = request.POST.get('video')
		sujet = request.POST.get('sujet')
		coment = request.POST.get('commentaire')
		c = comment(video=vdeo.objects.get(id=video),name=sujet,contenue=coment)
		c.save()
		id=id
		return redirect('video',id)

@login_required
def like_video(request, pk):
	video = get_object_or_404(vdeo,id=request.POST.get('video_id'))
	video.n_likes.add(request.user)
	return HttpResponseRedirect(reverse('video',args=[str(pk)]))

@login_required
def abonni_video(request, pk):
	chaine_chaine = get_object_or_404(UserAbonn,id=request.POST.get('chaine_id'))
	userr = User.objects.filter(id=chaine_chaine.id)
	chaine_chaine.abonnements.add(userr)
	if userr.exists():
		chaine_chaine.abonnements.add(request.user)
		return HttpResponseRedirect(reverse('video', args=[str(pk)]))
	else:
		chaine = UserAbonn.objects.create(
			chaine=request.POST.get('chaine_id'),
			abonnements = request.user
		)
		chaine.abonnements.add(request.user)
		return HttpResponseRedirect(reverse('video', args=[str(pk)]))

@login_required
def save_video(request, pk):
	if request.method == "POST":
		video = get_object_or_404(vdeo,id=request.POST.get('id_video'))
		user = User.objects.get(id=request.user.id)
		c = savedvideo(video=video, user=user)
		c.save()
		return HttpResponseRedirect(reverse('video',args=[str(pk)]))

def vidéosjaime(request):
	vidéosjaime = vdeo.objects.filter(n_likes=request.user)
	context = {
		'vidéosjaime':vidéosjaime,
	}
	return render(request, 'membre/vidéosjaime.html', context)

@login_required
def a_regarder(request):
	videos = savedvideo.objects.filter(user = request.user)
	context = {
		'videos':videos,
	}
	return render(request, 'membre/a_regarder.html', context)

@login_required
def bibliothèque(request):
	chaines = UserAbonn.objects.filter(abonnements=request.user).order_by('-id')[:5]
	context = {
		'chaines' : chaines,
	}
	return render(request, 'membre/bibliothèque.html', context)

@login_required
def monprofile(request, id):
	profil = User.objects.all()
	#video=Video.objects.all().order_by('-id')
	context = {
		'profil' : profil,
	}
	return render(request, 'membre/account.html',context)

@login_required
def bibl_abonnements(request):
	chaine = UserAbonn.objects.filter(abonnements__in=request.user)
	context = {
		'chaine' : chaine
	}
	return render(request, 'membre/bibliothèque.html', context)


def maintenance(request):
	return render(request, 'membre/404.html')
