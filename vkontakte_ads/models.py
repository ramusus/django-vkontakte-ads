# -*- coding: utf-8 -*-
from django.db import models
from django.db.models.query import QuerySet
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext as _
from django.conf import settings
from datetime import datetime
from vkontakte import VKError
from vkontakte_api import fields
from vkontakte_api.models import VkontakteManager, VkontakteModel, VkontaktePKModel, VkontakteContentError, VkontakteCRUDModel, VkontakteCRUDManager
from smart_selects.db_fields import ChainedForeignKey
import simplejson as json
import requests
import logging
import time
import os

COMMIT_REMOTE = getattr(settings, 'VKONTAKTE_ADS_COMMIT_REMOTE', True)

log = logging.getLogger('vkontakte_ads')

ERROR_CODES = (
    (1, _('Unknown error occurred.')),
    (4, _('Incorrect signature.')),
    (5, _('User authorization failed.')),
    (6, _('Too many requests per second.')),
    (7, _('Permission to perform this action is denied by user.')),
    (10, _('Internal server error')),
    (100, _('One of the parameters specified was missing or invalid.')),
    (600, _('Permission denied. You have no access to operations specified with given object(s).')),
    (603, _('Specific error.')),
)

ACCOUNT_ACCESS_ROLE_CHOICES = (
    ('admin', u'главный администратор'),
    ('manager', u'администратор'),
    ('reports', u'наблюдатель'),
)

# taked from here view-source:http://vk.com/adsedit?ad_id=2081950
TARGETING_GROUP_TYPES_CHOICES = [[32,u"R&B"],[33,u"Rap & Hip-Hop"],[92,u"Автомобили"],[93,u"Автоспорт"],[58,u"Азартные игры"],[81,u"Академические группы"],[47,u"Баскетбол"],[76,u"Бизнес"],[79,u"Благотворительность"],[26,u"Блюз"],[55,u"Боевые искусства"],[15,u"ВКонтакте"],[49,u"Велосипеды"],[54,u"Водный спорт"],[86,u"Города"],[82,u"Группы выпускников"],[89,u"Дачи"],[27,u"Джаз"],[90,u"Дискуссионные клубы"],[12,u"Домашние животные"],[1,u"Друзья"],[64,u"Железо"],[10,u"Здоровье"],[52,u"Зимние виды спорта"],[13,u"Знаки зодиака"],[39,u"Знакомства"],[61,u"Игры"],[28,u"Инди"],[6,u"История"],[18,u"Кино"],[29,u"Классика"],[30,u"Латина"],[53,u"Легкая атлетика"],[17,u"Литература"],[88,u"Места отдыха"],[31,u"Металл"],[65,u"Мобильные технологии"],[77,u"Молодежные движения"],[94,u"Мотоспорт"],[75,u"Музыкальные движения"],[63,u"Мультимедиа"],[95,u"Настольные игры"],[9,u"Наука"],[3,u"Новости"],[24,u"Обмен музыкой"],[83,u"Общежития"],[85,u"Общества и клубы"],[80,u"Общества и клубы"],[5,u"Общество"],[14,u"Однофамильцы и тезки"],[40,u"Отношения полов"],[4,u"Политика"],[67,u"Программирование"],[96,u"Работа"],[23,u"Радио и Интернет-радио"],[34,u"Регги"],[8,u"Религия"],[35,u"Рок"],[51,u"Ролики"],[66,u"Сайты"],[62,u"Софт"],[56,u"Спортивные игры"],[78,u"Спортивные организации"],[87,u"Страны"],[84,u"Студенческие советы"],[36,u"Танцевальная"],[50,u"Танцы"],[16,u"Творчество"],[19,u"Театр"],[25,u"Тексты и аккорды"],[22,u"Телевидение"],[46,u"Теннис"],[41,u"Технические вопросы"],[11,u"Туризм и путешествия"],[60,u"Университетский спорт"],[57,u"Упражнения и фитнес"],[91,u"Фан-клубы"],[7,u"Философия"],[37,u"Фолк"],[20,u"Фотография и живопись"],[45,u"Футбол"],[48,u"Хоккей"],[59,u"Экстремальный спорт"],[38,u"Электронная"],[21,u"Юмор"],[2,u"Языки"]]
TARGETING_RELIGIONS_CHOICES = [[102,u"Православие"],[103,u"Православный"],[104,u"Православная"],[105,u"Orthodox"],[101,u"Католицизм"],[99,u"Католик"],[98,u"Католичка"],[97,u"Catholic"],[96,u"catholicism"],[107,u"Протестантизм"],[108,u"Протестант"],[167,u"Иудаизм"],[168,u"Иудей"],[169,u"Иудейка"],[170,u"Jewish"],[171,u"Judaism"],[122,u"Islam"],[123,u"Muslim"],[124,u"Ислам"],[125,u"Мусульманин"],[126,u"Мусульманка"],[129,u"Буддизм"],[130,u"Буддист"],[131,u"Buddhism"],[139,u"Конфуцианство"],[138,u"Даосизм"],[200,u"Светский гуманизм"],[201,u"Христианство"],[202,u"Христианин"],[203,u"Христианство"],[204,u"Christian"],[205,u"Атеизм"],[206,u"Атеист"],[207,u"Атеистка"]]
TARGETING_SEX_CHOICES = ((0, u'любой'), (1, u'женский'), (2, u'мужской'))
TARGETING_STATUS_CHOICES = ((1, u'Не женат/Не замужем'),(2, u'Есть подруга/Есть друг'),(3, u'Полмолвлен(а)'),(4, u'Женат/Замужем'),(5, u'Все сложно'),(6, u'В активном поиске'))


