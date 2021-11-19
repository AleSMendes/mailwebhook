# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden
from django.views.generic import View
from django.conf import settings
from django.core import serializers
import signals #import inbound_parse_event, standard_webhook_event
from braces.views import JSONResponseMixin
from secrets import compare_digest
from dj_iagentesms.models import WebhookMessage, WebhookMessageDetail
import json
import logging
logger = logging.getLogger('django.request')
from views_utils import qdict_to_dict

class StandardEventWebhookView(JSONResponseMixin, View):
    """
    Handle the IAgenteSMS callback
    """
    http_method_names = [u'post', u'get']

    json_dumps_kwargs = {'indent': 3}

    def dispatch(self, request, *args, **kwargs):
        logger.info('Recieved standard IAgenteSMS webhook')
        return super(StandardEventWebhookView, self).dispatch(request=request, *args, **kwargs)

    def post(self, request, *args, **kwargs):         
        data=json.loads(request.body)
        if type(data) == dict:
            data = [data]
                    
        signals.standard_webhook_event.send(sender=self, data=data)

        return self.render_json_response({
            'detail': 'Standard IAgenteSMS Webhook recieved',
        })

    def get(self, request, *args, **kwargs):                 
        data = qdict_to_dict(request.GET)
        if type(data) == dict:
            data = [data]

        signals.standard_webhook_event.send(sender=self, data=data)

        return self.render_json_response({
            'detail': 'Standard IAgenteSMS Webhook recieved',
        })        


class DataWebhookView(JSONResponseMixin, View):
    """
    Get statistics
    """
    http_method_names = [u'post']

    json_dumps_kwargs = {'indent': 3}

    def dispatch(self, request, *args, **kwargs):
        logger.info('Request data webhook')
        return super(DataWebhookView, self).dispatch(request=request, *args, **kwargs)

    def post(self, request, *args, **kwargs):  
        data  = json.loads(request.body)
        codigosms = data.get("codigosms", [])
        qs  = WebhookMessageDetail.objects.filter(codigosms__in = codigosms)
        #qs  = WebhookMessageDetail.objects.all()
        #data = serializers.serialize("json", qs, fields = ("email_to", "election_uuid", "event_name", "timestamp"))
        #data = json.dumps(list(qs.values()))  
        dictionaries = [ obj.as_dict() for obj in qs ]
        
        return self.render_json_response({
            'data': dictionaries,
        })        

    