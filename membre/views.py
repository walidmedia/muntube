import json
import time
import uuid
from functools import reduce
import plotly.express as px
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import models, transaction
from django.db.models import Count, Q, Sum
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import get_template, render_to_string
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse, request, HttpResponseNotAllowed, \
    HttpResponseForbidden
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.html import strip_tags
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.views.decorators.http import require_POST, require_http_methods
from google.auth.transport import requests
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from unicodedata import decimal

from ABLACKADABRA import settings
from ABLACKADABRA.settings import AUTH_USER_MODEL, STRIPE_SECRET_KEY
from account.models import User, UserAbonn, playlist as plist, playlist, AdsVideo
from .forms import ChannelForm, CommentForm
from .models import Video as vdeo, GalleryVideo, SubPlan, SubPlanFeature, Subscription, comment as commentaire, \
    savedvideo, Don, \
    VideoHistory, Notification, Channel, Like, Like_comment, soutien as Soutien, Channel, revendication as revendq, \
    Subscription_channel, Report_comment, Report_video, Category, Video, Reclamations_Don, SavedLink
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

def update_channel(request):
    channel = Channel.objects.get(owner=request.user)

    return render(request, 'membre/update_channel.html', {'channel': channel})

@login_required
def publier_info_gene(request):
    channel = Channel.objects.get(owner=request.user)

    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        image = request.FILES.get('image')
        cover_image = request.FILES.get('cover')

        # Update the channel instance with new information
        channel.name = name
        channel.description = description
        if image:
            channel.image = image
        if cover_image:
            channel.cover_image = cover_image
        channel.save()

        messages.success(request, 'Les informations de la chaine ont été mises à jour.')

        return redirect('publier_info_gene')  # Replace 'nom_de_la_vue' with the name of the view to redirect after form submission

    context = {'channel': channel}
    return render(request, 'membre/update_channel.html', context)  # Replace 'nom_du_template.html' with the name of the HTML template to render the form

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


"""def get_channel_videos(channel_id):
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
"""


def get_channel_videos(channel_id):
    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
    request = youtube.search().list(
        part='snippet',
        channelId=channel_id,
        type='video,liveStream',
        maxResults=50,
        order='date'
    )
    response = request.execute()
    video_ids = []
    videos = []
    live_videos = []
    for item in response['items']:
        if item['id'].get('videoId'):
            video_ids.append(item['id']['videoId'])
        elif item['id'].get('liveStreamId'):
            video_ids.append(item['id']['liveStreamId'])
    for video_id in video_ids:
        video_request = youtube.videos().list(
            part='snippet,player,statistics',
            id=video_id
        ).execute()
        video = video_request['items'][0]
        if video['snippet'].get('liveBroadcastContent', '') == 'live':
            live_videos.append(video)
        else:
            videos.append(video)
    return videos, live_videos


# Contenu de la chaîne
@login_required
def upload(request):
    playlists = vdeo.objects.filter(user_id=request.user.id)
    play_lists = plist.objects.filter(user_playlist_id=request.user.id)
    notifs = Notification.objects.filter(recipient_id=request.user.id)
    categorys = Category.objects.all()

    # Check if this is the user's first video upload
    first_upload = Video.objects.filter(user=request.user).count() == 0

    context = {
        'play_lists': play_lists,
        'notifs': notifs,
        'categorys': categorys,
        'first_upload': first_upload
    }
    return render(request, 'membre/upload.html', context)


@login_required
@login_required
def addvideo(request):
    if request.method == "POST":
        id = request.POST.get('id')
        video = request.FILES.get('video')
        image = request.FILES.get('image')
        titre = request.POST.get('titre')
        description = request.POST.get('description')
        categorie_id = request.POST.get('categorie')
        play_list_id = request.POST.get('play_list')
        tags = request.POST.get('tags')
        contenue_18 = request.POST.get('contenue_18') == 'on'
        status_video = request.POST.get('status_video')
        links = request.POST.get('links')  # get list of links
        documents = request.FILES.get('documents')  # get list of documents

        # check if category and playlist are provided, otherwise create default ones
        if categorie_id:
            categorie = Category.objects.get(id=categorie_id)
        else:
            categorie, created = Category.objects.get_or_create(
                name='Non Classés',
            )

        if play_list_id:
            play_lists = playlist.objects.get(id=play_list_id)
        else:
            play_lists, created = playlist.objects.get_or_create(
                nom_playlist='Non Classés',
                user_playlist=request.user,
            )

        with transaction.atomic():
            # create the Video object
            v = Video.objects.create(
                user=User.objects.get(id=id),
                vid=video,
                miniature=image,
                detail=description,
                title=titre,
                category=categorie,
                play_lists=play_lists,
                tags=tags,
                status_video=status_video,
                contenue_18=contenue_18,
                link=links,
                documents=documents,
            )


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

def progress_view(request):
    progress = 0
    if request.is_ajax():
        progress = int(request.GET.get('progress', 0))
        if progress > 100:
            progress = 100

    data = {
        'progress': progress
    }

    return JsonResponse(data)


@login_required
def view_history(request):
    history = VideoHistory.objects.filter(user=request.user).order_by('-viewed_at')
    notifs = Notification.objects.filter(recipient_id=request.user.id)
    return render(request, 'membre/historique.html', {'notifs': notifs, 'history': history})


