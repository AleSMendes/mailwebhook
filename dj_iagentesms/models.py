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
    timestamp       = models.DateTimeField(blank=True, null=True)
    codigosms       = models.CharField(max_length=250, null=True)
    status          = models.CharField(max_length=250, null=True)
    election_uuid   = models.CharField(max_length=250, null=True)
    celular         = models.CharField(max_length=250, null=True)
    shortcode       = models.CharField(max_length=250, null=True)
    mensagem        = models.CharField(max_length=250, null=True)


    class Meta:
        indexes = [
            models.Index(fields=["celular", "election_uuid", "codigosms"]),
        ]        

    def as_dict(self):
        return {
            "codigosms": self.codigosms,
            "status": self.status,
            "election_uuid": self.election_uuid,
            "celular": self.celular,
            "shortcode": self.shortcode,
        }        