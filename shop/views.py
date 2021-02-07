from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import FormView, CreateView

from shop.models import PaymentRequest
from skyhorizon.mcrcon import MCRcon
from skyhorizon.settings.common import secrets
from .forms import SmsPayForm


def connect():
    mc = MCRcon()
    mc.connect(host=secrets['MC_HOST'], port=int(secrets['RCON_PORT']), password=secrets['RCON_PASSWORD'])
    return mc


def shop(request):
    return render(request, 'shop/ShopView.html')


class SmsPaymentView(CreateView, LoginRequiredMixin):
    template_name = 'shop/SmsPaypemnt.html'
    model = PaymentRequest
    form_class = SmsPayForm
    success_url = reverse_lazy('shop:sms')

    def form_valid(self, form):
        try:
            sms = form.save(commit=False)
            sms.user = self.request.user
            sms.type = 'wallet'
            sms.payment = 'sms'
            sms.status = 'SUCCESS'
            sms.save()
            mc = connect()
            moneyis = mc.command('sklepis ' + str(self.request.user.username) + ' ' + str(int(float(self.request.POST['money']))))
        except IntegrityError:
            raise ValidationError("This question already exist")

        return super(SmsPaymentView, self).form_valid(form)

    def form_invalid(self, form):
        sms = form.save(commit=False)
        sms.user = self.request.user
        sms.type = 'wallet'
        sms.payment = 'sms'
        sms.status = 'FAILED'
        sms.save()
        return super(SmsPaymentView, self).form_valid(form)