class VkontakteAdsMixin:
    methods_namespace = 'ads'
    methods_access_tag = 'ads'


class VkontakteAdsModel(VkontakteAdsMixin, VkontakteModel):
    class Meta:
        abstract = True


class VkontakteAdsIDModel(VkontakteAdsMixin, VkontaktePKModel):
    class Meta:
        abstract = True

    def fetch_ads(self, model=None, ids=None):
        '''
        Get all ads|ad_targetings|ad_layouts of campaign
        '''
        if not ids:
            ids = 'null'
        elif not isinstance(ids, list):
            raise ValueError('Argument ids must be list or tuple')

        kwargs = {
            'account_id': self.account.remote_id,
            'campaign_ids': [int(self.remote_id)],
            'ad_ids': ids,
        }
        if self.client:
            kwargs.update({'client_id': self.client.remote_id})

        instances = model.remote.get(**kwargs)
        instances_saved = []

        for instance in instances:
            instance.campaign = self
            instance.fetched = datetime.now()
            instance._commit_remote = False
            instances_saved += [model.remote.get_or_create_from_instance(instance)]

        return instances_saved

    def fetch_campaigns(self, account, client=None, ids=None):
        '''
        Get all campaigns of account
        '''
        if not ids:
            ids = 'null'
        elif not isinstance(ids, list):
            raise ValueError('Argument ids must be list or tuple')

        kwargs = {
            'account_id': account.remote_id,
            'campaign_ids': ids,
        }
        if client:
            kwargs.update({'client_id': client.remote_id})

        try:
            instances = Campaign.remote.get(**kwargs)
        except VKError, e:
            if e.code == 100:
                return []
            else:
                raise e
        instances_saved = []

        for instance in instances:
            instance.account = account
            instance.fetched = datetime.now()
            instance._commit_remote = False
            if client:
                instance.client = client
            instances_saved += [Campaign.remote.get_or_create_from_instance(instance)]

        return instances_saved

    def fetch_statistics(self, **kwargs):
        '''
        Get statistics of content object
        '''
        return Statistic.remote.fetch(objects=[self], **kwargs)


class VkontakteAdsIDContentModel(VkontakteCRUDModel, VkontakteAdsIDModel):
    '''
    Model with remote_id and CRUD remote methods
    '''
    class Meta:
        abstract = True

    def __unicode__(self):
        return (u'(архив) ' if self.archived else '') + self.name

    def parse_remote_id_from_response(self, response):
        '''
        Handle response errors
        # http://vk.com/developers.php?oid=-1&p=ads.createAds
        # http://vk.com/developers.php?oid=-1&p=ads.updateAds
        If id in response == 0 -> raise error, otherwise log error and return it for saving to local DB
        '''
        error_message = "Error while saving %s. Code %s, description: '%s'" % (self._meta.object_name, response[0].get('error_desc'), response[0].get('error_desc'))
        if response[0]['id']:
            if 'error_code' in response[0]:
                # TODO: add message to contrib.messages
                log.error(error_message)
            return response[0]['id']
        else:
            log.error(error_message)
            raise VkontakteContentError(error_message)

    def prepare_create_params(self, **kwargs):
        return {
            'account_id': self.account.remote_id,
            'data': [self.fields_for_create()],
        }

    def prepare_update_params(self, **kwargs):
        return self.fields_for_update()

    def prepare_update_params_distinct(self, **kwargs):
        return {
            'account_id': self.account.remote_id,
            'data': [super(VkontakteAdsIDContentModel, self).prepare_update_params_distinct()],
        }

    def prepare_delete_params(self, **kwargs):
        return {
            'account_id': self.account.remote_id,
            'ids': [self.remote_id],
        }

    def save(self, *args, **kwargs):
        '''
        Update remote version of object before saving if data is different
        '''
        if not self.account:
            raise ValueError("You must specify ad campaign field")

        super(VkontakteAdsIDContentModel, self).save(*args, **kwargs)

#     def delete(self, commit_remote=True, *args, **kwargs):
#         # TODO: make possible to delete remotely queryset of instances Model.objects.all().delete()
#         # carefully fix tests to do not delete all campagins of client, line 150 and other
#         self.archive(commit_remote)
#         super(VkontakteAdsIDModel, self).delete(*args, **kwargs)
#
#     def archive(self, commit_remote=True):
#         '''
#         TODO: Response right, but remote objects still exists (deleting clients)
#         Archive or delete objects remotely and mark it archived localy
#         '''
#         if commit_remote and self.account and self.remote_id:
#             params = {
#                 'account_id': self.account.remote_id,
#                 'ids': [self.remote_id],
#             }
#             response = type(self).remote.api_call(method='delete', **params)
#             model = self._meta.object_name
#             if response != [0]:
#                 message = "Error response '%s' while deleting remote %s with ID %s" % (response, model, self.remote_id)
#                 log.error(message)
#                 raise VkontakteContentError(message)
#             log.info("Remote object %s with ID %s was deleted successfully" % (model, self.remote_id))
#
#         self.archived = True
#         self.save(commit_remote=False)

    def refresh(self, *args, **kwargs):
        kwargs['include_deleted'] = 1
        super(VkontakteAdsIDContentModel, self).refresh(*args, **kwargs)

    def check_remote_existance(self, *args, **kwargs):
        # if we found strange instances with small remote_id, archive them immediately
        if self.remote_id < 10000:
            self.archive(commit_remote=False)
            return False

        super(VkontakteAdsIDContentModel, self).check_remote_existance(*args, **kwargs)

