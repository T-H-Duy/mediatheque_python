import pytest
from django.test import Client
from django.urls import reverse
from .models import Member, Media


@pytest.mark.django_db
def test_create_member():
    member = Member.objects.create(
        first_name='Dummy',
        last_name='Doll',
        email='dummy@hotmail.fr',
        tel='0601010101',
    )

    assert member.first_name == 'Dummy'
    assert member.last_name == 'Doll'
    assert member.email == 'dummy@hotmail.fr'
    assert member.tel == '0601010101'


@pytest.mark.django_db
def test_delete_member():
    member = Member.objects.create(
        first_name='Dummy',
        last_name='Doll',
        email='dummy@hotmail.fr',
        tel='0601010101',
    )

    assert Member.objects.count() == 1

    client = Client()
    response = client.post(reverse('delete_member', args=[member.id]))

    assert response.status_code == 302
    assert Member.objects.count() == 0


@pytest.mark.django_db
def test_update_member():
    member = Member.objects.create(
        first_name='Dummy',
        last_name='Doll',
        email='dummy@hotmail.fr',
        tel='0601010101',
    )

    assert member.first_name == 'Dummy'
    assert member.last_name == 'Doll'
    assert member.email == 'dummy@hotmail.fr'
    assert member.tel == '0601010101'

    client = Client()

    data = {
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'johndoe@gmail.com',
        'tel': '0607070707',
    }

    response = client.post(reverse('update_member', args=[member.id]), data)

    assert response.status_code == 302

    member.refresh_from_db()

    assert member.first_name == 'John'
    assert member.last_name =='Doe'
    assert member.email == 'johndoe@gmail.com'


@pytest.mark.django_db
def test_add_media():
    media = Media.objects.create(
        name='1984',
        creator='George Orwell',
        type_media='livre',
        disponible=True,
    )

    assert media.name == '1984'
    assert media.creator == 'George Orwell'
    assert media.type_media == 'livre'

