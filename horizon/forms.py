from bootstrap_modal_forms.mixins import PopRequestMixin, CreateUpdateAjaxMixin
from django import forms
from .models import Ban, Report


# class BansForm(forms.ModelForm):
#     class Meta:
#         model = Ban
#         fields = ['user']
#
class CreateReport(forms.ModelForm):
    user = forms.CharField(required=True)
    class Meta:
        model = Report
        exclude = ['user']

class ReportUpdate(PopRequestMixin, CreateUpdateAjaxMixin, forms.ModelForm):
    TYPE_CHOICES = (
        ('TEMPORARY', 'Czasowy'),
        ('PERMAMENTLY', 'Permanentnie'),
    )
    REPORT_CHOICES = (
        ('mute', 'mute'),
        ('ban', 'ban'),
    )
    EXPIRES_CHOICES = (

        (1, '1'),
        (3, '3'),
        (7, '7'),
        (12, '12'),
        (14, '14'),
        (21, '21'),
        (30, '30'),
    )
    EXPIRES_TIME_CHOICES = (
        ('h', 'Godziny'),
        ('d', 'Dni'),
    )
    type_report = forms.ChoiceField(choices=REPORT_CHOICES, required=False)
    type = forms.ChoiceField(choices=TYPE_CHOICES, required=False)
    expires = forms.ChoiceField(choices=EXPIRES_CHOICES)
    expires_time = forms.ChoiceField(choices=EXPIRES_TIME_CHOICES)
    reason = forms.CharField(required=False, widget=forms.Textarea)

    class Meta:
        model = Report
        fields = ['status']
