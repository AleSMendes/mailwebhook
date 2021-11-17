
# -*- coding: utf-8 -*-
from celery import shared_task
from celery.utils.log import get_logger
from dj_twilio.models import TwilioWebhookMessage, TwilioWebhookMessageDetail
from django.db.transaction import atomic, non_atomic_requests
from django.utils import timezone
import json
import datetime as dt
import time

@atomic
def process_standard_webhook_event(sender, election_uuid, data):

    TwilioWebhookMessage.objects.create(
        received_at=timezone.now(),
        message=data,
    )


    # register details
    for item in data:
        timestamp = int(item.get("timestamp", round(time.mktime(dt.datetime.now().timetuple()))))

        #if item.get("election_uuid", None):
        # somente persistir registro que possuam o identificador da urna (integraçao com Helios Voting)
        TwilioWebhookMessageDetail.objects.create(
                received_at     = timezone.now(),
                sms_status      = item.get("SmsStatus", "not defined"),
                sms_sid         = item.get("SmsSid", "not defined"),
                election_uuid   = item.get("election_uuid", election_uuid),
                message_sid     = item.get("MessageSid", None),
                account_sid     = item.get("AccountSid", None),
                to_number       = item.get("To", None),
                #timestamp       = dt.datetime.fromtimestamp(timestamp)
            )        