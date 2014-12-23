# -*- coding: utf-8 -*-
from django.core.management.base import AppCommand, LabelCommand
#from django.conf import settings
from optparse import make_option
from vkontakte_ads.models import Ad, Account, Campaign, Targeting
import logging

logger = logging.getLogger('command_fetch_vkontakte_ads_data')

class Command(AppCommand):
    help = 'Fetch all ads data from vkontakte via API'
    requires_model_validation = True

    option_list = LabelCommand.option_list + (
        make_option('--reset', action='store_true', dest='delete', help='Delete all content data before fetching'),
    )

    def handle(self, **options):
        reset = options.get('reset')

        if reset:
            Ad.objects.all().delete()
            Account.objects.all().delete()
            Campaign.objects.all().delete()
            Targeting.objects.all().delete()

        for account in Account.remote.fetch():
            logger.info(u'Получили аккаунт "%s"' % account)

            for client in account.fetch_clients():
                logger.info(u'Получили клиента "%s" аккаунта "%s"' % (client, account))
                for campaign in client.fetch_campaigns():
                    logger.info(u'Получили кампанию "%s" клиента "%s"' % (campaign, client))
                    campaign.fetch_ads()
                    logger.info(u'Получили рекламные объявления кампании "%s" клиента "%s"' % (campaign, client))
                    campaign.fetch_ads_targeting()
                    logger.info(u'Получили таргетинг рекламных объявлений кампании "%s" клиента "%s"' % (campaign, client))
                    campaign.fetch_ads_layout()
                    logger.info(u'Получили лэйаут рекламных объявлений кампании "%s" клиента "%s"' % (campaign, client))

            for campaign in account.fetch_campaigns():
                logger.info(u'Получили кампанию "%s" аккаунта "%s"' % (campaign, account))
                campaign.fetch_ads()
                logger.info(u'Получили рекламные объявления кампании "%s" аккаунта "%s"' % (campaign, account))
                campaign.fetch_ads_targeting()
                logger.info(u'Получили таргетинг рекламных объявлений кампании "%s" аккаунта "%s"' % (campaign, account))
                campaign.fetch_ads_layout()
                logger.info(u'Получили лэйаут рекламных объявлений кампании "%s" аккаунта "%s"' % (campaign, account))