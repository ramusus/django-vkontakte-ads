from vkontakte_api.factories import DjangoModelNoCommitFactory
from models import Account, Ad, Campaign, Client
import factory
import random


class AccountFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Account

    remote_id = factory.Sequence(lambda n: n)


class ClientFactory(DjangoModelNoCommitFactory):
    FACTORY_FOR = Client

    remote_id = factory.Sequence(lambda n: n)


class CampaignFactory(DjangoModelNoCommitFactory):
    FACTORY_FOR = Campaign

    remote_id = factory.Sequence(lambda n: n)


class AdFactory(DjangoModelNoCommitFactory):
    FACTORY_FOR = Ad

    remote_id = factory.Sequence(lambda n: n)
    cpc = bool(random.randint(0,1))
    cpm = not bool(cpc)
