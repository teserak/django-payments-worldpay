from __future__ import unicode_literals
import json
from django import forms
from django.utils.translation import ugettext_lazy as _

from payments.forms import CreditCardPaymentForm
from .widgets import WorldpayWidget

RESPONSE_STATUS = {
    'SUCCESS': 'confirmed',
    'FAILED': 'rejected'}

class PaymentForm(CreditCardPaymentForm):
    name = forms.CharField(label=_('Name on Card'))
    worldpyjs_validation_error = forms.CharField(widget=forms.HiddenInput, initial='', required=False)
    # token = forms.CharField(widget=forms.HiddenInput)

    def __init__(self, *args, **kwargs):
        super(PaymentForm, self).__init__(*args, **kwargs)
        widget = WorldpayWidget(provider=self.provider, payment=self.payment)
        self.fields['token'] = forms.CharField(widget=widget, required=False)
    
    def clean(self):
        cleaned_data = super(PaymentForm, self).clean()

        worldpay_error = cleaned_data.get('worldpyjs_validation_error')
        if worldpay_error and not self.errors:
            raise forms.ValidationError(worldpay_error)

        if not self.errors:
            if not self.payment.transaction_id:
                data = {
                    'token': cleaned_data.get('token'),}

                response = self.provider.get_payment_response(data)

                data = json.loads(response.text)
                if response.ok and RESPONSE_STATUS.get(data['paymentStatus'], False):
                    self.payment.transaction_id = data['orderCode']
                    self.payment.change_status(
                        RESPONSE_STATUS.get(data['paymentStatus'], 'error'))
                else:
                    errors = [data['message']]
                    self._errors['__all__'] = self.error_class(errors)
                    self.payment.change_status('error')
        return cleaned_data
