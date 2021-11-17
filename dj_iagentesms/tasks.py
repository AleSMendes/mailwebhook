
# -*- coding: utf-8 -*-
from celery import shared_task
from celery.utils.log import get_logger
from dj_iagentesms.models import WebhookMessage, WebhookMessageDetail
from django.db.transaction import atomic, non_atomic_requests
from django.utils import timezone
import json
import datetime as dt
import time

@atomic
def process_standard_webhook_event(sender, data):

    WebhookMessage.objects.create(
        received_at=timezone.now(),
        message=data,
    )

    # register details
    for item in data:
        #timestamp = int(item.get("timestamp", round(time.mktime(dt.datetime.now().timetuple()))))
        timestamp = item.get("data", None)
        

        #if item.get("election_uuid", None):
        # somente persistir registro que possuam o identificador da urna (integraçao com Helios Voting)
        WebhookMessageDetail.objects.create(
                received_at     = timezone.now(),
                status          = item.get("status", "not defined"),
                election_uuid   = item.get("election_uuid", None),
                celular         = item.get("celular", None),
                shortcode       = item.get("shortcode", None),
                codigosms       = item.get("codigosms", None),
                timestamp       = timestamp,
                #mensagem         = item.get("mensagem", None),
            )       