class Account(VkontakteAdsIDModel):
    class Meta:
        verbose_name = u'Рекламный кабинет Вконтакте'
        verbose_name_plural = u'Рекламные кабинеты Вконтакте'
        ordering = ['remote_id']

    remote_pk_field = 'account_id'

    name = models.CharField(u'Название', blank=True, max_length=100)

    account_status = models.BooleanField(help_text=u'Cтатус рекламного кабинета. активен / неактивен.')
    access_role = models.CharField(choices=ACCOUNT_ACCESS_ROLE_CHOICES, max_length=10, help_text=u'права пользователя в рекламном кабинете.')

    remote = VkontakteManager(remote_pk=('remote_id',), methods={
        'get': 'getAccounts'
    })

    statistics = generic.GenericRelation('Statistic', verbose_name=u'Статистика')

    def __unicode__(self):
        return self.name or 'Account #%s' % self.remote_id

    def _substitute(self, old_instance):
        super(Account, self)._substitute(old_instance)
        self.name = old_instance.name

    def fetch_clients(self):
        '''
        Get all clients of account
        '''
        try:
            instances = Client.remote.get(account_id=self.remote_id)
        except VKError, e:
            if e.code == 100:
                return []
            else:
                raise e
        instances_saved = []

        for instance in instances:
            instance.account = self
            instance.fetched = datetime.now()
            instance._commit_remote = False
            instances_saved += [Client.remote.get_or_create_from_instance(instance)]

        return instances_saved

    def fetch_campaigns(self, ids=None):
        '''
        Get all campaigns of account
        '''
        return super(Account, self).fetch_campaigns(account=self, ids=ids)

    def fetch_budget(self):
        '''
        Get budget of account
        '''
        instance = Budget.remote.get(account_id=self.remote_id)
        instance.account = self
        instance = Budget.remote.get_or_create_from_instance(instance)
        return instance


class Client(VkontakteAdsIDContentModel):
    class Meta:
        verbose_name = u'Рекламный клиент Вконтакте'
        verbose_name_plural = u'Рекламные клиенты Вконтакте'

    account = models.ForeignKey(Account, verbose_name=u'Аккаунт', related_name='clients', help_text=u'Номер рекламного кабинета, в котором должны создаваться кампании.')

    name = models.CharField(u'Название', max_length=60)
    day_limit = models.IntegerField(u'Дневной лимит', null=True, help_text=u'Целое число рублей.')
    all_limit = models.IntegerField(u'Общий лимит', null=True, help_text=u'Целое число рублей.')

    statistics = generic.GenericRelation('Statistic', verbose_name=u'Статистика')

    objects = VkontakteCRUDManager()
    remote = VkontakteManager(
        remote_pk = ('remote_id',),
        methods = {
        'get':'getClients',
        'create': 'createClients',
        'update': 'updateClients',
        'delete': 'deleteClients',
    })

    def __unicode__(self):
        return self.name

    fields_required_for_update = ['client_id']

    def fields_for_update(self):
        fields = self.fields_for_create()
        fields.update(client_id = self.remote_id)
        return fields

    def fields_for_create(self):
        fields = dict(name = self.name)
        if self.day_limit:
            fields.update(day_limit = self.day_limit)
        if self.all_limit:
            fields.update(all_limit = self.all_limit)
        return fields

    def fetch_campaigns(self, ids=None):
        '''
        Get all campaigns of account
        '''
        return super(Client, self).fetch_campaigns(account=self.account, client=self, ids=ids)


class Campaign(VkontakteAdsIDContentModel):
    class Meta:
        verbose_name = u'Рекламная кампания Вконтакте'
        verbose_name_plural = u'Рекламные кампании Вконтакте'
        ordering = ['name']

    account = models.ForeignKey(Account, verbose_name=u'Аккаунт', related_name='campaigns', help_text=u'Номер рекламного кабинета, в котором должны создаваться кампании.')
    client = ChainedForeignKey(Client, verbose_name=u'Клиент', chained_field="account", chained_model_field="account", show_all=False, auto_choose=True, related_name='campaigns', null=True, blank=True, help_text=u'Только для рекламных агентств. id клиента, в рекламном кабинете которого будет создаваться кампания.')

    name = fields.CharRangeLengthField(u'Название', min_length=3, max_length=60, help_text=u'Название рекламной кампании - строка длиной от 3 до 60 символов.')
    day_limit = models.IntegerField(u'Дневной лимит', null=True, help_text=u'Целое число рублей.')
    all_limit = models.IntegerField(u'Общий лимит', null=True, help_text=u'Целое число рублей.')
    start_time = models.DateTimeField(u'Время запуска', null=True, blank=True, help_text=u'Время запуска кампании в unixtime формате.')
    stop_time = models.DateTimeField(u'Время остановки', null=True, blank=True, help_text=u'Время остановки кампании в unixtime формате.')
    status = models.BooleanField(u'Статус', help_text=u'Статус рекламной кампании: остановлена / запущена.')

    statistics = generic.GenericRelation('Statistic', verbose_name=u'Статистика')

    objects = VkontakteCRUDManager()
    remote = VkontakteManager(
        remote_pk = ('remote_id',),
        methods = {
        'get':'getCampaigns',
        'create': 'createCampaigns',
        'update': 'updateCampaigns',
        'delete': 'deleteCampaigns',
    })

    def _substitute(self, old_instance):
        super(Campaign, self)._substitute(old_instance)
        self.account = old_instance.account
        self.client = old_instance.client

    def refresh(self, *args, **kwargs):
        kwargs = {}
        kwargs['account_id'] = self.account.remote_id
        kwargs['campaign_ids'] = [self.remote_id]
        if self.client:
            kwargs['client_id'] = self.client.remote_id

        super(Campaign, self).refresh(*args, **kwargs)

    def check_remote_existance(self, *args, **kwargs):
        existance = super(Campaign, self).check_remote_existance(**kwargs)
        if not existance:
            for ad in self.ads.all():
                ad.archived = True
                ad.save(commit_remote=False)
        return existance

    fields_required_for_update = ['campaign_id']

    def fields_for_update(self):
        '''
        TODO: add dropping start_time, stop_time http://vk.com/developers.php?oid=-1&p=ads.updateCampaigns
        '''
        fields = self.fields_for_create()
        if 'client_id' in fields:
            fields.pop('client_id')
        fields.update(campaign_id = self.remote_id)
        return fields

    def fields_for_create(self):
        fields = dict(name = self.name, status = int(self.status))
        if self.client:
            fields.update(client_id = self.client.remote_id)
        if self.day_limit:
            fields.update(day_limit = self.day_limit)
        if self.all_limit:
            fields.update(all_limit = self.all_limit)
        if self.start_time:
            fields.update(start_time = int(time.mktime(self.start_time.timetuple())))
        if self.stop_time:
            fields.update(stop_time = int(time.mktime(self.stop_time.timetuple())))
        return fields

    def parse(self, response):
        # Convert status=2 to flag archived
        if response['status'] == 2:
            response['status'] = 0
            self.archived = True
        super(Campaign, self).parse(response)

    def fetch_ads(self, ids=None):
        '''
        Get all ads of campaign
        '''
        return super(Campaign, self).fetch_ads(model=Ad, ids=ids)

    def fetch_ads_targeting(self, ids=None):
        '''
        Get all ad targetings of campaign
        '''
        return super(Campaign, self).fetch_ads(model=Targeting, ids=ids)

    def fetch_ads_layout(self, ids=None):
        '''
        Get all ad layouts of campaign
        '''
        return super(Campaign, self).fetch_ads(model=Layout, ids=ids)


