from bootstrap_modal_forms.mixins import PopRequestMixin, CreateUpdateAjaxMixin
from django import forms

from .models import Voucher, VoucherLog


class VoucherCreateForm(forms.ModelForm):
    value_x = forms.IntegerField(required=True)
    value_money = forms.IntegerField(required=True)

    class Meta:
        model = Voucher
        fields = ['voucher', 'money']


class VoucherUpdateForm(forms.Form):
   voucher = forms.CharField(max_length=8)