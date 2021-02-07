from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views
app_name = 'user'


urlpatterns = (
    path(r'login/', auth_views.LoginView.as_view(template_name='accounts/login_in.html', redirect_authenticated_user=True), name='login'),
    path(r'password/', views.change_password, name='change_password'),
    path(r'password/done/', auth_views.PasswordChangeDoneView.as_view(), name='change_password_done'),
    path(r'<slug:username>', views.profil, name='profile'),
    path(r'<slug:username>/ustawienia', views.profilSettings, name='profil_ssettings'),
    path(r'<slug:username>/reporty', views.user_report, name='user_report'),
    path(r'<int:desc_pk>/opis', views.AdminUpdate.as_view(), name='user_desc'),
    path(r'logout/', views.LogoutView, name='logout'),
)
