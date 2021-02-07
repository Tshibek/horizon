from django.contrib import admin
from django import forms
from .models import Ban, Mute, StoneLevel, KitName, Kit, Location,  NameLocation, BuyLogs, Report


class BansAdminForm(forms.ModelForm):
    class Meta:
        model = Ban
        fields = '__all__'


class BansAdmin(admin.ModelAdmin):
    form = BansAdminForm
    list_display = ('user', 'type', 'reason', 'admin')
    list_display_links = ('user', 'admin')
    list_filter = ('type', 'admin', 'expires', 'created')


class MutesAdminForm(forms.ModelForm):
    class Meta:
        model = Mute
        fields = '__all__'


class MutesAdmin(admin.ModelAdmin):
    form = MutesAdminForm
    list_display = ('user', 'reason', 'admin', 'expires')
    list_display_links = ('user', 'admin')
    list_filter = ('admin', 'expires', 'created')


class StoneLevelsForms(forms.ModelForm):
    class Meta:
        model = StoneLevel
        fields = '__all__'


class StoneLevelsAdmin(admin.ModelAdmin):
    form = StoneLevelsForms
    list_display = ('user', 'level', 'exp', 'all_stone')
    list_display_links = ('user',)
    list_filter = ('level', 'exp', 'all_stone')


class KitNameForms(forms.ModelForm):
    class Meta:
        model = KitName
        fields = '__all__'


class KitNameAdmin(admin.ModelAdmin):
    form = KitNameForms
    list_display = ('name',)
    list_display_links = ('name',)
    list_filter = ('name',)


class KitForms(forms.ModelForm):
    class Meta:
        model = Kit
        fields = '__all__'


class KitAdmin(admin.ModelAdmin):
    form = KitForms
    list_display = ('user', 'kit', 'get_kit',)
    list_display_links = ('kit',)
    list_filter = ('user', 'kit', 'get_kit')


class NameLocationForms(forms.ModelForm):
    class Meta:
        model = NameLocation
        fields = '__all__'


class NameLocationAdmin(admin.ModelAdmin):
    form = NameLocationForms
    list_display = ('name',)
    list_display_links = ('name',)
    list_filter = ('name',)



class LocationForms(forms.ModelForm):
    class Meta:
        model = Location
        fields = '__all__'


class LocationAdmin(admin.ModelAdmin):
    form = LocationForms
    list_display = ('name', 'cord',)
    list_display_links = ('name',)
    list_filter = ('name', 'cord')


class BuyLogsForm(forms.ModelForm):
    class Meta:
        model = BuyLogs
        fields = '__all__'


class BuyLogsAdmin(admin.ModelAdmin):
    form = BuyLogsForm
    list_display = ('user', 'name', 'date')
    list_display_links = ('name',)
    list_filter = ('name', 'date')


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = '__all__'


class ReportAdmin(admin.ModelAdmin):
    form = ReportForm
    list_display = ('user', 'report_user', 'status', 'mod', 'created')
    list_display_links = ('user',)
    list_filter = ('created', 'status')


admin.site.register(Ban, BansAdmin)
admin.site.register(Mute, MutesAdmin)
admin.site.register(StoneLevel, StoneLevelsAdmin)
admin.site.register(KitName, KitNameAdmin)
admin.site.register(Kit, KitAdmin)
admin.site.register(NameLocation, NameLocationAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(BuyLogs, BuyLogsAdmin)
admin.site.register(Report, ReportAdmin)
