# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import views

urlpatterns = [
    url(r'^webhook/standard/$', csrf_exempt(views.StandardEventWebhookView.as_view()), name='iagentesms_event_webhook_callback'),
    url(r'^webhook/data/$', csrf_exempt(views.DataWebhookView.as_view()), name='get_iagentesms_data'),
]