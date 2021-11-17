# -*- coding: utf-8 -*-
"""
Webhook signals

Effectively callbacks that other apps can wait and be notified about
"""

from django.dispatch import Signal
from django.dispatch import receiver
from django.utils import timezone
import json
import datetime as dt
#from secrets import compare_digest
from dj_iagentesms.models import WebhookMessage
import tasks

#
# Outgoing Events
#

# when an webhook event is received
standard_webhook_event = Signal(providing_args=['data'])  # standard webhook, bounce, unsubscribe, delivered, read etc..


@receiver(standard_webhook_event)
def on_standard_webhook_event(sender, data, **kwargs):
    #WebhookMessage.objects.filter(
    #    received_at__lte=timezone.now() - dt.timedelta(days=7)
    #).delete()
    tasks.process_standard_webhook_event(sender, data)