@login_required
def AddPlaylist(request):
    if request.method == 'POST':
        user = request.user  # Assuming the user is logged in
        nom_playlist = request.POST['nom_playlist']
        miniature_playlist = request.FILES['miniature_playlist']
        desc_playlist = request.POST['desc_playlist']

        # Create a new playlist instance and save it to the database
        new_playlist = playlist(user_playlist=user, nom_playlist=nom_playlist, miniature_playlist=miniature_playlist,
                                desc_playlist=desc_playlist)
        new_playlist.save()

        return redirect('chaine')  # Assuming you have a playlist page to redirect to
    else:
        return render(request, 'home.html')


@login_required
def success_upload(request):
    mesvideos = vdeo.objects.filter(user_id=request.user.id)
    context = {
        'mesvideos': mesvideos
    }
    return render(request, 'membre/accueilmembre.html', context)


@login_required
def mesvideos(request):
    mesvideos = vdeo.objects.filter(user_id=request.user.id)
    context = {
        'mesvideos': mesvideos
    }
    return render(request, 'membre/mesvideos.html', context)


def stockage(request):
    context = {
    }
    return render(request, 'membre/stockage.html', context)


@login_required
def chaine(request):
    mesvideos = vdeo.objects.filter(user_id=request.user.id)
    notifs = Notification.objects.filter(recipient_id=request.user.id)
    play_lists = plist.objects.filter(user_playlist_id=request.user.id)
    videos, live_videos = get_channel_videos(request.user.id_youtube_ch)
    chaines = Channel.objects.filter(owner=request.user.id)
    channel = Channel.objects.get(owner=request.user.id)
    context = {
        'mesvideos': mesvideos,
        'play_lists': play_lists,
        'videos': videos,
        'live_videos': live_videos,
        'notifs': notifs,
        'chaines': chaines,
        'channel': channel,
    }
    return render(request, 'membre/chaine.html', context)


def machaine(request):
    notifs = Notification.objects.filter(recipient_id=request.user.id)
    context = {
        'notifs': notifs,
    }
    return render(request, 'membre/machaine.html', context)


# Subscription Plans
@login_required
def stockage(request):
    plans = SubPlan.objects.annotate(total_members=Count('subscription__id')).all().order_by('price')
    dfeatures = SubPlanFeature.objects.all();
    return render(request, 'membre/stockage.html', {'plans': plans, 'dfeatures': dfeatures})


# Checkout
@login_required
def checkout(request, plan_id):
    planDetail = SubPlan.objects.get(pk=plan_id)
    return render(request, 'membre/checkout.html', {'plan': planDetail})


stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required
def checkout_session(request, plan_id):
    plan = SubPlan.objects.get(pk=plan_id)
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'eur',
                'product_data': {
                    'name': plan.title,
                },
                'unit_amount': plan.price * 100,
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
from django.core.mail import EmailMessage, send_mail


@login_required
def pay_success(request):
    session = stripe.checkout.Session.retrieve(request.GET['session_id'])
    plan_id = session.client_reference_id
    plan = SubPlan.objects.get(pk=plan_id)
    user = request.user
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
def checkout_don(request, video_id):
    cout_don = request.POST.get('cout_don')
    videoDetail = vdeo.objects.get(pk=video_id)
    context = {
        'cout_don': cout_don,
        'videoDetail': videoDetail
    }
    return render(request, 'membre/checkout_don.html', {'don': videoDetail, 'cout_don': cout_don})


@login_required
def checkout_sess_don(request, cout_don):
    video_id = request.POST.get('video_id')
    # video = get_object_or_404(vdeo, id=request.POST.get('video_id'))
    video = get_object_or_404(vdeo, id=request.POST.get(video_id))
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'eur',
                'product_data': {
                    'name': video.title,
                },
                'unit_amount': cout_don * 100,
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


def get_random_advertisement_video():
    pass


