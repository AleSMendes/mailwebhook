# -*- coding: utf-8 -*-
from django.test import TestCase, Client
from django.core.urlresolvers import reverse_lazy

from dj_twilio.views import TwilioStandardEventWebhookView

from . import   STANDARD_WEBHOOK_EVENT

import json



class StandardEventWebhookViewTest(TestCase):
    """
    """
    subject = TwilioStandardEventWebhookView

    def setUp(self):
        self.client = Client()
        self.url = reverse_lazy('standard_event_webhook_callback')
        self.valid_webhook_data = STANDARD_WEBHOOK_EVENT
        self.header = {"HTTP_TWILIO_WEBHOOK_TOKEN":"abc123"}

    def test_valid_method(self, *args, **kwargs):
        resp = self.client.post(self.url, content_type='application/json; charset=utf-8', data=json.dumps(self.valid_webhook_data), **self.header)
        self.assertEqual(resp.status_code, 200)

        self.assertEqual(json.loads(resp.content), {'detail': 'Standard Twilio Webhook recieved'})

        # test signal gets fired
