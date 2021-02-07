from django.db import models
from accounts.models import User


# Create your models here.

class PaymentRequest(models.Model):
    TYPE_CHOICES = (
        ('unban', 'unban'),
        ('wallet', 'wallet'),
    )
    PAYMENT_CHOICES = (
        ('sms', 'sms'),
        ('psc', 'psc'),
        ('paypal', 'paypal'),
        ('przelew', 'przelew'),
    )
    STATUS_CHOICES = (
        ('SUCCESS', 'SUCCESS'),
        ('PENDING', 'PENDING'),
        ('FAILURE', 'FAILURE'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=8, choices=TYPE_CHOICES)
    payment = models.CharField(max_length=7, choices=PAYMENT_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    sms_code = models.CharField(max_length=90, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    money = models.FloatField(default=0)

    def __str__(self):
        return self.payment

    class Meta:
        unique_together = ('user', 'sms_code')
