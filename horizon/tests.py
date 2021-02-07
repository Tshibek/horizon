import unittest
from django.urls import reverse
from django.test import Client
from .models import Bans
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType


def create_django_contrib_auth_models_user(**kwargs):
    defaults = {}
    defaults["username"] = "username"
    defaults["email"] = "username@tempurl.com"
    defaults.update(**kwargs)
    return User.objects.create(**defaults)


def create_django_contrib_auth_models_group(**kwargs):
    defaults = {}
    defaults["name"] = "group"
    defaults.update(**kwargs)
    return Group.objects.create(**defaults)


def create_django_contrib_contenttypes_models_contenttype(**kwargs):
    defaults = {}
    defaults.update(**kwargs)
    return ContentType.objects.create(**defaults)


def create_bans(**kwargs):
    defaults = {}
    defaults["name"] = "name"
    defaults.update(**kwargs)
    return Bans.objects.create(**defaults)


class BansViewTest(unittest.TestCase):
    '''
    Tests for Bans
    '''
    def setUp(self):
        self.client = Client()

    def test_list_bans(self):
        url = reverse('horizon_bans_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_bans(self):
        url = reverse('horizon_bans_create')
        data = {
            "name": "name",
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_bans(self):
        bans = create_bans()
        url = reverse('horizon_bans_detail', args=[bans.slug,])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_bans(self):
        bans = create_bans()
        data = {
            "name": "name",
        }
        url = reverse('horizon_bans_update', args=[bans.slug,])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


