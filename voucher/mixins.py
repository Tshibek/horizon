from django.contrib.auth.mixins import AccessMixin

from accounts.models import Profile


class CustomRoleAdminMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        set_role = Profile.objects.filter(user=request.user, rank='Właściciel')
        if not set_role.count():
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
