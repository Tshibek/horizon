from django.db import models
from django.utils import timezone

from accounts.models import User


class Voucher(models.Model):
    voucher = models.CharField(max_length=8, blank=True, unique=True)
    money = models.SmallIntegerField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    expires = models.DateTimeField()
    used = models.BooleanField(default=False)

    def __str__(self):
        return self.voucher


class VoucherLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    voucher = models.CharField(max_length=8)
    money = models.SmallIntegerField(default=0)
    added = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Kod %s o wartości %s dla %s'.format(self.voucher, self.money, self.user.username)
