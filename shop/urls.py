from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from .views import shop, SmsPaymentView
app_name = 'shop'


urlpatterns = (
    path(r'', shop, name='shop'),
    path(r'sms', SmsPaymentView.as_view(), name='sms'),
)
