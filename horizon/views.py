from bootstrap_modal_forms.mixins import PassRequestMixin
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Sum, Max
from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.urls import reverse_lazy, reverse
from django.utils import timezone

from django.views.generic import DetailView, ListView, UpdateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.db import IntegrityError

from horizon.forms import ReportUpdate
from horizon.mixins import CustomAdminMixin, CustomRoleOwnerMixin
from skyhorizon.mcrcon import MCRcon
from skyhorizon.settings.common import secrets
from .models import Ban, StoneLevel, BuyLogs, Report, Mute, New
from accounts.models import User, Profile, Admin


def connect():
    mc = MCRcon()
    mc.connect(host=secrets['MC_HOST'], port=int(secrets['RCON_PORT']), password=secrets['RCON_PASSWORD'])
    return mc


def handler404(request):
    response = render_to_response("http/404.html")
    response.status_code = 404
    return response


def handler400(request):
    response = render_to_response("http/400.html")
    response.status_code = 400
    return response


def handler500(request):
    response = render_to_response("http/500.html")
    response.status_code = 500
    return response


def handler403(request):
    response = render_to_response("http/403.html")
    response.status_code = 403
    return response


def home_page(request):
    user_uniq = User.objects.all().count()
    stone_level = StoneLevel.objects.all().order_by('-level')[:10]
    join_count = Profile.objects.all().order_by('join_count').last()
    coins = Profile.objects.all().order_by('money_is').last()
    buy_count = BuyLogs.objects.all().count()
    max_stone = StoneLevel.objects.all().order_by('all_stone').last()
    ban_count = Ban.objects.all().count()
    stone = list(StoneLevel.objects.all().aggregate(Sum('all_stone')).values())[0]
    context = locals()
    return render(request, 'horizon/HomePage.html', context)


def rules(request):
    return render(request, 'horizon/rulesPage.html')


def faq(request):
    return render(request, 'horizon/faqPage.html')


def ranking(request):
    stone_level = StoneLevel.objects.all().order_by('-level')[:10]
    pick_stone = StoneLevel.objects.all().order_by('-all_stone')[:10]
    kills = Profile.objects.all().order_by('-kills')[:10]
    sky_coins = Profile.objects.all().order_by('-money')[:10]
    join_count = Profile.objects.all().order_by('-join_count')[:10]
    context = locals()
    return render(request, 'horizon/assets/layoutRanking.html', context)


def contact(request):
    context = locals()
    return render(request, 'horizon/ContactPage.html', context)


def search(request):
    query = request.GET.get('q')
    if query:
        user = User.objects.filter(username=query)
        if user.count():
            x = user
        else:
            no = query
    context = locals()
    return HttpResponseRedirect(reverse('user:profile', args={query}))


def BanView(request):
    banned = Ban.objects.all().order_by('-created')[:10]
    context = locals()
    return render(request, 'horizon/BanPage.html', context)


def AdminsView(request):
    admins = Admin.objects.all().order_by('-user__profile__rank')
    context = locals()
    return render(request, 'horizon/AdminPage.html', context)


class ReportDetailView(LoginRequiredMixin, CustomAdminMixin, DetailView):
    pass


class ReportListView(LoginRequiredMixin, CustomAdminMixin, ListView):
    model = Report
    template_name = 'horizon/ListReportView.html'
    paginate_by = 15
    ordering = ['-created']
    context_object_name = 'reports'


class ReportAcceptListView(LoginRequiredMixin, CustomAdminMixin, ListView):
    model = Report
    template_name = 'horizon/ListReportView.html'
    paginate_by = 15
    ordering = ['-created']
    context_object_name = 'reports'


class ReportDeclineListView(LoginRequiredMixin, CustomAdminMixin, ListView):
    model = Report
    template_name = 'horizon/ListReportView.html'
    paginate_by = 15
    ordering = ['-created']
    context_object_name = 'reports'


class ReportPendingListView(LoginRequiredMixin, CustomAdminMixin, ListView):
    model = Report
    template_name = 'horizon/ListReportView.html'
    paginate_by = 15
    ordering = ['-created']
    context_object_name = 'reports'


class ReportCreateView(LoginRequiredMixin, CreateView):
    model = Report
    template_name = 'horizon/CreateRequest.html'
    # form_class = CreateReport
    success_url = reverse_lazy('horizon:report_create')
    fields = ['user', 'title', 'content', 'evidence']

    def form_valid(self, form):
        try:
            report = form.save(commit=False)
            report.report_user = self.request.user
            report.save()
            messages.success(self.request,
                             'Twoje zgłoszenie zostanie niedługo rozpatrzone, sprawdź swój profil w celu dowiedzenia się')

        except IntegrityError as e:
            user = User.objects.get(username=self.request.POST['user'])
            e = ("Użytkownik " + "<b>" + str(user) + "</b>" + " został już zreportowany")
            messages.error(self.request, e)
        return HttpResponseRedirect(reverse('horizon:report_create'))


class ReportUpdateView(PassRequestMixin, SuccessMessageMixin, LoginRequiredMixin, CustomAdminMixin, UpdateView):
    model = Report
    form_class = ReportUpdate
    template_name = 'horizon/UpdateRequest.html'
    success_url = reverse_lazy('horizon:report_list')

    def form_valid(self, form):
        report = form.save(commit=False)
        report.mod = Admin.objects.get(user=self.request.user)
        if self.request.POST['expires_time'] == 'd':
            date = timezone.localtime(timezone.now()) + timezone.timedelta(days=int(self.request.POST['expires']))
        else:
            date = timezone.localtime(timezone.now()) + timezone.timedelta(hours=int(self.request.POST['expires']))

        if report.status == 'zaakceptowane':
            mc = connect()
            if self.request.POST['type_report'] == 'ban':
                ban = Ban.objects.create(user=report.user, type=self.request.POST['type'],
                                         expires=date, reason=self.request.POST['reason'],
                                         admin=self.request.user)
                if self.request.POST['type'] == 'PERMAMENTLY':
                    mc_ban = mc.command(
                        'ban ' + str(report.user.username) + ' ' + str(self.request.POST['reason']))
                else:
                    mc_ban = mc.command('tempban ' + str(report.user.username)
                                        + ' ' + self.request.POST['expires'] + self.request.POST['expires_time'] + ' ' +
                                        str(self.request.POST['reason']))
            else:
                if not self.request.POST['type'] == 'PERMAMENTLY':
                    mute = Mute.objects.create(user=report.user, expires=date,
                                               reason=self.request.POST['reason'],
                                               admin=self.request.user)

                    mc_mute = mc.command(
                        'tempmute ' + str(report.user.username) + ' ' + str.upper(
                            self.request.POST['expires'] + self.request.POST['expires_time']) + ' ' + str(
                            self.request.POST['reason']))

        report.save()
        return super(ReportUpdateView, self).form_valid(form)


class NewsListView(ListView):
    model = New
    template_name = 'horizon/news/ListNewsView.html'
    paginate_by = 3
    ordering = ['-created']
    context_object_name = 'news'


class NewsCreateView(CreateView, LoginRequiredMixin, CustomRoleOwnerMixin):
    model = New
    fields = ['title', 'content', 'img']
    template_name = 'horizon/news/CreateNewsView.html'

    def form_valid(self, form):
        news = form.save(commit=False)
        news.admin = Admin.objects.get(user=self.request.user)
        news.save()
        return HttpResponseRedirect(reverse('horizon:news_create'))


class NewsDetailView(DetailView):
    model = New
    template_name = 'horizon/news/DetailNewsView.html'


class NewsUpdateView():
    pass
