import json
import time
from idlelib import history
import plotly.express as px
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import models
from django.db.models import Count, Q, Sum
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import get_template, render_to_string
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse, request
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from google.auth.transport import requests
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from unicodedata import decimal

from ABLACKADABRA import settings
from ABLACKADABRA.settings import AUTH_USER_MODEL
from account.models import User, UserAbonn, playlist as plist, playlist
from .forms import ChannelForm
from .models import Video as vdeo, GalleryVideo, SubPlan, SubPlanFeature, Subscription, comment as commentaire, \
	savedvideo, Don, \
	VideoHistory, Notification, Channel, Like, Like_comment, soutien as Soutien
import stripe
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from ABLACKADABRA.settings import YOUTUBE_API_KEY

youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

def channel_muntube(request):
    if request.method == 'POST':
        form = ChannelForm(request.POST)
        if form.is_valid():
            channel = form.save(commit=False)
            channel.owner = request.user
            channel.save()
            return redirect('chaine')
    else:
        form = ChannelForm()
    return render(request, 'membre/channel_muntube.html', {'form': form})


def chart_data(request):
    videos = vdeo.objects.all()
    payments = Don.objects.all()
    labels = [video.id for video in videos]
    data = [video.views for video in videos]
    user_don = [payment.user_don for payment in payments]
    amounts = [payment.cout_don for payment in payments]
    n_likes = [video.n_likes for video in videos]
    context = {
		'labels': labels,
		'data': data,
		'user_don': user_don,
		'amounts': amounts,
		'n_likes': n_likes,
	}
    return render(request, 'membre/stats.html', context)


def get_channel_videos(channel_id):
    try:
        # Call the search.list method to retrieve videos
        search_response = youtube.search().list(
            part='id,snippet',
            channelId=channel_id,
            type='video',
            maxResults=50
        ).execute()

        # Extract the video data from the response
        videos = []
        for search_result in search_response.get('items', []):
            videos.append({'id': search_result['id']['videoId'], 'title': search_result['snippet']['title']})

        return videos
    except HttpError as error:
        print(f'An error occurred: {error}')
        return None


def get_channel_videos(channel_id):
    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
    request = youtube.search().list(
        part='snippet',
        channelId=channel_id,
        type='video',
        maxResults=50
    )
    response = request.execute()
    video_ids = [item['id']['videoId'] for item in response['items']]
    videos = []
    for video_id in video_ids:
        video_request = youtube.videos().list(
            part='snippet,player,statistics',
            id=video_id
        ).execute()
        videos.append(video_request['items'][0])
    return videos

def channel_videos(request):
    videos = get_channel_videos('UCEgdi0XIXXZ-qJOFPf4JSKw')
    return render(request, 'membre/youtube.html', {'videos': videos})