class AdAbstract(VkontakteAdsIDContentModel):
    '''
    Abstract model of vkontakte ads with all fields for some special needs
    '''
    class Meta:
        abstract = True

    account = models.ForeignKey(Account, verbose_name=u'Аккаунт', related_name='ads', help_text=u'Номер рекламного кабинета, в котором создается объявление.')
    campaign = ChainedForeignKey(Campaign, verbose_name=u'Кампания', chained_field="account", chained_model_field="account", show_all=False, auto_choose=True, related_name='ads', help_text=u'Кампания, в которой будет создаваться объявление.')

    # max_lengh=100 потому что иногда рекламы созданные через интерфейс ВК имеют названия длиннее
    name = fields.CharRangeLengthField(u'Название', min_length=3, max_length=100, help_text=u'Название объявления (для использования в рекламном кабинете) - строка длиной от 3 до 60 символов.')
    all_limit = models.PositiveIntegerField(u'Общий лимит', null=True, help_text=u'Целое число рублей.')
    cost_type = models.PositiveSmallIntegerField(u'Тип оплаты', choices=((0, u'оплата за переходы'), (1, u'оплата за показы')), help_text=u'Флаг, описывающий тип оплаты')
    cpc = fields.IntegerRangeField(u'Цена за переход', min_value=50, null=True, blank=True, help_text=u'Если оплата за переходы, цена за переход в копейках, минимум 50 коп.')
    cpm = models.PositiveIntegerField(u'Цена за показы', null=True, blank=True, help_text=u'Если оплата за показы, цена за 1000 показов в копейках')
    status = models.BooleanField(u'Статус', help_text=u'Статус рекламного объявления: остановлено / запущено.')
    disclaimer = models.BooleanField(u'Противопоказания', help_text=u'Укажите, если имеются противопоказания (только для рекламы медицинских товаров и услуг).')

    # not exist in API docs
    approved = models.BooleanField(u'Одобрено')

    statistics = generic.GenericRelation('Statistic', verbose_name=u'Статистика')

    objects = VkontakteCRUDManager()
    remote = VkontakteManager(
        remote_pk = ('remote_id',),
        methods = {
        'get':'getAds',
        'create': 'createAds',
        'update': 'updateAds',
        'delete': 'deleteAds',
    })


class Ad(AdAbstract):
    '''
    Model of vkontakte ads
    '''
    class Meta:
        verbose_name = u'Рекламное объявление Вконтакте'
        verbose_name_plural = u'Рекламные объявления Вконтакте'
        ordering = ['name']

    def __init__(self, *args, **kwargs):

        targeting_defaults = dict([(k.replace('targeting__', ''), kwargs.pop(k)) for k in kwargs.keys() if k[:11] == 'targeting__'])
        layout_defaults = dict([(k.replace('layout__', ''), kwargs.pop(k)) for k in kwargs.keys() if k[:8] == 'layout__'])
        image = kwargs.pop('image', None)

        super(Ad, self).__init__(*args, **kwargs)

        self._targeting = Targeting(ad=self, campaign_id=self.campaign_id, **targeting_defaults)
        self._layout = Layout(ad=self, campaign_id=self.campaign_id, ** layout_defaults)
        if image:
            self._image = image
            self._image.ad = self
        else:
            self._image = Image(ad=self)

    def _substitute(self, old_instance):
        super(Ad, self)._substitute(old_instance)
        self.account = old_instance.account
        self.campaign = old_instance.campaign
        self.layout = old_instance.layout
        self.targeting = old_instance.targeting
        self.image = old_instance.image

    def refresh(self, *args, **kwargs):
        kwargs = {}
        kwargs['ad_ids'] = [self.remote_id]
        kwargs['account_id'] = self.account.remote_id
        kwargs['campaign_ids'] = [self.campaign.remote_id]
        if self.campaign.client:
            kwargs['client_id'] = self.campaign.client.remote_id

        super(Ad, self).refresh(**kwargs)

    fields_required_for_update = ['ad_id']

    def fields_for_update(self):
        fields = self.fields_for_create()
        for field in ['campaign_id', 'cost_type']:
            if field in fields:
                fields.pop(field)
        fields.update(ad_id = int(self.remote_id))
        return fields

    def fields_for_create(self):
        fields = dict(
            campaign_id = int(self.campaign.remote_id),
            cost_type = self.cost_type,
            title = self.layout.title,
            link_url = self.layout.link_url,
            status = int(self.status)
        )
        if self.image:
            if not self.image.hash:
                self.image.upload()
            fields.update(
                hash = self.image.hash,
                photo_hash = self.image.photo_hash,
                photo = self.image.photo,
                server = self.image.server
            )

        if self.cost_type == 0:
            fields.update(cpc = float(self.cpc)/100 if self.cpc else 0)
        elif self.cost_type == 1:
            fields.update(cpm = float(self.cpm)/100 if self.cpm else 0)

        if self.name:
            fields.update(name = self.name)
        if self.all_limit:
            fields.update(all_limit = self.all_limit)
        if self.layout.description:
            fields.update(description = self.layout.description)
        if self.layout.link_domain:
            fields.update(link_domain = self.layout.link_domain)
