from django.contrib.auth.mixins import AccessMixin

from accounts.models import Admin, Profile


class CustomAdminMixin(AccessMixin):
    """Verify that the current user is authenticated."""

    def dispatch(self, request, *args, **kwargs):
        admin = Admin.objects.filter(user=request.user)
        if not admin.count():
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class CustomRoleOwnerMixin(AccessMixin):
    """Verify that the current user is authenticated."""

    def dispatch(self, request, *args, **kwargs):
        admin = Profile.objects.filter(user=request.user, rank='Właściciel')
        admin2 = Profile.objects.filter(user=request.user, rank='Właściciel')
        if not admin.count() or not admin2.count():
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
