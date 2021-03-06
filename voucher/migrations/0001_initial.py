# Generated by Django 2.1.5 on 2019-02-22 12:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Voucher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('voucher', models.CharField(blank=True, max_length=8, unique=True)),
                ('money', models.SmallIntegerField(blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('expires', models.DateTimeField()),
                ('used', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='VoucherLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('voucher', models.CharField(max_length=8)),
                ('money', models.SmallIntegerField(default=0)),
                ('added', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
