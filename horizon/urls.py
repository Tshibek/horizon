
from django.urls import path

from . import views

app_name = 'horizon'
urlpatterns = (
    # urls for Bans
    path('', views.home_page, name='home'),
    path(r'kontakt', views.contact, name='contact'),
    path(r'szukaj', views.search, name='search'),
    path(r'ranking', views.ranking, name='ranking'),
    path(r'regulamin', views.rules, name='rules'),
    path(r'faq', views.faq, name='faq'),
    path(r'report/dodaj', views.ReportCreateView.as_view(), name='report_create'),
    path(r'reporty', views.ReportListView.as_view(), name='report_list'),
    path(r'reporty/zaakceptowane', views.ReportAcceptListView.as_view(), name='report_list_accept'),
    path(r'reporty/odrzucone', views.ReportDeclineListView.as_view(), name='report_list_decline'),
    path(r'reporty/oczekuje', views.ReportPendingListView.as_view(), name='report_list_pending'),
    path(r'report/<int:pk>', views.ReportUpdateView.as_view(), name='report_update'),
    path(r'bany', views.BanView, name='bans'),
    path(r'administracja', views.AdminsView, name='admins'),
    path(r'news/create', views.NewsCreateView.as_view(), name='news_create'),
    path(r'news', views.NewsListView.as_view(), name='news_list'),
    path(r'news/podglad/<int:pk>', views.NewsDetailView.as_view(), name='news_detail'),





    # path('create/', views.BansCreateView.as_view(), name='horizon_bans_create'),
    # path('detail/<slug:slug>/', views.BansDetailView.as_view(), name='horizon_bans_detail'),
    # path('update/<slug:slug>/', views.BansUpdateView.as_view(), name='horizon_bans_update'),
)

