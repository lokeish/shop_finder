from django.test import TestCase
from django.urls import reverse
from django.contrib.gis.geos import Point
from shops.models import Shop
from shops.util import helper


class ShopTestViews(TestCase):
    def setUp(self):
        self.shop_test_obj = Shop.objects.create(name='Test Shop Location', location=Point(78.99, -90.12), address='Startup')

    def test_create_shop_view(self):
        url = reverse('create_shop')
        data = {'name': 'Instamart', 'latitude': '99.00', 'longitude': '11.1011', 'address': 'Startup'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Shop.objects.filter(name='Instamart').exists())

    def test_create_shop_existing_name(self):
        url = reverse('create_shop')
        data = {'name': self.shop_test_obj.name, 'latitude': '99.00', 'longitude': '11.1011', 'address': 'Startup'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Name exists already')

    def test_update_shop(self):
        url = reverse('update_shop', args=[self.shop_test_obj.pk])
        data = {'name': 'Updated Shop', 'latitude': '100', 'longitude': '99', 'address': 'NPCI'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.shop_test_obj.refresh_from_db()
        self.assertEqual(self.shop_test_obj.name, 'Updated Shop')
        self.assertEqual(self.shop_test_obj.location.x, 99)
        self.assertEqual(self.shop_test_obj.location.y, 100)
        self.assertEqual(self.shop_test_obj.address, 'NPCI')


    def test_update_shop_with_existing_name(self):
        other_shop = Shop.objects.create(name='Other Shop', location=Point(2, 2), address='456 Other St.')
        url = reverse('update_shop', args=[self.shop_test_obj.pk])
        data = {'name': other_shop.name, 'latitude': '1', 'longitude': '1', 'address': 'Bangalore'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Name exists already')

    def test_search_shops_view(self):
        url = reverse('shop_search')
        data = {'latitude': '0', 'longitude': '0', 'distance': '10'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)

    def test_shop_list_view(self):
        url = reverse('shop_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.shop_test_obj.name)

    def test_shop_detail_view_with_invalid_id(self):
        url = reverse('shop_detail', args=[100])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_check_website_view(self):
        url = reverse('shop_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)