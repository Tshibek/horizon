from django.core.management.base import BaseCommand
from django.utils import timezone
from voucher.models import Voucher


class Command(BaseCommand):
    help = 'Deletes expired rows'

    def handle(self, *args, **options):
        date = timezone.now()
        Voucher.objects.filter(expires__lt=date).delete()