"""@login_required
def video(request, id):
    request.session['videos_watched_count'] = 0
    video = get_object_or_404(vdeo, pk=id)
    history_exists = VideoHistory.objects.filter(user=request.user, video=video).exists()
    if history_exists:
        pass
    else:
        VideoHistory.objects.create(user=request.user, video=video)
        request.session['videos_watched_count'] = request.session.get('videos_watched_count', 0) + 1

    videos_watched_count = request.session.get('videos_watched_count', 0)
    notifs = Notification.objects.filter(recipient_id=request.user.id)
    user = get_object_or_404(User, pk=video.user.id)
    don_par_user = Don.objects.filter(user_don=video.user).aggregate(total_payments=Sum('cout_don'))
    user_video = video.user
    chaine = Channel.objects.get(owner=user)
    comm = commentaire.objects.all()
    see_all_comm = commentaire.objects.all().order_by('-likes')
    video = vdeo.objects.filter(id=id)
    all_video = vdeo.objects.all()
    total_abonnés = Subscription_channel.objects.filter(channel=chaine).count()
    comments = commentaire.objects.filter(video=id).count()
    is_subscribed = False

    try:
        subscription = Subscription_channel.objects.get(
            user_id=request.user.id,
            channel_id=chaine.id,
        )
        is_subscribed = subscription.is_subscribed
    except Subscription_channel.DoesNotExist:
        # Subscription does not exist, set is_subscribed to False
        is_subscribed = False
    video_tag = vdeo.objects.get(pk=id)
    tags = video_tag.tags.split(",") if video_tag.tags else []  # split tags by comma and create list
    recpmanded_video = vdeo.objects.all().order_by('-n_likes')[:10]
    vues = get_object_or_404(vdeo, pk=id)
    vues.views += 1
    vues.save()

    # Check if it's time to display the ad video
    videos_watched_count = VideoHistory.objects.filter(user=request.user).count()
    print(f"Videos watched count: {videos_watched_count}")  # Debugging line, remove later

    if videos_watched_count % 2 == 0:
        ads_video = AdsVideo.objects.get(id=1)
        context = {
            'video': video,
            'comments': comments,
            'all_video': all_video,
            'comm': see_all_comm,
            'see_all_comm': see_all_comm,
            'recpmanded_video': recpmanded_video,
            'vues': vues,
            'don_par_user': don_par_user,
            'chaine': chaine,
            'is_subscribed': is_subscribed,
            'total_abonnés': total_abonnés,
            'tags': tags,
            'ads_video': ads_video,
        }
        videos_watched_count += 1
    else:
        context = {
            'video': video,
            'comments': comments,
            'all_video': all_video,
            'comm': see_all_comm,
            'see_all_comm': see_all_comm,
            'recpmanded_video': recpmanded_video,
            'vues': vues,
            'don_par_user': don_par_user,
            'chaine': chaine,
            'is_subscribed': is_subscribed,
            'total_abonnés': total_abonnés,
            'tags': tags,
        }
        videos_watched_count += 1
    request.session['videos_watched_count'] = videos_watched_count
    return render(request, 'video.html', context)
"""
@login_required
def video(request, id):
    video = get_object_or_404(vdeo, pk=id)

    history_exists = VideoHistory.objects.filter(user=request.user, video=video).exists()
    if not history_exists:
        VideoHistory.objects.create(user=request.user, video=video)

    videos_watched_count = VideoHistory.objects.filter(user=request.user).count()
    if videos_watched_count % 3 == 0:
        bool_watch = True
    else:
        bool_watch = False
    print(f"Videos watched count: {videos_watched_count}")  # Debugging line, remove later

    # Determine which ad to display
    ad_number = videos_watched_count % 3 + 1
    if ad_number == 1:
        ads_video = AdsVideo.objects.get(id=1)
    elif ad_number == 2:
        ads_video = AdsVideo.objects.get(id=2)
    else:
        ads_video = AdsVideo.objects.get(id=3)

    vues = get_object_or_404(vdeo, pk=id)
    vues.views += 1
    vues.save()

    user = get_object_or_404(User, pk=video.user.id)
    don_par_user = Don.objects.filter(user_don=video.user).aggregate(total_payments=Sum('cout_don'))
    user_video = video.user
    chaine = Channel.objects.get(owner=user)
    comm = commentaire.objects.all()
    see_all_comm = commentaire.objects.all().order_by('-likes')
    video = vdeo.objects.filter(id=id)
    all_video = vdeo.objects.all()
    total_abonnés = Subscription_channel.objects.filter(channel=chaine).count()
    comments = commentaire.objects.filter(video=id).count()
    is_subscribed = False

    try:
        subscription = Subscription_channel.objects.get(
            user_id=request.user.id,
            channel_id=chaine.id,
        )
        is_subscribed = subscription.is_subscribed
    except Subscription_channel.DoesNotExist:
        # Subscription does not exist, set is_subscribed to False
        is_subscribed = False

    video_tag = vdeo.objects.get(pk=id)
    tags = video_tag.tags.split(",") if video_tag.tags else []  # split tags by comma and create list
    recpmanded_video = vdeo.objects.all().order_by('-n_likes')[:10]

    if videos_watched_count % 3 == 0:
        context = {
            'video': video,
            'comments': comments,
            'all_video': all_video,
            'comm': see_all_comm,
            'see_all_comm': see_all_comm,
            'recpmanded_video': recpmanded_video,
            'vues': vues,
            'don_par_user': don_par_user,
            'chaine': chaine,
            'is_subscribed': is_subscribed,
            'total_abonnés': total_abonnés,
            'tags': tags,
            'ads_video': ads_video,
            'bool_watch': bool_watch,
        }
    else:
        context = {
            'video': video,
            'comments': comments,
            'all_video': all_video,
            'comm': see_all_comm,
            'see_all_comm': see_all_comm,
            'recpmanded_video': recpmanded_video,
            'vues': vues,
            'don_par_user': don_par_user,
            'chaine': chaine,
            'is_subscribed': is_subscribed,
            'total_abonnés': total_abonnés,
            'tags': tags,
            'bool_watch': bool_watch,
        }
        videos_watched_count += 1
    request.session['videos_watched_count'] = videos_watched_count

    return render(request, 'video.html', context)

def increment_videos_watched_count(request):
    if request.is_ajax() and request.method == 'POST':
        videos_watched_count = request.session.get('videos_watched_count', 0)
        request.session['videos_watched_count'] = videos_watched_count + 1
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False})

def get_playlist_videos(request, playlist_id):
    playlist = plist.objects.get(id=playlist_id)
    videos = Video.objects.filter(play_lists=playlist)
    first_video = videos.first()
    rest_videos = videos.exclude(id=first_video.id)
    user = get_object_or_404(User, pk=playlist.user_playlist.id)
    chaine = Channel.objects.get(owner=user)

    response = {
        'playlist': playlist,
        'chaine': chaine,
        'first_video': first_video,
        'videos': videos,
        'rest_videos': rest_videos,
        'rest_videos': rest_videos,
    }
    return render(request, 'membre/videos_playlist.html', response)


