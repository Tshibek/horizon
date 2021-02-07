from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.db.models import Max, Count, Func, F
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.fields import AutoSlugField

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_('username'), max_length=200, unique=True)
    ip = models.GenericIPAddressField(_('ip'), blank=True, null=True)
    uuid = models.CharField(_('uuid'), max_length=64, blank=True, null=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True, editable=False)
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
    )

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.username

    def get_username(self):
        return self.username

    def get_uuid(self):
        return self.uuid

    def profil(self):
        return Profile.objects.get(user=self.id)

    def get_join(self):
        return list(Profile.objects.all().aggregate(Max('join_count')).values())[0]

    def get_count(self):
        return User.objects.all().count()


class Profile(models.Model):
    RANK_CHOICES = (
        ('Gracz', 'Gracz'),
        ('Vip', 'Vip'),
        ('SVip', 'SVip'),
        ('Hero', 'Hero'),
        ('Helper', 'Helper'),
        ('Admin', 'Admin'),
        ('HeadAdmin', 'HeadAdmin'),
        ('Właściciel', 'Właściciel'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rank = models.CharField(max_length=30, default='Gracz', choices=RANK_CHOICES)
    buy_rank = models.DateTimeField(null=True)
    join_count = models.SmallIntegerField(default=0)
    money = models.SmallIntegerField(default=0)
    money_is = models.SmallIntegerField(default=0)
    kills = models.SmallIntegerField(default=0)
    deaths = models.SmallIntegerField(default=0)

    def __str__(self):
        return self.user.username

    @receiver(post_save, sender=User)
    def update_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
        instance.profile.save()

    def ranking_pvp(self):
        aggregate = Profile.objects.filter(kills__gt=self.kills).aggregate(ranking=Count('kills'))
        return aggregate['ranking'] + 1

    def stone(self):
        from horizon.models import StoneLevel
        return StoneLevel.objects.get(user=self.user)

    def ban(self):
        from horizon.models import Ban
        return Ban.objects.filter(user=self.user).first()

    def mute(self):
        from horizon.models import Mute
        return Mute.objects.filter(user=self.user).first()

    def uuid(self):
        return self.user.uuid

    def username(self):
        return self.user.username


class Admin(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='admin_user')
    special = models.CharField(max_length=30, blank=True, null=True)
    desc = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
