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
from dj_twilio.models import TwilioWebhookMessage
import tasks

#
# Outgoing Events
#
# when an inbound event is received
inbound_parse_event = Signal(providing_args=['text', 'html', 'from_', 'to', 'cc', 'subject', 'dkim', 'SPF', 'envelopeemail', 'charsets', 'spam_score', 'spam_report', 'attachments', 'attachment_info', 'attachmentX',])  # event for handling incoming email events

# when an webhook event is received
standard_webhook_event = Signal(providing_args=['data'])  # standard webhook, bounce, unsubscribe, delivered, read etc..


@receiver(inbound_parse_event)
def on_sendgrid_inbound_parse_event(sender, text, html, from_, to, cc, subject, dkim, SPF, envelopeemail, charsets, spam_score, spam_report, attachments, attachment_info, attachmentX, **kwargs):
    # do something amazing with the data passed in    
    pass


@receiver(standard_webhook_event)
def on_standard_webhook_event(sender, data, **kwargs):
    #WebhookMessage.objects.filter(
    #    received_at__lte=timezone.now() - dt.timedelta(days=7)
    #).delete()
    tasks.process_standard_webhook_event(sender, data)