# -*- coding: utf-8 -*-
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.contrib.contenttypes import generic
from django.conf.urls.defaults import patterns, url
from django.conf import settings
from django import forms
from models import Account, Campaign, Ad, Targeting, Client, Layout, Statistic, Image, TARGETING_STATUS_CHOICES
from vkontakte_api.models import VkontakteContentError
from vkontakte_api.widgets import AdminImageWidget
from vkontakte_api.admin import VkontakteModelAdmin
from ajax_select.admin import AjaxSelectAdmin
from ajax_select.fields import AutoCompleteSelectMultipleWidget, AutoCompleteSelectWidget
from utils.widgets import LinkFieldWidget
from views import targeting_stats

YEAR_CHOICES = [(0, u'Любой')] + [(year, u'c %d' % year) for year in range(2017, 1954, -1)]
AGE_FROM_CHOICES = [(0, u'Любой')] + [(age, u'c %d' % age) for age in range(12, 81)]
AGE_TO_CHOICES = [(0, u'Любой')] + [(age, u'до %d' % age) for age in range(23, 81)]

def campaign_link(obj):
    return u'<a href="%s">%s</a>' % (reverse('admin:vkontakte_ads_campaign_change', args=(obj.pk,)), obj)
campaign_link.short_description = u'Кампания'
campaign_link.allow_tags = True

def ad_link(obj):
    return u'<a href="%s">%s</a>' % (reverse('admin:vkontakte_ads_ad_change', args=(obj.pk,)), obj)
ad_link.short_description = 'Объявление'
ad_link.allow_tags = True

def related_campaign_link(obj):
    return u'<a href="%s">%s</a>' % (reverse('admin:vkontakte_ads_campaign_change', args=(obj.campaign.pk,)), obj.campaign)
related_campaign_link.short_description = u'Кампания'
related_campaign_link.allow_tags = True

def related_account_link(obj):
    return u'<a href="%s">%s</a>' % (reverse('admin:vkontakte_ads_account_change', args=(obj.account.pk,)), obj.account)
related_account_link.short_description = u'Кабинет'
related_account_link.allow_tags = True

class VkontakteAdsMixin(object):
    class Media:
        js = (
            settings.STATIC_URL + "vkontakte_ads/js/admin.js",
        )

class StatisticInline(generic.GenericTabularInline):
    model = Statistic
    fields = (
        'day','month','overall',
        'impressions','clicks','spent','video_views','join_rate',
    )
    readonly_fields = fields
    extra = 0
    max_num = 0
    can_delete = False

class AdsInline(admin.TabularInline):
    model = Ad
    fields = (ad_link,'cost_type','status')
    readonly_fields = fields
    extra = 0
    max_num = 0
    can_delete = False

class CampaignsInline(admin.TabularInline):
    model = Campaign
    fields = (campaign_link,'status','day_limit','all_limit')
    readonly_fields = fields
    extra = 0
    max_num = 0
    can_delete = False

class TargetingForm(forms.ModelForm):
    class Meta:
        model = Targeting
    def __init__(self, *args, **kwargs):
        super(TargetingForm, self).__init__(*args, **kwargs)
        self.fields['cities'].widget = AutoCompleteSelectMultipleWidget('vk_places_city')
        self.fields['cities_not'].widget = AutoCompleteSelectMultipleWidget('vk_places_city')
        self.fields['country'].widget = AutoCompleteSelectWidget('vk_places_country')

        self.fields['groups'].widget = AutoCompleteSelectMultipleWidget('vk_groups')

        self.fields['religions'].widget = AutoCompleteSelectMultipleWidget('vk_ads_religions')
        self.fields['interests'].widget = AutoCompleteSelectMultipleWidget('vk_ads_interests')
        self.fields['positions'].widget = AutoCompleteSelectMultipleWidget('vk_ads_positions')
        self.fields['browsers'].widget = AutoCompleteSelectMultipleWidget('vk_ads_browsers')
        self.fields['group_types'].widget = AutoCompleteSelectMultipleWidget('vk_ads_group_types')
        self.fields['districts'].widget = AutoCompleteSelectMultipleWidget('vk_ads_districts')