@login_required
def commenter(request, id):
    if request.method == "POST":
        video = request.POST.get('video')
        user = request.user
        sujet = request.POST.get('sujet')
        coment = request.POST.get('commentaire')
        c = commentaire(video=vdeo.objects.get(id=video), user=user, name=sujet, contenue=coment)
        c.save()
        video_obj = get_object_or_404(vdeo, id=video)
        video_obj.n_comments.add(user)

        # Create notification for video owner
        recipient = video_obj.user
        subject = f"Nouveau commentaire sur votre vidéo"
        message = f"{user.username} a commenté ta vidéo '{video_obj.title}': {coment}"
        notification = Notification(recipient=recipient, subject=subject, message=message)
        notification.save()

        return redirect('video', id)


def reply_comment(request, pk):
    parent_comment = get_object_or_404(commentaire, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.parent = parent_comment
            comment.save()
            return redirect('video_detail', pk=parent_comment.video.pk)
    else:
        form = CommentForm()
    return render(request, 'reply_comment.html', {'form': form})


@login_required
def like_video(request, video_id):
    video = get_object_or_404(vdeo, id=video_id)
    user = request.user
    is_liked = False

    try:
        # Try to get an existing like object
        like = Like.objects.get(user=user, video=video)
        like.delete()
    except Like.DoesNotExist:
        # If the user has not liked the video yet, create a new like object
        like = Like.objects.create(user=user, video=video)
        is_liked = True
        user = video.user
        if user != request.user:
            subject = f'{request.user.username} aime votre vidéo'
            message = f'{request.user.username} à aimé votre vidéo "{video.title}".'
            notification = Notification(recipient=user, subject=subject, message=message)
            notification.save()

    # Set the video's likes count to the number of likes on it
    video.likes = Like.objects.filter(video=video).count()
    video.save()

    # Return the updated number of likes and the user's current like status
    return JsonResponse({'likes': video.likes, 'is_liked': is_liked})



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


@csrf_exempt
@login_required
def like_comment(request, comment_id):
    print(comment_id)
    if request.method == 'POST':
        data = json.loads(request.body)
        comment = commentaire.objects.get(id=comment_id)
        user = request.user
        liked = data.get('liked')

        if isinstance(user, User):
            like, created = Like_comment.objects.get_or_create(user=user, commentt=comment)

            if liked:
                comment.likes += 1
                comment.n_likes.add(user)
                action = 'like'
            else:
                comment.likes -= 1
                comment.n_likes.remove(user)
                action = 'unlike'
                like.delete()

            comment.save()
            return JsonResponse({'likes': comment.likes, 'action': action})
        else:
            return JsonResponse({'error': 'User is not authenticated.'}, status=401)
    else:
        return HttpResponseNotAllowed(['POST'])



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
def subscribe(request):
    if request.method == 'POST':
        channel_id = request.POST.get('channel_id')
        user = request.user

        # Check if the user is already subscribed
        if user in UserAbonn.objects.get(chaine_id=channel_id).abonnements.all():
            return JsonResponse({'success': False})

        # If not, add the subscription and return a success response
        UserAbonn.objects.get(chaine_id=channel_id).abonnements.add(user)
        return JsonResponse({'success': True})


@login_required
def save_video(request, pk):
    if request.method == "POST":
        video = get_object_or_404(vdeo, id=request.POST.get('id_video'))
        user = User.objects.get(id=request.user.id)
        c = savedvideo(video=video, user=user)
        c.save()
        return HttpResponseRedirect(reverse('video', args=[str(pk)]))

@login_required
def save_video(request, pk):
    if request.method == "POST":
        video = get_object_or_404(vdeo, id=request.POST.get('id_video'))
        user = User.objects.get(id=request.user.id)
        c = savedvideo(video=video, user=user)
        c.save()
        return HttpResponseRedirect(reverse('video', args=[str(pk)]))

@login_required
@require_POST
def save_link(request):
    link = request.POST.get('link')
    print(link)
    print('liiiiiiiiiiiiiinkkkkkkkkkkkkkkkkkk')
    if link:
        SavedLink.objects.create(user=request.user, link=link)
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False})


def vidéosjaime(request):
    vidéosjaime = vdeo.objects.filter(n_likes=request.user)
    notifs = Notification.objects.filter(recipient_id=request.user.id)

    context = {
        'vidéosjaime': vidéosjaime,
        'notifs': notifs,
    }
    return render(request, 'membre/vidéosjaime.html', context)


@login_required
def a_regarder(request):
    videos = savedvideo.objects.filter(user=request.user)
    notifs = Notification.objects.filter(recipient_id=request.user.id)

    context = {
        'videos': videos,
        'notifs': notifs,
    }
    return render(request, 'membre/a_regarder.html', context)


@login_required
def bibliothèque(request):
    chaines = UserAbonn.objects.filter(abonnements=request.user).order_by('-id')[:5]
    notifs = Notification.objects.filter(recipient_id=request.user.id)
    abonnements = Subscription_channel.objects.filter(user=request.user)
    channels = Channel.objects.all()

    links = SavedLink.objects.filter(user=request.user)[:10]
    context = {
        'chaines': chaines,
        'notifs': notifs,
        'channels': abonnements,
        'links': links,
    }
    return render(request, 'membre/bibliothèque.html', context)


