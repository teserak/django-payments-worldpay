# django-payments-worldpay
django-payments Worldpay Backend

Quick and dirty work, no warranty, works for me.

### Quick Start

1. in settings
```
PAYMENT_VARIANTS = {
  'worldpay': ('payments_worldpay.WorldpayProvider', {
    'service_key': '<your_service_key>',
    'client_key': '<your_client_key>',
    'endpoint': 'https://api.worldpay.com/v1/orders',
  })
}
```

2. your payment form template file needs to create a token and set the form token value using javascript (the following is a quick version)
```
{% extends "ecomm/order/payment/details.html" %}
{% load as_horizontal_form from bootstrap %}
{% load i18n %}

{% block forms %}
<script type='text/javascript'>
window.onload = function() {
  var form = document.getElementById('payment-form');   
  
  /* map django-payments form fields for worldpay.js */
  form.number.setAttribute('data-worldpay', 'number');
  form.cvv2.setAttribute('data-worldpay', 'cvc');
  form.expiration_0.setAttribute('data-worldpay', 'exp-month');
  form.expiration_1.setAttribute('data-worldpay', 'exp-year');
  form.name.setAttribute('data-worldpay', 'name');
  
  Worldpay.setClientKey(form.token.getAttribute('data-client_key'));
  Worldpay.reusable = false;

  /* when submit the form, create token using worldpay js and send token back to server */
  $(form._submit).bind('click', function(e){
    e.preventDefault();
    
    Worldpay.card.createToken(form, function(status, response) {
      
      if (response.error) {
      	form.worldpyjs_validation_error.value = response.error.message
      }
      else{
      	form.worldpyjs_validation_error.value = ''
      }
      
      var token = response.token;
      form.token.value = token;
      form.submit()
      });
  })
}
</script>


<form id="payment-form"method="{{ form.method }}" class="form-horizontal"{% if form.action %} action="{{ form.action }}"{% endif %}>
    {% csrf_token %}
    {{ form.media }}
    {{ form|as_horizontal_form }}
    {% if form.errors %}
    <p><a class="btn" href="{% url "ecomm:order-details" token=payment.order.token %}">{% trans "Change payment method" %}</a></p>
    {% endif %}

    <p><input class="btn btn-primary" type="submit" name="_submit" value="Proceed"/></p>

</form>
{% endblock forms %}
```

### Behavior
The form will display django form validation errors first. If there is none and worldpay.js returned an error when trying to create a token, that error will be displayed.
