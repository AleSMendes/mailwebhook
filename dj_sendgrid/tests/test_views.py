# -*- coding: utf-8 -*-
from django.test import TestCase, Client
from django.core.urlresolvers import reverse_lazy

from dj_sendgrid.views import (InboundParseWebhookView,
                               StandardEventWebhookView)

from . import (INBOUND_POST_REQUEST,
               STANDARD_WEBHOOK_EVENT)

import json


class InboundParseWebhookViewTest(TestCase):
    """
    """
    subject = InboundParseWebhookView

    def setUp(self):
        self.client = Client()
        self.url = reverse_lazy('inbound_event_webhook_callback')
        self.valid_webhook_data = INBOUND_POST_REQUEST
        self.header = {"HTTP_SENDGRID_WEBHOOK_TOKEN":"abc123"}

    def test_valid_method(self, *args, **kwargs):
        resp = self.client.post(self.url, content_type='application/json; charset=utf-8', data=json.dumps(self.valid_webhook_data), **self.header)
        self.assertEqual(resp.status_code, 200)

        self.assertEqual(json.loads(resp.content), {'detail': 'Inbound Sendgrid Webhook recieved'})

        # test signal gets fired


class StandardEventWebhookViewTest(TestCase):
    """
    """
    subject = StandardEventWebhookView

    def setUp(self):
        self.client = Client()
        self.url = reverse_lazy('standard_event_webhook_callback')
        self.valid_webhook_data = STANDARD_WEBHOOK_EVENT
        self.header = {"HTTP_SENDGRID_WEBHOOK_TOKEN":"abc123"}

    def test_valid_method(self, *args, **kwargs):
        resp = self.client.post(self.url, content_type='application/json; charset=utf-8', data=json.dumps(self.valid_webhook_data), **self.header)
        self.assertEqual(resp.status_code, 200)

        self.assertEqual(json.loads(resp.content), {'detail': 'Standard Sendgrid Webhook recieved'})

        # test signal gets fired
