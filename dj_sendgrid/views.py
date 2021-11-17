# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden
from django.views.generic import View
from django.conf import settings
from django.core import serializers
import signals #import inbound_parse_event, standard_webhook_event
from braces.views import JSONResponseMixin
from secrets import compare_digest
from dj_sendgrid.models import WebhookMessage, WebhookMessageDetail
import json
import logging
logger = logging.getLogger('django.request')


class InboundParseWebhookView(JSONResponseMixin, View):
    """
    Handle the Sendgrid callback
    """
    http_method_names = [u'post' ]

    json_dumps_kwargs = {'indent': 3}

    def dispatch(self, request, *args, **kwargs):
        logger.info('Recieved inbound parse webhook')
        return super(InboundParseWebhookView, self).dispatch(request=request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        given_token = request.META.get("HTTP_SENDGRID_WEBHOOK_TOKEN", "")
        if not compare_digest(given_token, settings.SENDGRID_WEBHOOK_TOKEN):
            return HttpResponseForbidden(
                "Incorrect token in Sendgrid-Webhook-Token header.",
                content_type="text/plain",
            )

        data = request.POST
        if not len(data):
            data = eval(request.body)
        
        if "from" in data.keys():
            data["from_"] = data["from"]

        if "attachment-info" in data.keys():
            data["attachment_info"] = data["attachment-info"]            
        #
        # Send the event
        #
        signals.inbound_parse_event.send(sender=self, **data)

        return self.render_json_response({
            'detail': 'Inbound Sendgrid Webhook recieved',
        })


class StandardEventWebhookView(JSONResponseMixin, View):
    """
    Handle the Sendgrid callback
    """
    http_method_names = [u'post',]

    json_dumps_kwargs = {'indent': 3}

    def dispatch(self, request, *args, **kwargs):
        logger.info('Recieved standard sendgrid webhook')
        return super(StandardEventWebhookView, self).dispatch(request=request, *args, **kwargs)

    def post(self, request, *args, **kwargs):        
        #given_token = request.META.get("HTTP_SENDGRID_WEBHOOK_TOKEN", "") #headers
        
        #if not compare_digest(given_token, settings.SENDGRID_WEBHOOK_TOKEN):
        #    return HttpResponseForbidden(
        #        "Incorrect token in Sendgrid-Webhook-Token header.",
        #        content_type="text/plain",
        #    )

        #
        # Send the event
        #        
        data=json.loads(request.body)
        
        if type(data) == dict:
            data = [data]

        signals.standard_webhook_event.send(sender=self, data=data)

        return self.render_json_response({
            'detail': 'Standard Sendgrid Webhook recieved',
        })


class DataWebhookView(JSONResponseMixin, View):
    """
    Get statistics
    """
    http_method_names = [u'post',]

    json_dumps_kwargs = {'indent': 3}

    def dispatch(self, request, *args, **kwargs):
        logger.info('Request data webhook')
        return super(DataWebhookView, self).dispatch(request=request, *args, **kwargs)

    def post(self, request, *args, **kwargs):  
        data  = json.loads(request.body)
        uuids = data.get("election_uuid", [])
        qs  = WebhookMessageDetail.objects.filter(election_uuid__in = uuids)
        #data = serializers.serialize("json", qs, fields = ("email_to", "election_uuid", "event_name", "timestamp"))
        #data = json.dumps(list(qs.values()))  
        dictionaries = [ obj.as_dict() for obj in qs ]
        
        return self.render_json_response({
            'data': dictionaries,
        })        