@login_required
def monprofile(request, user_id):
    profil = User.objects.get(pk=user_id)
    # video=Video.objects.all().order_by('-id')
    notifs = Notification.objects.filter(recipient_id=request.user.id)

    context = {
        'profil': profil,
        'notifs': notifs,
    }
    return render(request, 'membre/account.html', context)


@login_required
def bibl_abonnements(request):
    chaine = UserAbonn.objects.filter(abonnements__in=request.user)
    notifs = Notification.objects.filter(recipient_id=request.user.id)
    context = {
        'chaine': chaine,
        'notifs': notifs,
    }
    return render(request, 'membre/bibliothèque.html', context)


def maintenance(request):
    return render(request, 'membre/404.html')


def proced_don(request, id):
    video = get_object_or_404(vdeo, pk=id)
    notifs = Notification.objects.filter(recipient_id=request.user.id)
    amount = int(request.POST.get('don').split('€')[0])
    don_amount = amount * 100
    return render(request, 'membre/proced_don.html',
                  {'video': video, 'amount': amount, 'don_amount': don_amount, 'notifs': notifs, })


def payment(request):
    notifs = Notification.objects.filter(recipient_id=request.user.id)
    return render(request, 'membre/payment.html', {'notifs': notifs, })


@login_required()
def charge(request, pk):
    if request.method == 'POST':
        # Get the amount from the form
        amount = int(request.POST.get('amount'))
        token = request.POST.get('stripeToken')
        video = get_object_or_404(Video, pk=pk)
        to_user = video.user
        # Set your secret key: remember to change this to your live secret key in production
        # See your keys here: https://dashboard.stripe.com/account/apikeys
        stripe.api_key = settings.STRIPE_SECRET_KEY
        account = stripe.Account.retrieve(to_user.stripe_account_id)

        # Check if to_user or stripe_account_id is None
        if not to_user or not to_user.stripe_account_id:
            charge = stripe.Charge.create(
                amount=amount * 100,  # amount in cents, again
                currency="eur",
                source="tok_visa",  # obtained with Stripe.js
                description="Example charge"
            )
            Reclamations_Don.objects.create(
                user_don=request.user,
                to_user_don=to_user,
                video=video,
                cout_don=amount
            )
            Notification.objects.create(
                recipient=to_user,
                subject='Vous avez un don mais non completé',
                message='',
            )
            subject = 'DON MunTube'
            html_content = get_template('membre/ordermail.html').render({'title': video.title})
            from_email = 'merchab08@gmail.com'

            msg = EmailMessage(subject, html_content, from_email,
                               [request.user.email, 'ablackadabra.com@gmail.com'])
            msg.content_subtype = "html"  # Main content is now text/html
            msg.send()
            return redirect('success')

        else:
            # Retrieve the account details using stripe_account_id
            account = stripe.Account.retrieve(to_user.stripe_account_id)
            if not account.charges_enabled or not account.payouts_enabled:
                # Redirect to another page if the account is not active
                return redirect('inactive_account')

            # Create a transfer to send the payment to the account
            transfer = stripe.Transfer.create(
                amount=amount * 100,
                currency="eur",
                destination=to_user.stripe_account_id,
                description="Video payment"
            )

            # Create Don and Notification objects
            Don.objects.create(
                user_don=request.user,
                to_user_don=to_user,
                video=video,
                cout_don=amount
            )
            Notification.objects.create(
                recipient=to_user,
                subject='Vous avez reçu un don',
                message='',
            )

            # Send email to customer with order details
            subject = 'DON MunTube'
            html_content = get_template('membre/ordermail.html').render({'title': video.title})
            from_email = 'merchab08@gmail.com'

            msg = EmailMessage(subject, html_content, from_email, [request.user.email, 'ablackadabra.com@gmail.com'])
            msg.content_subtype = "html"  # Main content is now text/html
            msg.send()

            #return HttpResponseRedirect(reverse('video', args=[str(pk)]))
            return redirect('success')

    return render(request, 'home.html')





"""def charge(request, pk):
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
                amount=amount * 100,  # amount in cents, again
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
                recipient=to_user,
                subject='Vous avez reçu un don',
                message='',
            )
            subject = 'DON MunTube'
            html_content = get_template('membre/ordermail.html').render({'title': video.title})
            from_email = 'merchab08@gmail.com'

            msg = EmailMessage(subject, html_content, from_email, [request.user.email, 'ablackadabra.com@gmail.com'])
            msg.content_subtype = "html"  # Main content is now text/html
            msg.send()
        except stripe.error.CardError as e:
            # The card has been declined
            pass

        # Send the order details to the customer
        # ...

        return HttpResponseRedirect(reverse('video', args=[str(pk)]))
    return render(request, 'home.html')"""


def success(request):
    notifs = Notification.objects.filter(recipient_id=request.user.id)

    return render(request, 'membre/success.html', {'notifs': notifs, })


