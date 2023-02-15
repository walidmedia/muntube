from django.conf.urls.static import static
from django.urls import path

from ABLACKADABRA import settings
from .views import checkout, upload, success_upload, addvideo, mesvideos, checkout_session, machaine, stockage, \
        pay_success, pay_cancel, video, commenter, subscribe, monprofile, save_video, \
        vidéosjaime, bibliothèque, a_regarder, chaine, AddPlaylist, maintenance, checkout_sess_don, checkout_don, \
        charge, mescommentaires, like_comment, view_history, success, proced_don, payment, \
        display_notification, mesnotifications, search, channel_muntube, chart_data, like_video, subscribe, mesdons, \
        soutenir, soutien, connect_stripe, get_stripe_account_id, get_stripe_access_token, newvideo, chaine_profile

urlpatterns = [
        #path('pricing/', pricing, name='pricing'),
        path('upload/', upload, name='upload'),
        path('addvideo/', addvideo, name='addvideo'),
        path('MesVideos/', mesvideos, name='mesvideos'),
        path('stockage/', stockage, name='stockage'),
        path('machaine/', machaine, name='machaine'),
        path('success_upload/', success_upload, name='success_upload'),
        path('checkout/<int:plan_id>', checkout, name='checkout'),
        path('checkout_don/<int:video_id>', checkout_don, name='checkout_don'),
        path('checkout_session/<int:pk>',checkout_session,name='checkout_session'),
        path('checkout_sess_don/<int:cout_don>',checkout_sess_don,name='checkout_sess_don'),
        path('pay_success', pay_success, name='pay_success'),
        path('success', success, name='success'),
        path('pay_cancel', pay_cancel, name='pay_cancel'),
        path('video/<int:id>', video, name='video'),
        path('commenter/<int:id>', commenter, name='commenter'),
        path('video/<int:video_id>/like/', like_video, name='like_video'),
        path('like_comment/<int:comment_id>/', like_comment, name='like_comment'),
        path('subscribe/', subscribe, name='subscribe'),
        path('save_video/<int:pk>', save_video, name='save_video'),
        path('monprofile/<int:id>', monprofile, name='monprofile'),
        path('vidéosjaime/', vidéosjaime, name='vidéosjaime'),
        path('bibliothèque/', bibliothèque, name='bibliothèque'),
        path('a_regarder/', a_regarder, name='a_regarder'),
        path('chaine/', chaine, name='chaine'),
        path('AddPlaylist/', AddPlaylist, name='AddPlaylist'),
        path('maintenance/', maintenance, name='maintenance'),
        path('charge/<int:pk>', charge, name='charge'),
        path('mescomments/', mescommentaires, name='mescommentaires'),
        #path('channel_videos/', channel_videos, name='channel_videos'),
        #path('video/<int:id>', play_video, name='play_video'),
        path('historique/', view_history, name='view_history'),
        path('proced_don/<int:id>', proced_don, name='proced_don'),
        path('payment/', payment, name='payment'),
        path('display_notification/', display_notification, name='display_notification'),
        path('mesnotifications/', mesnotifications, name='mesnotifications'),
        path('search/', search, name='search'),
        path('channel_muntube/', channel_muntube, name='channel_muntube'),
        path('stats/', chart_data, name='video_stats'),
        path('subscribe/<int:channel_id>/', subscribe, name='subscribe'),
        path('mesdons/', mesdons, name='mesdons'),
        path('soutenir/', soutenir, name='soutenir'),
        path('soutien/', soutien, name='soutien'),
        path('connect_stripe/', connect_stripe, name='connect_stripe'),
        path('get_stripe_account_id/', get_stripe_account_id, name='get_stripe_account_id'),
        path('get_stripe_access_token/', get_stripe_access_token, name='get_stripe_access_token'),
        path('newvideo/', newvideo, name='newvideo'),
        path('chaine/<int:chaine_id>/', chaine_profile, name='chaine_profile'),

]
