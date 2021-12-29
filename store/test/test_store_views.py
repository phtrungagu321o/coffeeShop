import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_root_url(client):
    url = reverse('store:index')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_root_url2(client):
    url = reverse('store:product_all')
    response = client.get(url)
    assert response.status_code == 200