#        TODO: оттестировать, потому что объявления с disclaimer==True он принудительно обновляет после каждого get запроса
#        if self.disclaimer:
#            fields.update(disclaimer = self.disclaimer)

        # targeting
        fields.update(
            sex = self.targeting.sex,
            age_from = self.targeting.age_from,
            age_to = self.targeting.age_to,
            country = self.targeting.country,
            school_from = self.targeting.school_from,
            school_to = self.targeting.school_to,
            uni_from = self.targeting.uni_from,
            uni_to = self.targeting.uni_to,
            travellers = int(self.targeting.travellers == 'on')
        )
        if self.targeting.tags:
            fields.update(tags = self.targeting.tags)
        if self.targeting.birthday:
            fields.update(birthday = self.targeting.birthday)
        for field in ['cities','cities_not','statuses','group_types','groups','districts',
            'stations','streets','schools','positions','religions','interests','browsers']:
                if getattr(self.targeting, field):
                    fields[field] = getattr(self.targeting, field)

        return fields

    def parse(self, response):
        # Convert status=2 to flag archived
        if response['status'] == 2:
            response['status'] = 0
            self.archived = True
        super(Ad, self).parse(response)

    def save(self, *args, **kwargs):

        try:
            self.account = self.campaign.account
        except ObjectDoesNotExist:
            pass

        if self.cost_type is None:
            if self.cpc is not None:
                self.cost_type = 0
            elif self.cpm is not None:
                self.cost_type = 1
            else:
                raise ValueError('Properties cost_type or cpc and cpm must be specified before saving')

        # if ad new get remote_id and save in local DB
        super(Ad, self).save(*args, **kwargs)

        # get linked objects and update it's fields or create new one
        try:
            self.targeting
        except:
            self._targeting.save()

        try:
            self.layout
        except:
            self._layout.save()

        try:
            self.image
        except:
            self._image.save()

class Targeting(VkontakteAdsMixin, VkontakteModel):

    class Meta:
        verbose_name = u'Таргетинг объявления Вконтакте'
        verbose_name_plural = u'Таргетинг объявления Вконтакте'
        ordering = ['ad']

    remote_pk_local_field = 'ad'

    ad = models.OneToOneField(Ad, verbose_name=u'Объявление', primary_key=True, related_name='targeting')

    campaign = models.ForeignKey(Campaign, verbose_name=u'Кампания')

    sex = models.PositiveSmallIntegerField(u'Пол', choices=TARGETING_SEX_CHOICES, default=0)
    age_from = models.PositiveSmallIntegerField(u'Возраст с', default=0)
    age_to = models.PositiveSmallIntegerField(u'Возраст до', default=0)
    birthday = models.CommaSeparatedIntegerField(u'День рождения', max_length=100, choices=[('',u'Неважно'),(1,u'Сегодня'),(2,u'Завтра'),(3,u'Сегодня или завтра')], blank=True)

    country = models.PositiveIntegerField(u'Страна', default=0)
    cities = models.CommaSeparatedIntegerField(u'Города', max_length=500, blank=True)
    cities_not = models.CommaSeparatedIntegerField(u'Города исключить', max_length=500, blank=True)
    statuses = models.CommaSeparatedIntegerField(u'Семейное положение', max_length=500, blank=True)

    group_types = models.CommaSeparatedIntegerField(u'Категории групп', max_length=500, blank=True)
    groups = models.CommaSeparatedIntegerField(u'Группы', max_length=500, blank=True)
    religions = models.CommaSeparatedIntegerField(u'Религиозные взгляды', max_length=500, blank=True)
    interests = fields.CommaSeparatedCharField(u'Интересы', max_length=500, blank=True, help_text=u'Последовательность слов, разделенных запятой.')
    travellers = models.BooleanField(u'Путешественники')

    # Расширенная география
    districts = models.CommaSeparatedIntegerField(u'Районы', max_length=500, blank=True)
    stations = models.CommaSeparatedIntegerField(u'Станции метро', max_length=500, blank=True)
    streets = models.CommaSeparatedIntegerField(u'Улицы', max_length=500, blank=True)

    # Образование и работа
    schools = models.CommaSeparatedIntegerField(u'Учебные заведения', max_length=500, blank=True)
    positions = models.CommaSeparatedIntegerField(u'Должности', max_length=500, blank=True)
    school_from = models.PositiveSmallIntegerField(u'Окончание школы после', default=0)
    school_to = models.PositiveSmallIntegerField(u'Окончание школы дое', default=0)
    uni_from = models.PositiveSmallIntegerField(u'Окончание ВУЗа после', default=0)
    uni_to = models.PositiveSmallIntegerField(u'Окончание ВУЗа до', default=0)

    # Дополнительные параметры
    browsers = models.CommaSeparatedIntegerField(u'Браузеры и устройства', max_length=500, blank=True)
    tags = fields.CommaSeparatedCharField(u'Ключевые слова', max_length=200, blank=True, help_text=u'Набор строк, разделенных запятой.')

    # not exist in API docs
    approved = models.BooleanField(u'Одобрено')
    count = models.PositiveIntegerField(null=True, blank=True, help_text=u'')
    operators = models.CommaSeparatedIntegerField(u'Операторы', max_length=500, blank=True, help_text=u'')

    remote = VkontakteManager(
        remote_pk = ('ad_id',),
        methods = {'get':'getAdsTargeting'}
    )


