from django.test import TestCase, Client
from django.urls import reverse


class MyViewTests(TestCase):
    # @TODO da rivedere perché non funziona la reverse ...
    def setUp(self):
        self.client = Client()

    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'albdif/home.html')
        self.assertContains(response, 'Home Page')

    def test_home_view(self):
        response = self.client.get(reverse('proprieta_partner'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'albdif/proprieta_list.html')
        self.assertContains(response, 'Home Page')


