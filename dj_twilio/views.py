# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden
from django.views.generic import View
from django.conf import settings
from django.core import serializers
import signals 
from braces.views import JSONResponseMixin
from secrets import compare_digest
from dj_twilio.models import TwilioWebhookMessage, TwilioWebhookMessageDetail
import json
import logging
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from functools import wraps
#from twilio.twiml.voice_response import VoiceResponse
#from twilio.twiml.messaging_response import MessagingResponse
try:
    from twilio.util import RequestValidator
except:
    from twilio.request_validator import RequestValidator  

import os
logger = logging.getLogger('django.request')


# https://www.twilio.com/docs/usage/tutorials/how-to-secure-your-django-project-by-validating-incoming-twilio-requests

def validate_twilio_request(f):
    """Validates that incoming requests genuinely originated from Twilio"""
    @wraps(f)
    def decorated_function(request, *args, **kwargs):
        # Create an instance of the RequestValidator class
        #validator = RequestValidator(os.environ.get('TWILIO_AUTH_TOKEN'))
        validator = RequestValidator(settings.TWILIO_AUTH_TOKEN)

        # Validate the request using its URL, POST data,
        # and X-TWILIO-SIGNATURE header
        request_valid = validator.validate(
            request.build_absolute_uri(),
            request.POST,
            request.META.get('HTTP_X_TWILIO_SIGNATURE', ''))

        # Continue processing the request if it's valid, return a 403 error if
        # it's not
        if request_valid or settings.DEBUG:
            return f(request, *args, **kwargs)
        else:
            return HttpResponseForbidden()
    return decorated_function
    

@method_decorator(validate_twilio_request, name='dispatch')
class TwilioStandardEventWebhookView(JSONResponseMixin, View):
    """
    Handle the Twilio callback
    """
    http_method_names = [u'post',]

    json_dumps_kwargs = {'indent': 3}

    def dispatch(self, request, *args, **kwargs):
        logger.info('Recieved standard Twilio webhook')
        return super(TwilioStandardEventWebhookView, self).dispatch(request=request, *args, **kwargs)

    def post(self, request, *args, **kwargs):        
        #
        # Send the event
        #          
        data=json.loads(request.body)
        election_uuid =  kwargs.get("election_uuid", None)

        if type(data) == list:
            pass
        elif type(data) == dict:
            data["election_uuid"] = election_uuid
            data = [data]

        
        signals.standard_webhook_event.send(sender=self, data=data, election_uuid=election_uuid)

        return self.render_json_response({
            'detail': 'Standard Twilio Webhook recieved',
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
        qs  = TwilioWebhookMessageDetail.objects.filter(election_uuid__in = uuids)
        #data = serializers.serialize("json", qs, fields = ("email_to", "election_uuid", "event_name", "timestamp"))
        #data = json.dumps(list(qs.values()))  
        dictionaries = [ obj.as_dict() for obj in qs ]
        
        return self.render_json_response({
            'data': dictionaries,
        })        