class Layout(VkontakteAdsMixin, VkontakteModel):
    class Meta:
        verbose_name = u'Контент объявления Вконтакте'
        verbose_name_plural = u'Контент объявления Вконтакте'
        ordering = ['ad']

    remote_pk_local_field = 'ad'

    ad = models.OneToOneField(Ad, verbose_name=u'Объявление', primary_key=True, related_name='layout')

    campaign = models.ForeignKey(Campaign, verbose_name=u'Кампания', help_text=u'Кампания объявления.')
    # change max_length=50, because found string with len=27
    title = fields.CharRangeLengthField(u'Заголовок', min_length=3, max_length=50, help_text=u'Заголовок объявления - строка длиной от 3 до 25 символов')
    # change max_length=100, because found string with len=65
    description = fields.CharRangeLengthField(u'Описание', min_length=3, max_length=100, help_text=u'Описание объявления - строка длиной от 3 до 60 символов - обязательно при выборе типа "оплата за переходы"')
    link_url = models.URLField(u'Ссылка', max_length=500, help_text=u'Ссылка на рекламируемый объект в формате http://yoursite.com или ВКонтакте API. Если в ссылке содержатся строки "{ad_id}" или "{campaign_id}", то они заменяются соответственно на ID объявления и ID кампании в момент перехода пользователя по такой ссылке.')
    link_domain = models.CharField(u'Домен', blank=True, max_length=50, help_text=u'Домен рекламируемого объекта в формате yoursite.com')

    # not exist in API docs
    preview_link = models.CharField(u'Превью', blank=True, max_length=200)

    # preview content
    preview = models.TextField()

    remote = VkontakteManager(
        remote_pk = ('ad_id',),
        methods = {'get':'getAdsLayout'}
    )

    def save(self, *args, **kwargs):
        self.set_preview()
        super(Layout, self).save(*args, **kwargs)

    def set_preview(self):
        if self.preview_link:
            response = requests.get(self.preview_link)
            # decode, becouse otherwise test would crash
            self.preview = response.content.decode('windows-1251', 'ignore')


class Image(VkontakteAdsMixin, VkontakteModel):
    '''
    Model of vkontakte image
    '''
    class Meta:
        verbose_name = u'Картинка объявления Вконтакте'
        verbose_name_plural = u'Картинка объявления Вконтакте'

    def _get_upload_to(self, filename=None):
        return 'images/%f.jpg' % time.time()

#    ad = models.OneToOneField(Ad, related_name='image')
    ad = models.OneToOneField(Ad, verbose_name=u'Объявление', primary_key=True, related_name='image')

    hash = models.CharField(max_length=50, blank=True, help_text=u'Значение, полученное в результате загрузки фотографии на сервер')
    photo_hash = models.CharField(max_length=50, blank=True, help_text=u'Значение, полученное в результате загрузки фотографии на сервер')
    photo = models.CharField(max_length=200, blank=True, help_text=u'Значение, полученное в результате загрузки фотографии на сервер')
    server = models.PositiveIntegerField(blank=True, null=True, help_text=u'Значение, полученное в результате загрузки фотографии на сервер')
    size = models.CharField(max_length=1, blank=True)
    aid = models.PositiveIntegerField(null=True, blank=True)
    width = models.PositiveIntegerField(null=True, blank=True)
    height = models.PositiveIntegerField(null=True, blank=True)

    file = models.ImageField(u'Картинка', upload_to=_get_upload_to, blank=True)

    # not in API
    post_url = models.CharField(max_length=200, blank=True, help_text=u'Адрес загрузки картинки на сервер')

    remote = VkontakteManager(methods = {'get_post_url':'getUploadURL'})

    def get_post_url(self):
        self.post_url = Image.remote.api_call(method='get_post_url', cost_type=self.ad.cost_type)
        return self.post_url

    def upload(self):
        if self.file:
            # save file to disk
            if not self.file._committed:
                self.file.field.pre_save(self, True)
            url = self.post_url or self.get_post_url()
            files = {'file': (self.file.name.split('/')[-1], open(os.path.join(settings.MEDIA_ROOT, self.file.name), 'rb'))}

            response = requests.post(url, files=files)
            response = json.loads(response.content)
            if 'errcode' in response:
                raise VkontakteContentError("Error with code %d while uploading image %s" % (response['errcode'], self.file))
            self.parse(response)


