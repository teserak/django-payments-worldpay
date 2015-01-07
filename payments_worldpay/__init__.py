from __future__ import unicode_literals

import requests
import json

from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponseForbidden

from .forms import PaymentForm
from payments import BasicProvider


class WorldpayProvider(BasicProvider):

    def __init__(self, *args, **kwargs):
        self.client_key = kwargs.pop('client_key')
        self.service_key = kwargs.pop('service_key')
        self.endpoint = kwargs.pop(
            'endpoint', 'https://api.worldpay.com/v1/orders')
        super(WorldpayProvider, self).__init__(*args, **kwargs)
        if not self._capture:
            raise ImproperlyConfigured(
                'Worldpay does not support pre-authorization.')

    def get_transactions_data(self):
        data = {
            'amount': int(float(self.payment.total) * 100),
            'currencyCode': self.payment.currency,
            'orderDescription': self.payment.description,
        }
        return data

    def get_product_data(self, extra_data=None):
        data = self.get_transactions_data()

        if extra_data:
            data.update(extra_data)

        return data

    def get_payment_response(self, extra_data=None):
        post = self.get_product_data(extra_data)
        headers = {'Authorization': self.service_key,'Content-type': 'application/json'}
        return requests.post(self.endpoint, data=json.dumps(post), headers=headers)

    def get_form(self, data=None):
        return PaymentForm(data=data, payment=self.payment, provider=self,
                           action='')

    def process_data(self, request):
        return HttpResponseForbidden('FAILED')
