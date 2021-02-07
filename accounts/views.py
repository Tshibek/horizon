from django.contrib import messages
from django.contrib.auth import logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView

from horizon.mixins import CustomAdminMixin
from horizon.models import Report
from .models import User, Admin
from django.views.generic.edit import UpdateView


@login_required(login_url=reverse_lazy('user:login'))
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Twoje hasło zostało zmienione.')
            return HttpResponseRedirect(reverse('user:change_password'))
        else:
            messages.error(request, 'Proszę popraw poniżse błędy.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {'form': form})


# Create your views here.
def LogoutView(request):
    logout(request)
    return redirect('horizon:home')


def profil(request, username):
    user = User.objects.get(username=username)
    context = locals()
    return render(request, 'accounts/ProfilView.html', context)


def profilSettings(request, username):
    user = User.objects.get(username=request.user.username)
    context = locals()
    return context

class AdminUpdate(LoginRequiredMixin, CustomAdminMixin, UpdateView):
    model = Admin
    fields = ['desc']
    pk_url_kwarg = 'desc_pk'
    template_name = 'accounts/adminForm.html'
    success_url = reverse_lazy('horizon:admins')


def user_report(request, username):
    reports = Report.objects.filter(report_user__username=username).all()
    context = locals()
    return render(request, 'horizon/ListReportView.html', context)