class VkontakteTargetingStatsManager(VkontakteManager):

    def api_call(self, method='get', **kwargs):

        ad = kwargs.pop('ad')
        kwargs['link_url'] = ad.layout.link_url
        kwargs['link_domain'] = ad.layout.link_domain
        kwargs['account_id'] = ad.account.remote_id

        if ad.remote_id:
            kwargs['ad_id'] = ad.remote_id
        else:
            kwargs['criteria'] = dict([(k,v) for k,v in ad.targeting.__dict__.items() if k[0] != '_'])
            for field_name in ['campaign_id','approved']:
                del kwargs['criteria'][field_name]

        return super(VkontakteTargetingStatsManager, self).api_call('get', **kwargs)

    def parse_response_list(self, response_list, extra_fields=None):
        return super(VkontakteTargetingStatsManager, self).parse_response_list([response_list], extra_fields)

    def fetch(self):
        raise Exception("Impossible to fetch targeting stats, use get() method")


class TargetingStats(VkontakteAdsModel):
    class Meta:
        verbose_name = u'Размер целевой аудитории Вконтакте'
        verbose_name_plural = u'Размеры целевой аудитории Вконтакте'

    audience_count = models.PositiveIntegerField(help_text=u'Размер целевой аудитории')
    recommended_cpc = models.FloatField(help_text=u'Рекомендованная цена для объявлений за клики, указана в рублях с копейкам в дробной части')
    recommended_cpm = models.FloatField(help_text=u'Рекомендованная цена для объявлений за показы, указана в рублях с копейкам в дробной части')

    remote = VkontakteTargetingStatsManager(methods={'get':'getTargetingStats'})

    def parse(self, response):
        '''
        Additionally convert values from rubles to kopeyki :)
        '''
        super(TargetingStats, self).parse(response)
        self.recommended_cpc *= 100
        self.recommended_cpm *= 100
        self.fetched = datetime.now()


class VkontakteStatisticManager(VkontakteManager):

    def _get_types(self):
        return (
            (ContentType.objects.get_for_model(Ad), 'ad'),
            (ContentType.objects.get_for_model(Campaign), 'campaign'),
            (ContentType.objects.get_for_model(Client), 'client'),
            (ContentType.objects.get_for_model(Account), 'office'),
        )

    def parse_response_list(self, response_list, extra_fields=None):
        '''
        Parse retrieved objects from remote server
        '''
        types = dict([(v,k) for k,v in self._get_types()])

        instances = []
        for resource in response_list:

            # in response with stats there is extra array inside each element
            if isinstance(resource, list) and len(resource):
                resource = resource[0]

            try:
                resource = dict(resource)
            except ValueError, e:
                log.error("Impossible to handle response of api call %s with parameters: %s" % (self.methods['get'], kwargs))
                raise e

            for stat in resource['stats']:
                instance = self.model()

                try:
                    instance.content_type = types[resource['type']]
                    model = instance.content_type.model_class()
                except KeyError:
                    raise ValueError("Could not find type of object for statistic %s" % resource['type'])

                try:
                    instance.object_id = model.objects.get(remote_id=resource['id']).pk
                except model.DoesNotExist:
                    raise ValueError("Could not find object %s for statistic with id %s" % (model, resource['id']))

                # important to do it before calling parse method
                if extra_fields:
                    instance.__dict__.update(extra_fields)

                instance.parse(stat)
                instances += [instance]

        return instances

    def fetch(self, objects, period='overall', date_from=0, date_to=0):
        '''
        Retrieve and save object to local DB
        '''
        if isinstance(objects, QuerySet):
            ids = [str(id) for id in objects.values_list('remote_id', flat=True)]
        elif isinstance(objects, (list, tuple)):
            ids = [str(campaign.remote_id) for campaign in objects]
        else:
            raise ValueError("Argument objects must be list or QuerySet")

        if not ids:
            return []

        if period not in ('day','month','overall'):
            raise ValueError("Period argument must be 'day','month' or 'overall'.")

        try:
            types = dict(self._get_types())
            ids_type = types[ContentType.objects.get_for_model(objects[0])]
            if ids_type == 'ad':
                account_id = objects[0].campaign.account.remote_id
            elif ids_type in ['campaign','client']:
                account_id = objects[0].account.remote_id
            elif ids_type == 'office' and len(objects) == 1:
                account_id = objects[0].remote_id
            else:
                raise ValueError("Could not define account_id for multiple objects %s" % objects)
        except KeyError:
            raise ValueError("Could not recognize ids_type for object %s" % objects[0])

        kwargs = {
            'account_id': account_id,
            'ids_type': ids_type,
            'ids': ','.join(ids),
            'period': period,
            'date_from': date_from,
            'date_to': date_to,
        }

        instances = super(VkontakteStatisticManager, self).fetch(**kwargs)
        return instances

    def fetch_for_all_campaigns(self, **kwargs):
        stats = []
        for account in Account.objects.all():
            stats += self.fetch(account.campaigns.all(), **kwargs)
        return stats

    def fetch_for_all_ads(self, **kwargs):
        stats = []
        for account in Account.objects.all():
            stats += self.fetch(Ad.objects.filter(campaign__account=account), **kwargs)
        return stats

    def fetch_for_all_clients(self, **kwargs):
        stats = []
        for account in Account.objects.all():
            stats += self.fetch(account.clients.all(), **kwargs)
        return stats

    def fetch_for_all_accounts(self, **kwargs):
        stats = []
        for account in Account.objects.all():
            stats += self.fetch([account], **kwargs)
        return stats


class StatisticAbstract(VkontakteAdsModel):
    '''
    Abstract model of vkontakte statistic with stat fields for some special needs
    '''
    class Meta:
        abstract = True

    clicks = models.PositiveIntegerField(u'Клики', default=0)
    impressions = models.PositiveIntegerField(u'Просмотры', default=0)
    reach = models.PositiveIntegerField(u'Охват', default=0)
    spent = models.FloatField(u'Потраченные средства', default=0)
    video_views = models.PositiveIntegerField(u'Просмотры видеозаписи (для видеорекламы)', null=True)
    join_rate = models.FloatField(null=True, help_text=u'Вступления в группу, событие, подписки на публичную страницу или установки приложения (только если в объявлении указана прямая ссылка на соответствующую страницу ВКонтакте)')

