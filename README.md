Django Vkontakte Ads [![Build Status](https://travis-ci.org/ramusus/django-vkontakte-ads.png?branch=master)](https://travis-ci.org/ramusus/django-vkontakte-ads)
====================

Приложение позволяет взаимодействовать с рекламными объектами Вконтакте через Вконтакте API Ads используя стандартные модели Django

Установка
---------

    pip install django-vkontakte-api

В `settings.py` необходимо добавить:

    INSTALLED_APPS = (
        ...
        'oauth_tokens',
        'vkontakte_api',
        'vkontakte_ads',
    )

    # oauth-tokens settings
    OAUTH_TOKENS_HISTORY = True                                         # to keep in DB expired access tokens
    OAUTH_TOKENS_VKONTAKTE_CLIENT_ID = ''                               # application ID
    OAUTH_TOKENS_VKONTAKTE_CLIENT_SECRET = ''                           # application secret key
    OAUTH_TOKENS_VKONTAKTE_SCOPE = ['ads,wall,photos,friends,stats']    # application scopes
    OAUTH_TOKENS_VKONTAKTE_USERNAME = ''                                # user login
    OAUTH_TOKENS_VKONTAKTE_PASSWORD = ''                                # user password
    OAUTH_TOKENS_VKONTAKTE_PHONE_END = ''                               # last 4 digits of user mobile phone

Покрытие методов API
--------------------

* [ads.getAccounts](http://vk.com/developers.php?oid=-1&p=ads.getAccounts) — получение списка рекламных кабинетов.
* [ads.getClients](http://vk.com/developers.php?oid=-1&p=ads.getClients) — получение списка клиентов рекламного агентства.
* [ads.createClients](http://vk.com/developers.php?oid=-1&p=ads.createClients) — создание клиентов рекламного агентства.
* [ads.updateClients](http://vk.com/developers.php?oid=-1&p=ads.updateClients) — редактирование клиентов рекламного агентства.
* [ads.deleteClients](http://vk.com/developers.php?oid=-1&p=ads.deleteClients) — архивирование (удаление) клиентов рекламного агентства.
* [ads.getCampaigns](http://vk.com/developers.php?oid=-1&p=ads.getCampaigns) — получение списка рекламных кампаний.
* [ads.createCampaigns](http://vk.com/developers.php?oid=-1&p=ads.createCampaigns) — создание рекламных кампаний.
* [ads.updateCampaigns](http://vk.com/developers.php?oid=-1&p=ads.updateCampaigns) — редактирование рекламных кампаний.
* [ads.deleteCampaigns](http://vk.com/developers.php?oid=-1&p=ads.deleteCampaigns) — архивирование (удаление) рекламных кампаний.
* [ads.getAds](http://vk.com/developers.php?oid=-1&p=ads.getAds) — получение списка рекламных объявлений.
* [ads.getAdsLayout](http://vk.com/developers.php?oid=-1&p=ads.getAdsLayout) — получение внешнего вида объявлений.
* [ads.getAdsTargeting](http://vk.com/developers.php?oid=-1&p=ads.getAdsTargeting) — получение параметров таргетинга объявлений.
* [ads.createAds](http://vk.com/developers.php?oid=-1&p=ads.createAds) — создание рекламных объявлений.
* [ads.updateAds](http://vk.com/developers.php?oid=-1&p=ads.updateAds) — редактирование рекламных объявлений.
* [ads.deleteAds](http://vk.com/developers.php?oid=-1&p=ads.deleteAds) — архивирование (удаление) рекламных объявлений.
* [ads.getStatistics](http://vk.com/developers.php?oid=-1&p=ads.getStatistics) — получение статистики показателей эффективности.
* [ads.getBudget](http://vk.com/developers.php?oid=-1&p=ads.getBudget) — получение оставшегося бюджета рекламного кабинета.
* [ads.getTargetingStats](http://vk.com/developers.php?oid=-1&p=ads.getTargetingStats) — получение характеристик таргетинга.
* [ads.getSuggestions](http://vk.com/developers.php?oid=-1&p=ads.getSuggestions) — получение подсказок автодополнения.
* [ads.getUploadURL](http://vk.com/developers.php?oid=-1&p=ads.getUploadURL) — получение URL-адреса для загрузки фотографии объявления.

В планах:

* [ads.getDemographics](http://vk.com/developers.php?oid=-1&p=ads.getDemographics) — получение демографической статистики;
* [ads.getOfficeUsers](http://vk.com/developers.php?oid=-1&p=ads.getOfficeUsers) — получение наблюдателей и администраторов рекламного кабинета;
* [ads.addOfficeUsers](http://vk.com/developers.php?oid=-1&p=ads.addOfficeUsers) — добавление наблюдателей и администраторов рекламного кабинета;
* [ads.removeOfficeUsers](http://vk.com/developers.php?oid=-1&p=ads.removeOfficeUsers) — удаление наблюдателей и администраторов рекламного кабинета;
* [ads.getVideoUploadURL](http://vk.com/developers.php?oid=-1&p=ads.getVideoUploadURL) — получение URL-адреса для загрузки видеозаписи объявления;
* [ads.getFloodStats](http://vk.com/developers.php?oid=-1&p=ads.getFloodStats) — получение остатка количества разрешенных операций над рекламным кабинетом;
* [ads.getRejectionReason](http://vk.com/developers.php?oid=-1&p=ads.getRejectionReason) — получение информации о причине отклонения объявления;
* [ads.createTargetGroup](http://vk.com/developers.php?oid=-1&p=ads.createTargetGroup) — создание группы ретаргетинга;
* [ads.updateTargetGroup](http://vk.com/developers.php?oid=-1&p=ads.updateTargetGroup) — редактирование группы ретаргетинга;
* [ads.deleteTargetGroup](http://vk.com/developers.php?oid=-1&p=ads.deleteTargetGroup) — удаление группы ретаргетинга;
* [ads.getTargetGroups](http://vk.com/developers.php?oid=-1&p=ads.getTargetGroups) — получение списка групп ретаргетинга;
* [ads.importTargetContacts](http://vk.com/developers.php?oid=-1&p=ads.importTargetContacts) — импорт списка контактов в группу ретаргетинга;