# -*- coding: utf-8 -*-
from annoying.decorators import signals
from django.conf import settings
from models import Targeting

if 'vkontakte_places' in settings.INSTALLED_APPS:
    from vkontakte_places.models import City

    @signals.post_save(sender=Targeting)
    def fetch_cities_for_targeting(sender, instance, created, **kwargs):
        if instance.cities:
            City.remote.fetch(ids=instance.cities.split(','))
        if instance.cities_not:
            City.remote.fetch(ids=instance.cities_not.split(','))

if 'vkontakte_groups' in settings.INSTALLED_APPS:
    from vkontakte_groups.models import Group

    @signals.post_save(sender=Targeting)
    def fetch_cities_for_targeting(sender, instance, created, **kwargs):
        if instance.groups:
            Group.remote.fetch(ids=instance.groups.split(','))