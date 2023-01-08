from django.conf.urls.static import static
from django.urls import path

from ABLACKADABRA import settings
from .views import checkout, upload, success_upload, addvideo, mesvideos, checkout_session, machaine, stockage, \
        pay_success, pay_cancel, video

urlpatterns = [
        #path('pricing/', pricing, name='pricing'),
        path('upload/', upload, name='upload'),
        path('addvideo/', addvideo, name='addvideo'),
        path('MesVideos/', mesvideos, name='mesvideos'),
        path('stockage/', stockage, name='stockage'),
        path('machaine/', machaine, name='machaine'),
        path('success_upload/', success_upload, name='success_upload'),
        path('checkout/<int:plan_id>', checkout, name='checkout'),
        path('checkout_session/<int:plan_id>',checkout_session,name='checkout_session'),
        path('pay_success', pay_success, name='pay_success'),
        path('pay_cancel', pay_cancel, name='pay_cancel'),
        path('video/', video, name='video'),

]
