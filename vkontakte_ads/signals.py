# -*- coding: utf-8 -*-
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.conf import settings
from models import Targeting, Ad

if 'vkontakte_places' in settings.INSTALLED_APPS:
    from vkontakte_places.models import City

    @receiver(post_save, sender=Targeting)
    def fetch_cities_for_targeting(sender, instance, created, **kwargs):
        if instance.cities:
            City.remote.fetch(ids=instance.cities.split(','))
        if instance.cities_not:
            City.remote.fetch(ids=instance.cities_not.split(','))

if 'vkontakte_groups' in settings.INSTALLED_APPS:
    from vkontakte_groups.models import Group

    @receiver(post_save, sender=Targeting)
    def fetch_cities_for_targeting(sender, instance, created, **kwargs):
        if instance.groups:
            Group.remote.fetch(ids=instance.groups.split(','))

# @receiver(post_delete, sender=Ad)
# def post_delete_ad(sender, instance, *args, **kwargs):
#     import ipdb; ipdb.set_trace()
#     if instance.layout:
#         instance.layout.delete()
#     if instance.targeting:
#         instance.targeting.delete()
#     if instance.image:
#         instance.image.delete()