@login_required
def pay_success_don(request):
    session = stripe.checkout.Session.retrieve(request.GET['session_id'])
    cout = session.cout_reference
    user = session.client_reference_id
    # user = request.user
    Don.objects.create(
        user_don=user,
        # video=video,
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
    videos = vdeo.objects.filter(user_id=request.user.id)
    # mesvideos = commentaire.objects.filter(user_id= request.user.id)
    mesvideos = commentaire.objects.all().order_by('-date_added')
    notifs = Notification.objects.filter(recipient_id=request.user.id)

    context = {
        'videos': videos,
        'mesvideos': mesvideos,
        'notifs': notifs,
    }
    return render(request, 'membre/mescommentaires.html', context)


def mesnotifications(request):
    notifs = Notification.objects.filter(recipient_id=request.user.id)
    context = {
        'notifs': notifs,
    }
    return render(request, 'membre/mesnotifications.html', context)


def display_notification(request):
    notifs = Notification.objects.filter(recipient_id=request.user.id)
    return render(request, 'base.html', {'notifs': notifs})


def search(request):
    query = request.GET.get('q')
    if query:
        words = query.split()
        results = vdeo.objects.filter(
            reduce(lambda x, y: x & y, [Q(title__icontains=word) | Q(tags__icontains=word) for word in words])
        )
        if not results:
            message = "Aucun résultat trouvé pour la requête: '{}'".format(query)
        else:
            message = "Résultats trouvés pour la requête: '{}'".format(query)
    else:
        message = "Aucune requête fournie"
    return render(request, 'search_results.html', {'message': message, 'results': results, 'query': query})


def mesdons(request):
    all_dons = Don.objects.all()
    context = {
        'all_dons': all_dons
    }
    return render(request, 'membre/mesDons.html', context)


def soutenir(request):
    return render(request, 'soutenir.html')


@login_required()
def soutien(request):
    if request.method == 'POST':
        # Get the amount from the form
        # amount = int(request.POST.get('amount'))
        token = request.POST.get('stripeToken')
        # to_user = video.user
        # Set your secret key: remember to change this to your live secret key in production
        # See your keys here: https://dashboard.stripe.com/account/apikeys
        stripe.api_key = settings.STRIPE_SECRET_KEY

        # Create a charge: this will charge the user's card
        try:
            charge = stripe.Charge.create(
                amount=75,  # amount in cents, again
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

            msg = EmailMessage(subject, html_content, from_email, [request.user.email, 'ablackadabra.com@gmail.com'])
            msg.content_subtype = "html"  # Main content is now text/html
            msg.send()
        except stripe.error.CardError as e:
            # The card has been declined
            pass

        # Send the order details to the customer
        # ...

        return HttpResponseRedirect(reverse('index'))
    return render(request, 'home.html')



def newvideo(request):
    return render(request, 'membre/newvideo.html')


def mes_muntubes(request):
    chaines = Channel.objects.filter(owner=request.user.id)
    return render(request, 'machaine.html', {'chaines': chaines})


def chaine_profile(request, chaine_id):
    user = get_object_or_404(User, id=chaine_id)
    chaine = Channel.objects.filter(owner=user).first()
    all_chaine = Channel.objects.filter(owner=user)
    videos = vdeo.objects.filter(user=user)
    play_lists = plist.objects.filter(user_playlist_id=user.id)
    total_abonnés = Subscription_channel.objects.filter(channel=chaine).count()
    is_subscribed = False

    try:
        subscription = Subscription_channel.objects.get(
            user_id=request.user.id,
            channel_id=chaine.id,
        )
        is_subscribed = subscription.is_subscribed
    except Subscription_channel.DoesNotExist:
        # Subscription does not exist, set is_subscribed to False
        is_subscribed = False
    context = {
        'chaine': chaine,
        'videos': videos,
        'play_lists': play_lists,
        'all_chaine': all_chaine,
        'total_abonnés': total_abonnés,
        'is_subscribed': is_subscribed,
               }
    return render(request, 'machaine.html', context)


@login_required
def update_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)

    if request.method == 'POST':
        user.first_name = request.POST.get('firstName')
        user.last_name = request.POST.get('lastName')
        user.username = request.POST.get('Pseudonyme')
        user.email = request.POST.get('email')
        user.country = request.POST.get('pays')
        user.bio = request.POST.get('bio')
        #user.phoneNumber = request.POST.get('phoneNumber')
        user.id_youtube_ch = request.POST.get('id_ytb')
        user.Active_don = request.POST.get('Active_don') == 'on'

        if 'img' in request.FILES:
            user.photo = request.FILES['img']

        user.save()

        messages.success(request, 'User profile updated successfully.')
        return redirect('monprofile', user_id=user.id)
    else:
        return render(request, 'membre/home.html', {'user': user})

@login_required
def updatevideo(request, video_id):
    video = get_object_or_404(vdeo, pk=video_id)
    video_url = video.vid.url
    miniature_url = video.miniature.url
    play_lists = plist.objects.filter(user_playlist_id=request.user.id)
    #video = vdeo.objects.filter(id=video_id)

    return render(request, 'membre/update_video.html', {'video':video,'video_url':video_url,
                                                        'miniature_url':miniature_url,'play_lists':play_lists})


@login_required
def confirmupdatevideo(request, video_id):
    video = get_object_or_404(vdeo, pk=video_id)

    if request.method == 'POST':
        video.title = request.POST.get('titre')
        video.detail = request.POST.get('description')
        video.categorie = request.POST.get('categorie')
        video.play_lists = get_object_or_404(playlist, id=request.POST.get('play_list'))
        video.tags = request.POST.get('tags')
        video.contenue_18 = request.POST.get('contenue_18') == 'on'
        video.status_video = request.POST.get('statut')

        # handle video upload
        if request.FILES.get('video'):
            video.vid.delete()  # remove old file if exists
            video.vid = request.FILES['video']

        # handle image upload
        if request.FILES.get('image'):
            video.miniature.delete()  # remove old file if exists
            video.miniature = request.FILES['image']

        video.save()

        messages.success(request, 'Video updated successfully.')
        return redirect('chaine')
        #return redirect('chaine', video_id=video.id)
    else:
        return render(request, 'home.html')

@csrf_exempt
@require_http_methods(["DELETE"])
def delete_video(request, video_id):
    video = get_object_or_404(vdeo, pk=video_id)
    video.delete()
    return HttpResponse(status=204)


def revendiquer(request):
    if request.method == 'POST':
        pseudonyme = request.POST['pseudonyme']
        prenom = request.POST['prénom']
        nom = request.POST['nom']
        email = request.POST['email']
        date = request.POST['date']
        pays = request.POST['pays']
        phone_number = request.POST['phoneNumber']
        message = request.POST['message']

        # Create a new UserProfile object and save it to the database
        revendication = revendq(
            pseudonyme=pseudonyme,
            prenom=prenom,
            nom=nom,
            email=email,
            date=date,
            pays=pays,
            phone_number=phone_number,
            message=message
        )
        revendication.save()

        subject = 'Revendication chaine'
        html_content = get_template('membre/ordermail.html').render({
            'title': 'Revendication chaine',
            'email': email
            })
        from_email = email

        msg = EmailMessage(subject, html_content, from_email, ['ablackadabra.com@gmail.com'])
        msg.content_subtype = "html"  # Main content is now text/html
        msg.send()

        # return a JSON response to display a success alert using JavaScript
        return JsonResponse({'success': True})


    return render(request, 'machaine.html')

"""@login_required
def subscribe(request):
    user_id = request.POST['user_id']
    channel_id = request.POST['channel_id']
    subscription, created = Subscription_channel.objects.get_or_create(
        user_id=user_id,
        channel_id=channel_id,
    )
    if created:
        status = 'subscribed'
    else:
        subscription.delete()
        status = 'unsubscribed'
    return JsonResponse({'status': status})

@login_required
def unsubscribe(request):
    user_id = request.POST['user_id']
    channel_id = request.POST['channel_id']
    Subscription_channel.objects.filter(
        user_id=user_id,
        channel_id=channel_id,
    ).delete()
    return JsonResponse({'status': 'unsubscribed'})"""


def subscription_status(request, channel_id):
    user_id = request.user.id
    subscription = Subscription_channel.objects.filter(user_id=user_id, channel_id=channel_id).first()
    is_subscribed = subscription.is_subscribed if subscription else False
    return JsonResponse({'is_subscribed': is_subscribed})

@login_required
def subscribe(request):
    user_id = request.POST['user_id']
    channel_id = request.POST['channel_id']
    subscription, created = Subscription_channel.objects.get_or_create(
        user_id=user_id,
        channel_id=channel_id,
    )
    if created:
        subscription.is_subscribed = True
        subscription.save()
        status = 'subscribed'
    else:
        subscription.is_subscribed = False
        subscription.save()
        status = 'unsubscribed'

    # Create a notification for the channel owner if a new subscription is made
    """if created:
        channel = subscription.channel.owner
        if channel.owner != request.user:
            subject = f'{request.user.username} subscribed to your channel'
            message = f'{request.user.username} has subscribed to your channel "{channel.title}".'
            notification = Notification(recipient=channel, subject=subject, message=message)
            notification.save()
"""
    return JsonResponse({'status': status})



def unsubscribe(request):
    user_id = request.POST['user_id']
    channel_id = request.POST['channel_id']
    subscription = Subscription_channel.objects.filter(
        user_id=user_id,
        channel_id=channel_id,
    ).first()
    if subscription:
        subscription.delete()
        status = 'unsubscribed'
    else:
        status = 'not subscribed'
    return JsonResponse({'status': status})


def delete_comment(request, comment_id):
    comment = get_object_or_404(commentaire, id=comment_id)

    if request.method == 'POST':
        comment.delete()
        return JsonResponse({'success': True})

    return JsonResponse({'success': False})

def report_comment(request, comment_id):
    comment = get_object_or_404(commentaire, id=comment_id)

    if request.method == 'POST':
        # Report the comment
        user = request.user
        contenue = comment.contenue
        reports = Report_comment.objects.filter(commentt=comment,contenue=comment.contenue, user=user)
        if not reports:
            report = Report_comment.objects.create(commentt=comment, contenue=comment.contenue,user=user)

            # Send email to admin
            subject = f'Comment reported: {comment.id}'
            context = {'comment': comment, 'user': user, 'contenue':contenue}
            html_message = render_to_string('membre/report_comment_email.html', context)
            plain_message = strip_tags(html_message)
            send_mail(
                subject,
                plain_message,
                settings.EMAIL_HOST_USER,
                ['ablackadabra.com@gmail.com'],
                html_message=html_message,
                fail_silently=False,
            )

            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'message': 'You have already reported this comment.'})

    return JsonResponse({'success': False})

