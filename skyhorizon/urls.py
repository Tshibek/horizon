from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
  url(r'^admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
  url(r'^panel/owner/jet', include('jet.urls', 'jet')),  # Django JET URLS
  url(r'^panel/owner/jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),
  url(r'^panel/owner/admin', admin.site.urls),
  url(r'', include('horizon.urls', namespace='horizon')),
  url(r'user/', include('accounts.urls', namespace='user')),
  url(r'sklep/', include('shop.urls', namespace='shop')),
  url(r'voucher/', include('voucher.urls', namespace='voucher')),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

