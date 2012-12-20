from models import Account, Ad, Campaign
import factory
import random

class AccountFactory(factory.Factory):
    FACTORY_FOR = Account

    remote_id = factory.Sequence(lambda n: n)

class CampaignFactory(factory.Factory):
    FACTORY_FOR = Campaign

    remote_id = factory.Sequence(lambda n: n)

class AdFactory(factory.Factory):
    FACTORY_FOR = Ad

    remote_id = factory.Sequence(lambda n: n)