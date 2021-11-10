# -*- coding: utf-8 -*-
"""
Data Objects for Webhook.
"""
import uuid
from django.conf import settings
from django.db import models, transaction
import jsonfield

class WebhookMessage(models.Model):
    received_at = models.DateTimeField(help_text="When we received the event.")
    #message = models.JSONField(default=None, null=True)
    message = jsonfield.JSONField(default=None, null=True)

    class Meta:
        indexes = [
            models.Index(fields=["received_at"]),
        ]

class WebhookMessageDetail(models.Model):
    received_at     = models.DateTimeField(help_text="When we received the event.")
    event_name      = models.CharField(max_length=250, null=False, default="bounce")
    type            = models.CharField(max_length=250, null=True)
    status          = models.CharField(max_length=250, null=True)
    server          = models.CharField(max_length=250, null=True)
    election_uuid   = models.CharField(max_length=250, null=True)
    email_from      = models.CharField(max_length=250, null=True)
    email_to        = models.CharField(max_length=250, null=False)
    subject         = models.CharField(max_length=250, null=True)


    class Meta:
        indexes = [
            models.Index(fields=["received_at", "election_uuid", "email_to"]),
        ]        