#    account = models.ForeignKey(Account, help_text=u'Номер рекламного кабинета, в котором запрашивается статистика.')
#    ad = models.ForeignKey(Ad, help_text=u'Рекламное объявление, для которого запрашивается статистика.')
#    campaign = models.ForeignKey(Campaign, help_text=u'Кампания, для которой запрашивается статистика.')
#    client = models.ForeignKey(Client, help_text=u'Клиент, для которого запрашивается статистика.')

#    ids_type = models.CharField(max_length=15, choices=STATISTIC_TYPE_CHOICES, help_text=u'Тип запрашиваемых объектов, которые перечислены в параметре ids')
#    ids = models.TextField(help_text=u'Перечисленные через запятую id запрашиваемых объявлений, кампаний, клиентов или кабинетов, в зависимости от того, что указано в параметре ids_type. Максимум 2000 объектов.')
#    date_from = models.DateTimeField(help_text=u'Начальная дата выводимой статистики.')
#    date_to = models.DateTimeField(help_text=u'Конечная дата выводимой статистики.')
#    period = models.CharField(max_length=15, choices=STATISTIC_PERIOD_CHOICES, help_text=u'Способ группировки данных по датам')

    # auto-estimated values
    ctr = models.FloatField(null=True)
    cpc = models.FloatField(null=True)
    cpm = models.FloatField(null=True)

    def set_auto_values(self):
        # estimate auto values
        if not self.ctr:
            self.ctr = float('%.3f' % (100*float(self.clicks)/self.impressions)) if self.impressions else None
        if not self.cpc:
            self.cpc = float('%.2f' % (self.spent/self.clicks)) if self.clicks else None
        if not self.cpm:
            self.cpm = float('%.2f' % (100*self.spent/self.impressions)) if self.impressions else None

    def save(self, *args, **kwargs):
        self.set_auto_values()
        return super(StatisticAbstract, self).save(*args, **kwargs)


class Statistic(StatisticAbstract):
    class Meta:
        verbose_name = u'Рекламная статистика Вконтакте'
        verbose_name_plural = u'Рекламная статистика Вконтакте'
        unique_together = ('content_type','object_id','day','month','overall')

    content_type = models.ForeignKey(ContentType, limit_choices_to=(models.Q(app_label='vkontakte_ads', model='account') | models.Q(app_label='vkontakte_ads', model='campaign') | models.Q(app_label='vkontakte_ads', model='ad') | models.Q(app_label='vkontakte_ads', model='client')))
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey()

    day = models.DateField(u'День', null=True)
    month = models.CharField(u'Месяц', max_length=7)
    overall = models.BooleanField(u'За все время?')

    objects = models.Manager() # because we need it as a default manager for relations
    remote = VkontakteStatisticManager(remote_pk=('content_type','object_id','day','month','overall'), methods={'get':'getStatistics'})


class Budget(VkontakteAdsModel):
    class Meta:
        verbose_name = u'Бюджет личного кабинета Вконтакте'
        verbose_name_plural = u'Бюджеты личных кабинетов Вконтакте'

    account = models.ForeignKey(Account, primary_key=True, help_text=u'Номер рекламного кабинета, бюджет которого запрашивается.')
    budget = models.DecimalField(max_digits=10, decimal_places=2, help_text=u'Оставшийся бюджет в указанном рекламном кабинете.')

    remote = VkontakteManager(remote_pk=('account',), methods={'get':'getBudget'})


# Проще работать без модели см. lookups.py
#SUGGESTION_SECTION_CHOICES = (
#    'countries', 'запрос списка стран. Если q не задана или пуста, выводится краткий список стран. Иначе выводится полный список стран.',
#    'regions', 'запрос списка регионов. Обязательно присутствие параметра country.',
#    'cities', 'запрос списка городов. Обязательно присутствие параметра country.',
#    'districts', 'запрос списка районов. Обязательно присутствие параметра cities.',
#    'stations', 'запрос списка станций метро. Обязательно присутствие параметра cities.',
#    'streets', 'запрос списка улиц. Обязательно присутствие параметра cities.',
#    'schools', 'запрос списка учебных заведений. Обязательно присутствие параметра cities.',
#    'interests', 'запрос списка интересов.',
#    'positions', 'запрос списка должностей (профессий).',
#    'group_types', 'запрос списка типов групп.',
#    'religions', 'запрос списка религиозных взглядов.',
#    'browsers', 'запрос списка браузеров и мобильных устройств.',
#)
#
#class Suggestion(VkontakteModel):
#    class Meta:
#        abstract = True
#        verbose_name = _('Vkontakte ad suggestion')
#        verbose_name_plural = _('Vkontakte ad suggestions')
#
#    section = models.CharField(choices=SUGGESTION_SECTION_CHOICES, help_text=u'Раздел, в котором заправшиваются подсказки.')
#    q = models.CharField(help_text=u'Строка-фильтр запроса (для countries, regions, cities, streets, schools, interests, positions).')
#    country = models.PositiveIntegerField(help_text=u'id страны, в которой ищутся объекты (для regions и cities)')
#    cities = models.CommaSeparatedIntegerField(help_text=u'Разделенные запятыми id городов, в которых ищутся объекты.')
#
#    remote = VkontakteManager(methods={'get':'getSuggestions'})
#

import signals
