from __future__ import unicode_literals

from django.forms.widgets import HiddenInput
from django.utils.translation import ugettext_lazy as _

class WorldpayWidget(HiddenInput):

    def __init__(self, provider, payment, *args, **kwargs):
        attrs = kwargs.get('attrs', {})
        kwargs['attrs'] = {
            'data-client_key': provider.client_key,
        }
        kwargs['attrs'].update(attrs)
        super(WorldpayWidget, self).__init__(*args, **kwargs)


    class Media:
        js = ('https://cdn.worldpay.com/v1/worldpay.js', )