#        self.fields['streets'].widget = AutoCompleteSelectMultipleWidget('vk_ads_streets')
        self.fields['schools'].widget = AutoCompleteSelectMultipleWidget('vk_ads_schools')

        self.fields['age_from'].widget = forms.Select(choices=AGE_FROM_CHOICES)
        self.fields['age_to'].widget = forms.Select(choices=AGE_TO_CHOICES)

        self.fields['school_from'].widget = forms.Select(choices=YEAR_CHOICES)
        self.fields['school_to'].widget = forms.Select(choices=YEAR_CHOICES)
        self.fields['uni_from'].widget = forms.Select(choices=YEAR_CHOICES)
        self.fields['uni_to'].widget = forms.Select(choices=YEAR_CHOICES)

        self.fields['statuses'].widget = forms.SelectMultiple(choices=TARGETING_STATUS_CHOICES)
        self.fields['birthday'].widget = forms.Select(choices=Targeting._meta.get_field('birthday').choices)

class AdForm(forms.ModelForm):
    class Meta:
        model = Ad
    def __init__(self, *args, **kwargs):
        super(AdForm, self).__init__(*args, **kwargs)

#    def clean(self, *args, **kwargs):
#        '''
#        Add Layout, Targeting and Image data to Ad instance for generating correct upload API call to VK
#        Save instance in clean() method instead of save() for showing validation error, caused by remote VK side
#        '''
#        for relation_name in ['layout','targeting','image']:
#            relation_data = {}
#            for form_field in ['data','files']:
#                relation_field = '%s-0-' % relation_name
#                relation_field_len = len(relation_field)
#                values = dict([(k.replace(relation_field, ''), getattr(self, form_field)[k]) for k in getattr(self, form_field).keys() if k[:relation_field_len] == relation_field])
#                relation_data.update(values)
#
#            if self.instance.pk is None:
#                del relation_data['id']
#
#            getattr(self.instance, relation_name).__dict__.update(relation_data)
#
#        try:
#            return super(AdForm, self).save(*args, **kwargs)
#        except VkontakteContentError, e:
#            raise forms.ValidationError(e)

    def save(self, *args, **kwargs):
        '''
        Add Layout, Targeting and Image data to Ad instance for generating correct upload API call to VK
        '''
        for relation_name in ['layout','targeting','image']:
            relation_data = {}
            for form_field in ['data','files']:
                relation_field = '%s-0-' % relation_name
                relation_field_len = len(relation_field)
                values = dict([(k.replace(relation_field, ''), getattr(self, form_field)[k]) for k in getattr(self, form_field).keys() if k[:relation_field_len] == relation_field])
                relation_data.update(values)

            if self.instance.pk is None and 'id' in relation_data:
                del relation_data['id']

            getattr(self.instance, relation_name).__dict__.update(relation_data)

        return super(AdForm, self).save(*args, **kwargs)

class LayoutForm(forms.ModelForm):
    class Meta:
        model = Layout
    def __init__(self, *args, **kwargs):
        super(LayoutForm, self).__init__(*args, **kwargs)
        self.fields['preview_link'].widget = LinkFieldWidget(text='Preview')
        self.fields['link_domain'].widget = LinkFieldWidget(text='Domain', url='http://%s')
        self.fields['link_url'].widget = LinkFieldWidget(text='Url')
        self.fields['description'].widget = forms.TextInput(attrs={'size':'100'})

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
    def __init__(self, *args, **kwargs):
        super(ImageForm, self).__init__(*args, **kwargs)
        self.fields['file'].widget = AdminImageWidget()

class ImageInline(admin.StackedInline):
    model = Image
    form = ImageForm
    readonly_fields = ('hash','photo','server','size','aid','width','height','post_url')
    fieldsets = (
        (None, {
            'fields': ('file','width','height')
        }),
        (u'Технические характеристики', {
            'classes': ('collapse',),
            'fields': ('hash','photo','server','size','aid','post_url')
        }),
    )

    def get_formset(self, request, obj=None, **kwargs):
        '''
        Make 'file' required for new ad, and not for existing
        '''
        formset = super(ImageInline, self).get_formset(request, obj=None, **kwargs)
        formset.form.base_fields['file'].required = not obj
        return formset

