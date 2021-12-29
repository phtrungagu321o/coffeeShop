import pytest
from django.urls import reverse


def test_category_str(product_category):
    assert product_category.__str__() == 'coffee'


def test_category_reverse(client, product_category):
    category = product_category
    url = reverse('store:category_list', args=[category])
    response = client.get(url)
    assert response.status_code == 200


def test_producttype_str(product_type):
    assert product_type.__str__() == 'ice'


def test_product_spec_str(product_specification):
    assert product_specification.__str__() == "size"


def test_product_str(product):
    assert product.__str__() == 'product_title'


def test_product_url_resolve(client, product):
    slug = 'product_slug'
    category = '1'
    url = reverse('store:product_detail', args=[slug, category])
    response = client.get(url)
    assert response.status_code == 200


def test_product_specification_value(product_spec_value):
    assert product_spec_value.__str__() == '3'