@login_required
def report_video(request):
    print(request.POST.get('id_video'))
    if request.method == 'POST':
        id_video = request.POST.get('id_video')
        video = vdeo.objects.get(id=id_video)
        reporter = request.user
        report = Report_video.objects.create(video=video, reporter=reporter)
        report.save()

        subject = f"Video {video.title} has been reported"
        message = f"Video {video.title} has been reported by user {reporter.username}. Please investigate the issue."
        email_from = settings.EMAIL_HOST_USER
        email_to = ['ablackadabra.com@gmail.com']
        send_mail(subject, message, email_from, email_to, fail_silently=True)

        return JsonResponse({'success': True})

    return JsonResponse({'success': False})

@csrf_protect
@login_required
def reply_comment(request, comment_id):
    comment = get_object_or_404(commentaire, id=comment_id)

    if request.method == 'POST':
        reply_text = request.POST.get('reply_text', '').strip()
        if reply_text:
            # Check if the reply comment already exists
            reply = commentaire.objects.filter(user=request.user, parent=comment, contenue=reply_text).first()
            if not reply:
                reply = commentaire.objects.create(
                    user=request.user,
                    parent=comment,
                    contenue=reply_text
                )
            html = render(request, 'membre/reply_list.html', {'reply': reply}).content.decode('utf-8')
            return JsonResponse({'success': True, 'html': html})
    return JsonResponse({'success': False})

