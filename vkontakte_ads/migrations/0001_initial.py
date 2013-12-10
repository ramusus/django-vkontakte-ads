# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Account'
        db.create_table(u'vkontakte_ads_account', (
            ('fetched', self.gf('django.db.models.fields.DateTimeField')(db_index=True, null=True, blank=True)),
            ('remote_id', self.gf('django.db.models.fields.BigIntegerField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('account_status', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('access_role', self.gf('django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal(u'vkontakte_ads', ['Account'])

        # Adding model 'Client'
        db.create_table(u'vkontakte_ads_client', (
            ('fetched', self.gf('django.db.models.fields.DateTimeField')(db_index=True, null=True, blank=True)),
            ('remote_id', self.gf('django.db.models.fields.BigIntegerField')(primary_key=True)),
            ('archived', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('account', self.gf('django.db.models.fields.related.ForeignKey')(related_name='clients', to=orm['vkontakte_ads.Account'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('day_limit', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('all_limit', self.gf('django.db.models.fields.IntegerField')(null=True)),
        ))
        db.send_create_signal(u'vkontakte_ads', ['Client'])

        # Adding model 'Campaign'
        db.create_table(u'vkontakte_ads_campaign', (
            ('fetched', self.gf('django.db.models.fields.DateTimeField')(db_index=True, null=True, blank=True)),
            ('remote_id', self.gf('django.db.models.fields.BigIntegerField')(primary_key=True)),
            ('archived', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('account', self.gf('django.db.models.fields.related.ForeignKey')(related_name='campaigns', to=orm['vkontakte_ads.Account'])),
            ('client', self.gf('smart_selects.db_fields.ChainedForeignKey')(blank=True, related_name='campaigns', null=True, to=orm['vkontakte_ads.Client'])),
            ('name', self.gf('vkontakte_api.fields.CharRangeLengthField')(max_length=60)),
            ('day_limit', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('all_limit', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('start_time', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('stop_time', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'vkontakte_ads', ['Campaign'])

        # Adding model 'Ad'
        db.create_table(u'vkontakte_ads_ad', (
            ('fetched', self.gf('django.db.models.fields.DateTimeField')(db_index=True, null=True, blank=True)),
            ('remote_id', self.gf('django.db.models.fields.BigIntegerField')(primary_key=True)),
            ('archived', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('account', self.gf('django.db.models.fields.related.ForeignKey')(related_name='bulk_ads', to=orm['vkontakte_ads.Account'])),
            ('campaign', self.gf('smart_selects.db_fields.ChainedForeignKey')(related_name='bulk_ads', to=orm['vkontakte_ads.Campaign'])),
            ('name', self.gf('vkontakte_api.fields.CharRangeLengthField')(max_length=100)),
            ('all_limit', self.gf('django.db.models.fields.PositiveIntegerField')(null=True)),
            ('cost_type', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('cpc', self.gf('vkontakte_api.fields.IntegerRangeField')(null=True, blank=True)),
            ('cpm', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('disclaimer', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('approved', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'vkontakte_ads', ['Ad'])

        # Adding model 'Targeting'
        db.create_table(u'vkontakte_ads_targeting', (
            ('fetched', self.gf('django.db.models.fields.DateTimeField')(db_index=True, null=True, blank=True)),
            ('ad', self.gf('django.db.models.fields.related.OneToOneField')(related_name='targeting', unique=True, primary_key=True, to=orm['vkontakte_ads.Ad'])),
            ('campaign', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['vkontakte_ads.Campaign'])),
            ('sex', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('age_from', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('age_to', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('birthday', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=100, blank=True)),
            ('country', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('cities', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=500, blank=True)),
            ('cities_not', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=500, blank=True)),
            ('statuses', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=500, blank=True)),
            ('group_types', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=500, blank=True)),
            ('groups', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=500, blank=True)),
            ('religions', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=500, blank=True)),
            ('interests', self.gf('vkontakte_api.fields.CommaSeparatedCharField')(max_length=500, blank=True)),
            ('travellers', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('districts', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=500, blank=True)),
            ('stations', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=500, blank=True)),
            ('streets', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=500, blank=True)),
            ('schools', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=500, blank=True)),
            ('positions', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=500, blank=True)),
            ('school_from', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('school_to', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('uni_from', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('uni_to', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('browsers', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=500, blank=True)),
            ('tags', self.gf('vkontakte_api.fields.CommaSeparatedCharField')(max_length=200, blank=True)),
            ('approved', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('count', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('operators', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=500, blank=True)),
        ))
        db.send_create_signal(u'vkontakte_ads', ['Targeting'])

        # Adding model 'Layout'
        db.create_table(u'vkontakte_ads_layout', (
            ('fetched', self.gf('django.db.models.fields.DateTimeField')(db_index=True, null=True, blank=True)),
            ('ad', self.gf('django.db.models.fields.related.OneToOneField')(related_name='layout', unique=True, primary_key=True, to=orm['vkontakte_ads.Ad'])),
            ('campaign', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['vkontakte_ads.Campaign'])),
            ('title', self.gf('vkontakte_api.fields.CharRangeLengthField')(max_length=50)),
            ('description', self.gf('vkontakte_api.fields.CharRangeLengthField')(max_length=100)),
            ('link_url', self.gf('django.db.models.fields.URLField')(max_length=500)),
            ('link_domain', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('preview_link', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('preview', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'vkontakte_ads', ['Layout'])

        # Adding model 'Image'
        db.create_table(u'vkontakte_ads_image', (
            ('fetched', self.gf('django.db.models.fields.DateTimeField')(db_index=True, null=True, blank=True)),
            ('ad', self.gf('django.db.models.fields.related.OneToOneField')(related_name='image', unique=True, primary_key=True, to=orm['vkontakte_ads.Ad'])),
            ('hash', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('photo_hash', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('photo', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('server', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('size', self.gf('django.db.models.fields.CharField')(max_length=1, blank=True)),
            ('aid', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('width', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('height', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('file', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('post_url', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
        ))
        db.send_create_signal(u'vkontakte_ads', ['Image'])

        # Adding model 'TargetingStats'
        db.create_table(u'vkontakte_ads_targetingstats', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('fetched', self.gf('django.db.models.fields.DateTimeField')(db_index=True, null=True, blank=True)),
            ('audience_count', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('recommended_cpc', self.gf('django.db.models.fields.FloatField')()),
            ('recommended_cpm', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal(u'vkontakte_ads', ['TargetingStats'])

        # Adding model 'Statistic'
        db.create_table(u'vkontakte_ads_statistic', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('fetched', self.gf('django.db.models.fields.DateTimeField')(db_index=True, null=True, blank=True)),
            ('clicks', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('impressions', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('reach', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('spent', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('video_views', self.gf('django.db.models.fields.PositiveIntegerField')(null=True)),
            ('join_rate', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('ctr', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('cpc', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('cpm', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('day', self.gf('django.db.models.fields.DateField')(null=True)),
            ('month', self.gf('django.db.models.fields.CharField')(max_length=7)),
            ('overall', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'vkontakte_ads', ['Statistic'])

        # Adding unique constraint on 'Statistic', fields ['content_type', 'object_id', 'day', 'month', 'overall']
        db.create_unique(u'vkontakte_ads_statistic', ['content_type_id', 'object_id', 'day', 'month', 'overall'])

        # Adding model 'Budget'
        db.create_table(u'vkontakte_ads_budget', (
            ('fetched', self.gf('django.db.models.fields.DateTimeField')(db_index=True, null=True, blank=True)),
            ('account', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['vkontakte_ads.Account'], primary_key=True)),
            ('budget', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2)),
        ))
        db.send_create_signal(u'vkontakte_ads', ['Budget'])


    def backwards(self, orm):
        # Removing unique constraint on 'Statistic', fields ['content_type', 'object_id', 'day', 'month', 'overall']
        db.delete_unique(u'vkontakte_ads_statistic', ['content_type_id', 'object_id', 'day', 'month', 'overall'])

        # Deleting model 'Account'
        db.delete_table(u'vkontakte_ads_account')

        # Deleting model 'Client'
        db.delete_table(u'vkontakte_ads_client')

        # Deleting model 'Campaign'
        db.delete_table(u'vkontakte_ads_campaign')

        # Deleting model 'Ad'
        db.delete_table(u'vkontakte_ads_ad')

        # Deleting model 'Targeting'
        db.delete_table(u'vkontakte_ads_targeting')

        # Deleting model 'Layout'
        db.delete_table(u'vkontakte_ads_layout')

        # Deleting model 'Image'
        db.delete_table(u'vkontakte_ads_image')

        # Deleting model 'TargetingStats'
        db.delete_table(u'vkontakte_ads_targetingstats')

        # Deleting model 'Statistic'
        db.delete_table(u'vkontakte_ads_statistic')

        # Deleting model 'Budget'
        db.delete_table(u'vkontakte_ads_budget')


    models = {
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'vkontakte_ads.account': {
            'Meta': {'ordering': "['remote_id']", 'object_name': 'Account'},
            'access_role': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'account_status': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'fetched': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'remote_id': ('django.db.models.fields.BigIntegerField', [], {'primary_key': 'True'})
        },
        u'vkontakte_ads.ad': {
            'Meta': {'ordering': "['name']", 'object_name': 'Ad'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'bulk_ads'", 'to': u"orm['vkontakte_ads.Account']"}),
            'all_limit': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'approved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'archived': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'campaign': ('smart_selects.db_fields.ChainedForeignKey', [], {'related_name': "'bulk_ads'", 'to': u"orm['vkontakte_ads.Campaign']"}),
            'cost_type': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'cpc': ('vkontakte_api.fields.IntegerRangeField', [], {'null': 'True', 'blank': 'True'}),
            'cpm': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'disclaimer': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'fetched': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'name': ('vkontakte_api.fields.CharRangeLengthField', [], {'max_length': '100'}),
            'remote_id': ('django.db.models.fields.BigIntegerField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'vkontakte_ads.budget': {
            'Meta': {'object_name': 'Budget'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['vkontakte_ads.Account']", 'primary_key': 'True'}),
            'budget': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'fetched': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'})
        },
        u'vkontakte_ads.campaign': {
            'Meta': {'ordering': "['name']", 'object_name': 'Campaign'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'campaigns'", 'to': u"orm['vkontakte_ads.Account']"}),
            'all_limit': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'archived': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'client': ('smart_selects.db_fields.ChainedForeignKey', [], {'blank': 'True', 'related_name': "'campaigns'", 'null': 'True', 'to': u"orm['vkontakte_ads.Client']"}),
            'day_limit': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'fetched': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'name': ('vkontakte_api.fields.CharRangeLengthField', [], {'max_length': '60'}),
            'remote_id': ('django.db.models.fields.BigIntegerField', [], {'primary_key': 'True'}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'stop_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        u'vkontakte_ads.client': {
            'Meta': {'object_name': 'Client'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'clients'", 'to': u"orm['vkontakte_ads.Account']"}),
            'all_limit': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'archived': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'day_limit': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'fetched': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'remote_id': ('django.db.models.fields.BigIntegerField', [], {'primary_key': 'True'})
        },
        u'vkontakte_ads.image': {
            'Meta': {'object_name': 'Image'},
            'ad': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'image'", 'unique': 'True', 'primary_key': 'True', 'to': u"orm['vkontakte_ads.Ad']"}),
            'aid': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'fetched': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'hash': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'height': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'photo': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'photo_hash': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'post_url': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'server': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'size': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'}),
            'width': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'vkontakte_ads.layout': {
            'Meta': {'ordering': "['ad']", 'object_name': 'Layout'},
            'ad': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'layout'", 'unique': 'True', 'primary_key': 'True', 'to': u"orm['vkontakte_ads.Ad']"}),
            'campaign': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['vkontakte_ads.Campaign']"}),
            'description': ('vkontakte_api.fields.CharRangeLengthField', [], {'max_length': '100'}),
            'fetched': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'link_domain': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'link_url': ('django.db.models.fields.URLField', [], {'max_length': '500'}),
            'preview': ('django.db.models.fields.TextField', [], {}),
            'preview_link': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'title': ('vkontakte_api.fields.CharRangeLengthField', [], {'max_length': '50'})
        },
        u'vkontakte_ads.statistic': {
            'Meta': {'unique_together': "(('content_type', 'object_id', 'day', 'month', 'overall'),)", 'object_name': 'Statistic'},
            'clicks': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            'cpc': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'cpm': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'ctr': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'day': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'fetched': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'impressions': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'join_rate': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'month': ('django.db.models.fields.CharField', [], {'max_length': '7'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'overall': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'reach': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'spent': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'video_views': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'})
        },
        u'vkontakte_ads.targeting': {
            'Meta': {'ordering': "['ad']", 'object_name': 'Targeting'},
            'ad': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'targeting'", 'unique': 'True', 'primary_key': 'True', 'to': u"orm['vkontakte_ads.Ad']"}),
            'age_from': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'age_to': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'approved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'birthday': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '100', 'blank': 'True'}),
            'browsers': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '500', 'blank': 'True'}),
            'campaign': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['vkontakte_ads.Campaign']"}),
            'cities': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '500', 'blank': 'True'}),
            'cities_not': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '500', 'blank': 'True'}),
            'count': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'districts': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '500', 'blank': 'True'}),
            'fetched': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'group_types': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '500', 'blank': 'True'}),
            'groups': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '500', 'blank': 'True'}),
            'interests': ('vkontakte_api.fields.CommaSeparatedCharField', [], {'max_length': '500', 'blank': 'True'}),
            'operators': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '500', 'blank': 'True'}),
            'positions': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '500', 'blank': 'True'}),
            'religions': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '500', 'blank': 'True'}),
            'school_from': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'school_to': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'schools': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '500', 'blank': 'True'}),
            'sex': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'stations': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '500', 'blank': 'True'}),
            'statuses': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '500', 'blank': 'True'}),
            'streets': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '500', 'blank': 'True'}),
            'tags': ('vkontakte_api.fields.CommaSeparatedCharField', [], {'max_length': '200', 'blank': 'True'}),
            'travellers': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'uni_from': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'uni_to': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'})
        },
        u'vkontakte_ads.targetingstats': {
            'Meta': {'object_name': 'TargetingStats'},
            'audience_count': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'fetched': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'recommended_cpc': ('django.db.models.fields.FloatField', [], {}),
            'recommended_cpm': ('django.db.models.fields.FloatField', [], {})
        }
    }

    complete_apps = ['vkontakte_ads']