from django.test import TestCase
from django.contrib.auth.models import User
from .models import Client


class ClientModelTest(TestCase):
    def setUp(self):
        self.client_obj = Client.objects.create(
            nom='Dupont',
            prenom='Jean',
            email='jean.dupont@example.com',
            telephone='0600000000',
            statut='actif',
            categorie='particulier',
        )

    def test_full_name(self):
        self.assertEqual(self.client_obj.get_full_name(), 'Jean Dupont')

    def test_str(self):
        self.assertEqual(str(self.client_obj), 'Jean Dupont')

    def test_statut_default(self):
        self.assertEqual(self.client_obj.statut, 'actif')