@login_required
def get_replies(request):
    if request.method == 'POST' and request.is_ajax():
        comment_id = request.POST.get('comment_id')
        comment = commentaire.objects.get(id=comment_id)
        replies = comment.children.all()
        context = {'replies': replies}
        html = render(request, 'reply_list.html', context=context).content.decode('utf-8')
        return JsonResponse({'success': True, 'html': html})
    else:
        return JsonResponse({'success': False})





def add_stripe(request):
    user = get_object_or_404(User, id=request.user.id)
    stripe_info = User.objects.get(id=request.user.id)
    return render(request,'membre/connect_stripe.html',{'stripe_info':stripe_info})

@login_required
def stripe_info(request):
    user = request.user

    if request.method == 'POST':
        stripe_account_id = request.POST.get('stripe_account_id')
        stripe_account_holder_name = request.POST.get('stripe_account_holder_name')
        stripe_account_number = request.POST.get('stripe_account_number')
        stripe_routing_number = request.POST.get('stripe_routing_number')

        # Check if the Stripe account ID is valid
        try:
            stripe.api_key = settings.STRIPE_SECRET_KEY
            stripe.Account.retrieve(stripe_account_id)
        except stripe.error.InvalidRequestError:
            messages.error(request, 'ID de compte Stripe invalide.')
            return render(request, 'membre/connect_stripe.html')

        # Save the data to the user model
        user.stripe_account_id = stripe_account_id
        user.stripe_account_holder_name = stripe_account_holder_name
        user.stripe_account_number = stripe_account_number
        user.stripe_routing_number = stripe_routing_number
        user.save()

        messages.success(request, 'Vos informations Stripe ont été mises à jour avec succès..')

    stripe_info = User.objects.get(id=request.user.id)
    return render(request, 'membre/connect_stripe.html', {'stripe_info': stripe_info})


def stripe_connect(request):
    user = request.user

    # Check if the user already has a Stripe account connected
    if user.stripe_account_id:
        return render(request, "stripe_connect.html", {"message": "You've already connected your Stripe account."})

    if request.method == "POST":
        # Get the user's email address and redirect URI
        email = request.POST.get("email")
        redirect_uri = request.build_absolute_uri("/stripe/connect/callback/")

        # Create a new Stripe account link
        account_link = stripe.AccountLink.create(
            account={
                "country": "US",
                "type": "custom",
                "email": email,
                "capabilities": {
                    "card_payments": {"requested": True},
                    "transfers": {"requested": True},
                },
            },
            refresh_url=redirect_uri,
            return_url=redirect_uri,
        )

        # Redirect the user to the Stripe account link URL
        return redirect(account_link.url)

    return render(request, "stripe_connect.html")


def stripe_redirect(request):
    stripe.api_key = STRIPE_SECRET_KEY

    # Exchange the authorization code for an access token
    code = request.GET.get("code")
    resp = stripe.oauth.token(
        grant_type="authorization_code", code=code
    )

    # Save the user's Stripe account ID and access token in your database
    user_id = request.GET.get("state")
    stripe_account_id = resp.stripe_user_id
    access_token = resp.access_token

    # Save the Stripe account ID and access token in your database
    user = User.objects.get(id=user_id)
    user.stripe_account_id = stripe_account_id
    user.stripe_access_token = access_token
    user.save()

    # Redirect the user to a success page
    return render(request, "stripe_success.html")


"""def create_charge(payer, payee, amount):
    stripe.api_key = "YOUR_SECRET_KEY"

    # Get the payee's Stripe account ID and access token
    payee_id = payee.stripe_account_id
    access_token = payee.stripe_access_token

    # Create the charge using the payee's Stripe account
    resp = stripe.Charge.create(
        amount=amount,
        currency="usd",
        source=payer.stripe_customer_id,
        application_fee_amount=100,  # Your platform's fee
        stripe_account=payee_id,
        metadata={
            "payer_name": payer.name,
            "payer_email": payer.email,
            "payee_name": payee.name,
            "payee_email": payee.email,
        },
        idempotency_key=str(uuid.uuid4()),
    )

    # Record the transaction in your database
    transaction = Transaction(
        payer=payer,
        payee=payee,
        amount=amount,
        charge_id=resp.id
    )
    transaction.save()

    # Return the Stripe charge ID
    return resp.id"""