class LayoutInline(admin.StackedInline):
    model = Layout
    form = LayoutForm
    fields = ('title','description','link_url','link_domain','preview_link')
    readonly_fields = ('fetched',)

class TargetingInline(admin.StackedInline):
    model = Targeting
    form = TargetingForm
    exclude = ('campaign',)
    readonly_fields = ('approved','count','fetched')
    fieldsets = (
        (u'География', {
            'fields': ('country','cities','cities_not'),
        }),
        (u'Демография', {
            'fields': ('sex','age_from','age_to','birthday','statuses'),
        }),
        (u'Интересы', {
            'classes': ('collapse',),
            'fields': ('group_types','groups','religions','interests','travellers'),
        }),
        (u'Расширенная география', {
            'classes': ('collapse',),
            'fields': ('districts','stations','streets'),
        }),
        (u'Образование и работа', {
            'classes': ('collapse',),
            'fields': ('schools','positions','school_from','school_to','uni_from','uni_to'),
        }),
        (u'Дополнительные параметры', {
            'classes': ('collapse',),
            'fields': ('browsers','tags'),
        }),
    )

class CrudVkontakteAdmin(admin.ModelAdmin):
    readonly_fields = ('remote_id','fetched')

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('account',) + self.readonly_fields
        return self.readonly_fields

class AccountAdmin(CrudVkontakteAdmin, VkontakteAdsMixin):
    inlines = [CampaignsInline, StatisticInline]#, AccountReportInline]

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields
        return ('fetched',)

class CampaignAdmin(CrudVkontakteAdmin, VkontakteAdsMixin):
    list_display = ('name','status','archived','day_limit','all_limit')
    list_filter = ('status','archived','account',)
    inlines = [AdsInline, StatisticInline]#, CampaignStatInline, CampaignReportInline]

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super(CampaignAdmin, self).get_readonly_fields(request, obj)
        readonly_fields += ('archived',)
        if obj:
            return ('client',) + readonly_fields
        return readonly_fields

class AdAdmin(CrudVkontakteAdmin, VkontakteAdsMixin):
    list_display = ('name','status','archived',related_campaign_link,'cpc','cpm')
    list_filter = ('status','archived','cost_type','disclaimer','account','campaign',)
    search_fields = ('name','layout__title','layout__description',)
    form = AdForm
    inlines = [ImageInline, LayoutInline, TargetingInline, StatisticInline]

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super(AdAdmin, self).get_readonly_fields(request, obj)
        readonly_fields += ('approved','archived',)
        if obj:
            return ('campaign',) + readonly_fields
        return readonly_fields

    def save_formset(self, request, form, formset, change):
        if change:
            super(AdAdmin, self).save_formset(request, form, formset, change)

    def get_urls(self):
        urls = super(AdAdmin, self).get_urls()
        urls_new = patterns('', url(r'^(.+)/targeting_stats/$', targeting_stats, name='vkontakte_ads_ad_targeting_stats'))
        return urls_new + urls

class ClientAdmin(CrudVkontakteAdmin, VkontakteAdsMixin):
    list_display = ('name',related_account_link,'day_limit','all_limit')
    list_filter = ('account',)
    inlines = [CampaignsInline, StatisticInline]


class StatisticAdmin(VkontakteModelAdmin):
    list_display = (
        'day','month','overall',
        'content_object',
        'impressions','clicks','spent','video_views','join_rate','reach','ctr','cpc','cpm',
    )
    list_filter = ('day','month','overall','content_type')
    list_display_links = ('content_object',)

class TargetingAdmin(AjaxSelectAdmin):
    form = TargetingForm

admin.site.register(Account, AccountAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Campaign, CampaignAdmin)
admin.site.register(Ad, AdAdmin)
admin.site.register(Statistic, StatisticAdmin)