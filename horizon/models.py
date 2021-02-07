from django.contrib.contenttypes.models import ContentType
from django.db import models as models
from django.db.models import Count

from accounts.models import User, Admin
from ckeditor.fields import RichTextField

class Ban(models.Model):
    TYPE_CHOICES = (
        ('TEMPORARY', 'TEMPORARY'),
        ('PERMAMENTLY', 'PERMAMENTLY'),
    )
    user = models.OneToOneField(User, related_name='banned', on_delete=models.CASCADE)
    type = models.CharField(max_length=12, choices=TYPE_CHOICES)
    reason = models.CharField(max_length=190)
    admin = models.ForeignKey(User, related_name='ban_admin', on_delete=models.DO_NOTHING)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    expires = models.DateTimeField(null=True, blank=True)


class Mute(models.Model):
    user = models.OneToOneField(User, related_name='muted', on_delete=models.CASCADE)
    reason = models.CharField(max_length=190)
    admin = models.ForeignKey(User, related_name='mute_admin', on_delete=models.DO_NOTHING)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    expires = models.DateTimeField()


class StoneLevel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    level = models.SmallIntegerField(default=1)
    exp = models.SmallIntegerField(default=0)
    next_level = models.SmallIntegerField(default=5)
    all_stone = models.SmallIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

    def ranking_lvl(self):
        aggregate = StoneLevel.objects.filter(level__gt=self.level).aggregate(ranking=Count('level'))
        return aggregate['ranking'] + 1

    def ranking_stone(self):
        aggregate = StoneLevel.objects.filter(all_stone__gt=self.all_stone).aggregate(ranking=Count('all_stone'))
        return aggregate['ranking'] + 1

class KitName(models.Model):
    name = models.CharField(max_length=190)
    created = models.DateTimeField(auto_now_add=True)


class Kit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    kit = models.ForeignKey(KitName, on_delete=models.CASCADE)
    get_kit = models.DateTimeField()


class NameLocation(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Location(models.Model):
    name = models.ForeignKey(NameLocation, on_delete=models.CASCADE)
    cord = models.CharField(max_length=196)


class BuyLogs(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=190)
    date = models.DateTimeField(auto_now_add=True)


class Report(models.Model):
    STATUS_CHOICES = (
        ('odrzucone', 'odrzucone'),
        ('oczekuje', 'oczekuje'),
        ('zaakceptowane', 'zaakceptowane'),
    )
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='reporting')
    report_user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='reported')
    status = models.CharField(max_length=25, choices=STATUS_CHOICES, default='oczekuje')
    title = models.CharField(max_length=190)
    content = models.TextField()
    evidence = models.URLField()
    created = models.DateTimeField(auto_now_add=True)
    mod = models.ForeignKey(Admin, on_delete=models.DO_NOTHING, blank=True, null=True)

    class Meta:
        unique_together = ('user', 'report_user',)


class New(models.Model):
    title = models.CharField(max_length=190)
    content = RichTextField()
    img = models.ImageField(upload_to='news/%Y/%m/%d/', max_length=190, default='default/skyhorizon.png')
    created = models.DateTimeField(auto_now_add=True)
    admin = models.ForeignKey(Admin, on_delete=models.DO_NOTHING)
