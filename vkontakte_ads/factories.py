import random

import factory
from django.utils import timezone
from vkontakte_api.factories import DjangoModelNoCommitFactory

from . import models


class AccountFactory(factory.DjangoModelFactory):

    remote_id = factory.Sequence(lambda n: n)
    fetched = factory.LazyAttribute(lambda o: timezone.now())

    class Meta:
        model = models.Account


class ClientFactory(DjangoModelNoCommitFactory):

    remote_id = factory.Sequence(lambda n: n)
    fetched = factory.LazyAttribute(lambda o: timezone.now())

    class Meta:
        model = models.Client


class CampaignFactory(DjangoModelNoCommitFactory):

    remote_id = factory.Sequence(lambda n: n)
    fetched = factory.LazyAttribute(lambda o: timezone.now())

    class Meta:
        model = models.Campaign


class AdFactory(DjangoModelNoCommitFactory):

    remote_id = factory.Sequence(lambda n: n)
    fetched = factory.LazyAttribute(lambda o: timezone.now())
    cpc = bool(random.randint(0, 1))
    cpm = not bool(cpc)

    class Meta:
        model = models.Ad
