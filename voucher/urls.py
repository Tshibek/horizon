from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from .views import VoucherCreateView, CheckVoucher, VoucherAdminListView, VoucherUserListView
app_name = 'voucher'


urlpatterns = (
    path(r'create', VoucherCreateView.as_view(), name='voucher_create'),
    path(r'lista/admin', VoucherAdminListView.as_view(), name='voucher_list_admin'),
    path(r'lista', VoucherUserListView.as_view(), name='voucher_list_user'),
    path(r'check', CheckVoucher, name='voucher_update'),
)