# Contenu de la chaîne
@login_required
def upload(request):
	playlists = vdeo.objects.filter(user_id= request.user.id)
	play_lists = plist.objects.filter(user_playlist_id=request.user.id)
	notifs = Notification.objects.filter(recipient_id=request.user.id)

	context = {
		'play_lists' : play_lists,
		'notifs' : notifs,
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

"""@login_required
def play_video(request, video_id):
    video = get_object_or_404(vdeo, pk=video_id)
    VideoHistory.objects.create(user=request.user, video=video)
    return render(request, 'video.html', {'video': video})"""

@login_required
def view_history(request):
	history = VideoHistory.objects.filter(user=request.user).order_by('-viewed_at')
	notifs = Notification.objects.filter(recipient_id=request.user.id)
	return render(request, 'membre/historique.html', {'notifs': notifs,'history': history})

@login_required
def AddPlaylist(request):
	if request.method == "POST":
		#id_user = get_object_or_404(User, id=request.POST.get('id_user'))
		id_user = request.user.id
		playlist = request.POST.get('playlist')
		miniature = request.FILES.get('miniature')
		description = request.POST.get('description')
		play = plist(user_playlist=User.objects.get(id=id_user),nom_playlist=playlist,miniature_playlist=miniature , desc_playlist=description)
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
	notifs = Notification.objects.filter(recipient_id=request.user.id)
	play_lists = plist.objects.filter(user_playlist_id=request.user.id)
	videos = get_channel_videos('UCJO44FUePQs91aBIoS69gvg')
	context = {
		'mesvideos': mesvideos,
		'play_lists': play_lists,
		'videos': videos,
		'notifs': notifs,
	}
	return render(request, 'membre/chaine.html', context)


def machaine(request):
	notifs = Notification.objects.filter(recipient_id=request.user.id)
	context={
		'notifs': notifs,
	}
	return render(request, 'membre/machaine.html', context)


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

@login_required
def checkout_don(request,video_id):
	cout_don = request.POST.get('cout_don')
	videoDetail=vdeo.objects.get(pk=video_id)
	context = {
		'cout_don' : cout_don,
		'videoDetail' : videoDetail
	}
	return render(request, 'membre/checkout_don.html',{'don':videoDetail, 'cout_don':cout_don})

@login_required
def checkout_sess_don(request,cout_don):
	video_id = request.POST.get('video_id')
	#video = get_object_or_404(vdeo, id=request.POST.get('video_id'))
	video = get_object_or_404(vdeo, id=request.POST.get(video_id))
	session=stripe.checkout.Session.create(
		payment_method_types=['card'],
		line_items=[{
	      'price_data': {
	        'currency': 'eur',
	        'product_data': {
	          'name': video.title,
	        },
	        'unit_amount': cout_don*100,
	      },
	      'quantity': 1,
	    }],
	    mode='payment',

	    success_url='http://127.0.0.1:8000/pay_success_don?session_id={CHECKOUT_SESSION_ID}',
	    cancel_url='http://127.0.0.1:8000/pay_cancel_don',
	    client_reference_id=video.id,
	    cout_reference=cout_don
	)
	return redirect(session.url, code=303)


@login_required
def video(request,id):
	video = get_object_or_404(vdeo, pk=id)
	history_exists = VideoHistory.objects.filter(user=request.user, video=video).exists()
	if history_exists:
		pass
	else:
		VideoHistory.objects.get_or_create(user=request.user, video=video)
	"""if history_exists:
		try:
			history, created = VideoHistory.objects.get_or_create(user=request.user, video=video)
		except VideoHistory.DoesNotExist:
			history, created = VideoHistory.objects.get_or_create(user=request.user, video=video)"""

	"""if request.method == 'POST':
		time_paused = request.POST.get('time_paused', None)
		if time_paused:
			history.time_paused = float(time_paused)
			history.save()"""
	notifs = Notification.objects.filter(recipient_id=request.user.id)

	don_par_user = Don.objects.filter(user_don=video.user).aggregate(total_payments=Sum('cout_don'))

	comm = commentaire.objects.all().order_by('-n_likes')[:5]
	see_all_comm = commentaire.objects.all().order_by('-n_likes')
	video = vdeo.objects.filter(id=id)
	all_video = vdeo.objects.all()
	comments = commentaire.objects.filter(video=id).count()
	recpmanded_video = vdeo.objects.all().order_by('-n_likes')[:10]
	vues = get_object_or_404(vdeo, pk=id)
	vues.views += 1
	vues.save()
	context={
		'video' : video,
		'comments' : comments,
		'all_video' : all_video,
		'comm': see_all_comm,
		'see_all_comm': see_all_comm,
		'recpmanded_video': recpmanded_video,
		'vues': vues,
		'don_par_user': don_par_user,
	}

	return render(request, 'video.html',{'video' : video,'all_video' : all_video,'comm': see_all_comm,
	'recpmanded_video': recpmanded_video, 'comments' : comments,'vues': vues,'notifs': notifs,
										 'see_all_comm': see_all_comm,'don_par_user': don_par_user,} )


@login_required
def commenter(request,id):
	if request.method == "POST":
		video = request.POST.get('video')
		user = request.user.id
		sujet = request.POST.get('sujet')
		coment = request.POST.get('commentaire')
		c = commentaire(video=vdeo.objects.get(id=video),user=User.objects.get(id=user),name=sujet,contenue=coment)
		c.save()
		video = get_object_or_404(vdeo, id=request.POST.get('video'))
		video.n_comments.add(request.user)
		return redirect('video',id)

@login_required
def like_video(request, video_id):
	video = get_object_or_404(vdeo, id=video_id)
	user = request.user
	try:
		like = Like.objects.get(user=user, video=video)
	except Like.DoesNotExist:
		like = Like.objects.create(user=user, video=video)
		video.n_likes.add(request.user)
		video.likes += 1
		video.save()
	return JsonResponse({'likes': video.likes})


"""def like_video(request, pk):
	video = get_object_or_404(vdeo,id=request.POST.get('video_id'))
	video.n_likes.add(request.user)
	# Get the post
	post = get_object_or_404(vdeo, id=pk)

	# Check if the user has already liked the post
	user_likes = vdeo.n_likes.filter(user=request.user)
	if user_likes.exists():
		# If the user has already liked the post, remove the like
		post.likes.remove(request.user)
	else:
		# If the user has not already liked the post, add the like
		post.likes.add(request.user)
	#return HttpResponseRedirect(reverse('video',args=[str(pk)]))
	return JsonResponse({'success': True, 'like_count': post.n_likes.count()})"""

@login_required
def subscribe(request, channel_id):
    channel = Channel.objects.get(id=channel_id)
    Subscription.objects.create(user=request.user, channel=channel)
    return JsonResponse({'status': 'success'})

"""
@login_required
def like_comment(request, pk):
	commentaire = get_object_or_404(comment,id=request.POST.get('commentaire'))
	commentaire.n_likes.add(request.user)
	return HttpResponseRedirect(reverse('video',args=[str(pk)]))"""

def like_comment(request, comment_id):
    comment = get_object_or_404(commentaire, id=comment_id)
    comment_like = Like_comment.objects.create(user=request.user,commentt=comment)
    comment.likes += 1
    comment.save()
    comment_like.save()
    return JsonResponse({'likes': comment.likes})

"""@csrf_exempt
def like_comment(request, pk):
    # Check if the request method is POST
    if request.method == 'POST':
        # Get the ID of the comment to be liked from the request data

        user = request.user
        # Retrieve the comment from the database
        comment = commentaire.objects.get(pk=pk)

        # Increment the number of likes for the comment
        comment_like = Like_comment.objects.create(user=user, commentt=comment)
        comment.n_likes.add(request.user)
        comment.likes += 1
        comment.save()
        comment_like.save()

        # Return a JSON response indicating success
        return JsonResponse({'success': True})"""

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
	notifs = Notification.objects.filter(recipient_id=request.user.id)

	context = {
		'vidéosjaime':vidéosjaime,
		'notifs': notifs,
	}
	return render(request, 'membre/vidéosjaime.html', context)

@login_required
def a_regarder(request):
	videos = savedvideo.objects.filter(user = request.user)
	notifs = Notification.objects.filter(recipient_id=request.user.id)

	context = {
		'videos':videos,
		'notifs': notifs,
	}
	return render(request, 'membre/a_regarder.html', context)

@login_required
def bibliothèque(request):
	chaines = UserAbonn.objects.filter(abonnements=request.user).order_by('-id')[:5]
	notifs = Notification.objects.filter(recipient_id=request.user.id)
	channels = Channel.objects.all()
	context = {
		'chaines' : chaines,
		'notifs': notifs,
		'channels': channels,
	}
	return render(request, 'membre/bibliothèque.html', context)

@login_required
def monprofile(request, id):
	profil = User.objects.all()
	#video=Video.objects.all().order_by('-id')
	notifs = Notification.objects.filter(recipient_id=request.user.id)

	context = {
		'profil' : profil,
		'notifs': notifs,
	}
	return render(request, 'membre/account.html',context)

@login_required
def bibl_abonnements(request):
	chaine = UserAbonn.objects.filter(abonnements__in=request.user)
	notifs = Notification.objects.filter(recipient_id=request.user.id)
	context = {
		'chaine' : chaine,
		'notifs': notifs,
	}
	return render(request, 'membre/bibliothèque.html', context)


def maintenance(request):
	return render(request, 'membre/404.html')

def proced_don(request, id):
	video = get_object_or_404(vdeo, pk=id)
	notifs = Notification.objects.filter(recipient_id=request.user.id)
	amount = int(request.POST.get('don'))
	don_amount = amount *100
	return render(request, 'membre/proced_don.html',{'video':video, 'amount':amount, 'don_amount':don_amount,'notifs': notifs,})

def payment(request):
	notifs = Notification.objects.filter(recipient_id=request.user.id)
	return render(request, 'membre/payment.html',{'notifs': notifs,})

@login_required()
def charge(request, pk):
	if request.method == 'POST':
		# Get the amount from the form
		amount = int(request.POST.get('amount'))
		token = request.POST.get('stripeToken')
		video = get_object_or_404(vdeo, pk=pk)
		to_user = video.user
		# Set your secret key: remember to change this to your live secret key in production
		# See your keys here: https://dashboard.stripe.com/account/apikeys
		stripe.api_key = settings.STRIPE_SECRET_KEY

		# Create a charge: this will charge the user's card
		try:
			charge = stripe.Charge.create(
				amount=amount*100,  # amount in cents, again
				currency="eur",
				source="tok_visa",  # obtained with Stripe.js
				description="Example charge"
			)
			Don.objects.create(
				user_don=request.user,
				to_user_don=to_user,
				video=video,
				cout_don=amount
			)
			Notification.objects.create(
				recipient = to_user,
				subject = 'Vous avez reçu un don',
				message= '',
			)
			subject = 'DON MunTube'
			html_content = get_template('membre/ordermail.html').render({'title': video.title})
			from_email = 'merchab08@gmail.com'

			msg = EmailMessage(subject, html_content, from_email, [request.user.email,'ablackadabra.com@gmail.com'])
			msg.content_subtype = "html"  # Main content is now text/html
			msg.send()
		except stripe.error.CardError as e:
			# The card has been declined
			pass

		# Send the order details to the customer
		# ...

		return HttpResponseRedirect(reverse('video', args=[str(pk)]))
	return render(request, 'home.html')

def success(request):
	notifs = Notification.objects.filter(recipient_id=request.user.id)

	return render(request, 'membre/success.html',{'notifs': notifs,})

@login_required
def pay_success_don(request):
	session = stripe.checkout.Session.retrieve(request.GET['session_id'])
	cout = session.cout_reference
	user = session.client_reference_id
	#user = request.user
	Don.objects.create(
		user_don=user,
		#video=video,
		cout_don=cout
	)
	subject = 'DON MunTube'
	html_content = get_template('membre/ordermail.html').render({'title': video.title})
	from_email = 'merchab08@gmail.com'

	msg = EmailMessage(subject, html_content, from_email, [request.user.email])
	msg.content_subtype = "html"  # Main content is now text/html
	msg.send()

	return render(request, 'membre/success.html')

def mescommentaires(request):
	videos = vdeo.objects.filter(user_id= request.user.id)
	mesvideos = commentaire.objects.filter(user_id= request.user.id)
	notifs = Notification.objects.filter(recipient_id=request.user.id)

	context = {
		'videos' : videos,
		'mesvideos' : mesvideos,
		'notifs': notifs,
	}
	return render(request, 'membre/mescommentaires.html', context)

def mesnotifications(request):
	notifs = Notification.objects.filter(recipient_id= request.user.id)
	context = {
		'notifs' : notifs,
	}
	return render(request, 'membre/mesnotifications.html', context)


def display_notification(request):
	notifs = Notification.objects.filter(recipient_id=request.user.id)
	return render(request, 'base.html', {'notifs' : notifs})

def search(request):
	query = request.GET.get('q')
	if query:
		results = vdeo.objects.filter(Q(title__icontains=query) | Q(detail__icontains=query))
	else:
		results = []
	return render(request, 'search_results.html', {'results': results})

def mesdons(request):
	all_dons = Don.objects.all()
	context = {
		'all_dons' : all_dons
	}
	return render(request, 'membre/mesDons.html', context)

def soutenir(request):
	return render(request, 'soutenir.html')

@login_required()
def soutien(request):
	if request.method == 'POST':
		# Get the amount from the form
		#amount = int(request.POST.get('amount'))
		token = request.POST.get('stripeToken')
		#to_user = video.user
		# Set your secret key: remember to change this to your live secret key in production
		# See your keys here: https://dashboard.stripe.com/account/apikeys
		stripe.api_key = settings.STRIPE_SECRET_KEY

		# Create a charge: this will charge the user's card
		try:
			charge = stripe.Charge.create(
				amount=10*100,  # amount in cents, again
				currency="eur",
				source="tok_visa",  # obtained with Stripe.js
				description="Nous Soutenir"
			)
			Soutien.objects.create(
				donneur=request.user,
				amount=10
			)

			subject = 'Soutien MunTube'
			html_content = get_template('membre/ordermail.html').render({'title': 'Vous avez reçu un don!'})
			from_email = 'merchab08@gmail.com'

			msg = EmailMessage(subject, html_content, from_email, [request.user.email,'ablackadabra.com@gmail.com'])
			msg.content_subtype = "html"  # Main content is now text/html
			msg.send()
		except stripe.error.CardError as e:
			# The card has been declined
			pass

		# Send the order details to the customer
		# ...

		return HttpResponseRedirect(reverse('index'))
	return render(request, 'home.html')
