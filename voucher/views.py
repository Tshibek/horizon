from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views.generic import DetailView, ListView, UpdateView, CreateView
from django.contrib import messages
from accounts.models import Profile
from .mixins import CustomRoleAdminMixin
from .models import Voucher, VoucherLog
from .forms import VoucherCreateForm, VoucherUpdateForm
import random
import string


# Create your views here.
def randomString(stringLenght=8):
    letters = string.ascii_letters + string.digits
    return ''.join(random.sample(letters, stringLenght))


class VoucherCreateView(LoginRequiredMixin, CustomRoleAdminMixin, CreateView):
    model = Voucher
    form_class = VoucherCreateForm
    template_name = 'voucher/VoucherCreateView.html'


    def form_valid(self, form):
        x = self.request.POST.get('value_x')
        x = int(x)
        date = timezone.now() + timezone.timedelta(days=14)
        objs = [
            Voucher(voucher=randomString(), money=int('0' + self.request.POST['value_money']), expires=date)
            for i in range(0, x)
        ]
        Voucher.objects.bulk_create(objs)
        return HttpResponseRedirect(reverse('voucher:voucher_create'))


@login_required()
def CheckVoucher(request):
    form = VoucherUpdateForm()
    if request.method == 'POST':
        form = VoucherUpdateForm(request.POST or None)
        if form.is_valid():
            vouper = form.cleaned_data['voucher']
            try:
                voucher_get = Voucher.objects.get(voucher__iexact=vouper)
                if voucher_get.used == False:
                    if voucher_get.expires >= timezone.now():
                        profil = Profile.objects.get(user=request.user)
                        voucher_get.used = True
                        profil.money_is = (profil.money_is + voucher_get.money)
                        profil.save()
                        voucher_get.save()
                        messages.success(request,
                                         'Kod jest prawidłowy! Pomyślnie dodałeś do swojego konta: ' + '<b>' + str(
                                             voucher_get.money) + '</b>' + ' zł')
                        VoucherLog.objects.create(user=request.user, voucher=vouper, money=voucher_get.money,
                                                  added=True)
                    else:
                        messages.warning(request,
                                         'Termin wazności kodu minał')
                else:
                    messages.warning(request,
                                     'Kod ' + '<b>' + '"' + str(vouper) + '"' + '</b>' + ' został już wykorzystany.')
            except Voucher.DoesNotExist:
                messages.error(request,
                               'Kod ' + '<b>' + '"' + str(vouper) + '"' + '</b>' + ' nie istnieje. ')
        else:
            messages.info(request,
                          'Coś poszło nie tak, spróbuj jeszcze raz za chwile! ')
    context = locals()
    return render(request, 'voucher/VoucherUpdateView.html', context)


class VoucherAdminListView(LoginRequiredMixin,CustomRoleAdminMixin, ListView):
    model = Voucher
    template_name = 'voucher/VoucherAdminListView.html'

    def get_queryset(self):
        return list(Voucher.objects.filter(used=False).order_by('-created'))


class VoucherUserListView(LoginRequiredMixin, ListView):
    model = VoucherLog
    template_name = 'voucher/VoucherUserListView.html'

    def get_queryset(self):
        return VoucherLog.objects.filter(user=self.request.user, added=True).order_by('-created')
