from django import forms
from .models import PaymentRequest


class SmsPayForm(forms.ModelForm):
    class Meta:
        model = PaymentRequest
        fields = ['sms_code', 'money']
