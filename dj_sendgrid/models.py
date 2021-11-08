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