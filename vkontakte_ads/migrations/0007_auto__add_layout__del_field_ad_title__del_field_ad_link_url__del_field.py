# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):

        # Adding model 'Layout'
        db.create_table('vkontakte_ads_layout', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('remote_id', self.gf('django.db.models.fields.BigIntegerField')(unique=True)),
            ('campaign', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['vkontakte_ads.Campaign'])),
            ('title', self.gf('vkontakte_ads.fields.CharRangeLengthField')(max_length=25)),
            ('description', self.gf('vkontakte_ads.fields.CharRangeLengthField')(max_length=60)),
            ('link_url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('link_domain', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('preview_link', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('vkontakte_ads', ['Layout'])

        # Deleting field 'Ad.title'
        db.delete_column('vkontakte_ads_ad', 'title')

        # Deleting field 'Ad.link_url'
        db.delete_column('vkontakte_ads_ad', 'link_url')

        # Deleting field 'Ad.link_domain'
        db.delete_column('vkontakte_ads_ad', 'link_domain')

        # Deleting field 'Ad.description'
        db.delete_column('vkontakte_ads_ad', 'description')

        # Adding field 'Ad.layout'
        db.add_column('vkontakte_ads_ad', 'layout', self.gf('django.db.models.fields.related.OneToOneField')(related_name='ad', unique=True, null=True, to=orm['vkontakte_ads.Layout']), keep_default=False)

        # Adding field 'Ad.preview_link'
        db.add_column('vkontakte_ads_ad', 'preview_link', self.gf('django.db.models.fields.CharField')(default='', max_length=200), keep_default=False)


    def backwards(self, orm):

        # Deleting model 'Layout'
        db.delete_table('vkontakte_ads_layout')

        # Adding field 'Ad.title'
        db.add_column('vkontakte_ads_ad', 'title', self.gf('vkontakte_ads.fields.CharRangeLengthField')(default='', max_length=25), keep_default=False)

        # Adding field 'Ad.link_url'
        db.add_column('vkontakte_ads_ad', 'link_url', self.gf('django.db.models.fields.URLField')(default='', max_length=200), keep_default=False)

        # Adding field 'Ad.link_domain'
        db.add_column('vkontakte_ads_ad', 'link_domain', self.gf('django.db.models.fields.CharField')(default='', max_length=50), keep_default=False)

        # Adding field 'Ad.description'
        db.add_column('vkontakte_ads_ad', 'description', self.gf('vkontakte_ads.fields.CharRangeLengthField')(default='', max_length=60), keep_default=False)

        # Deleting field 'Ad.layout'
        db.delete_column('vkontakte_ads_ad', 'layout_id')

        # Deleting field 'Ad.preview_link'
        db.delete_column('vkontakte_ads_ad', 'preview_link')


    models = {
        'vkontakte_ads.account': {
            'Meta': {'ordering': "['remote_id']", 'object_name': 'Account'},
            'access_role': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'account_id': ('django.db.models.fields.BigIntegerField', [], {'unique': 'True'}),
            'account_status': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'remote_id': ('django.db.models.fields.BigIntegerField', [], {'unique': 'True'})
        },
        'vkontakte_ads.ad': {
            'Meta': {'ordering': "['name']", 'object_name': 'Ad'},
            'all_limit': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'approved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'campaign': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'ads'", 'to': "orm['vkontakte_ads.Campaign']"}),
            'cost_type': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'cpc': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'cpm': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'disclaimer': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True'}),
            'hash': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'layout': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'ad'", 'unique': 'True', 'null': 'True', 'to': "orm['vkontakte_ads.Layout']"}),
            'name': ('vkontakte_ads.fields.CharRangeLengthField', [], {'max_length': '60'}),
            'photo': ('django.db.models.fields.TextField', [], {}),
            'photo_hash': ('django.db.models.fields.TextField', [], {}),
            'preview_link': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'remote_id': ('django.db.models.fields.BigIntegerField', [], {'unique': 'True'}),
            'server': ('django.db.models.fields.TextField', [], {}),
            'status': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'targeting': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'ad'", 'unique': 'True', 'null': 'True', 'to': "orm['vkontakte_ads.Targeting']"})
        },
        'vkontakte_ads.budget': {
            'Meta': {'object_name': 'Budget'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['vkontakte_ads.Account']", 'primary_key': 'True'}),
            'budget': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'})
        },
        'vkontakte_ads.campaign': {
            'Meta': {'ordering': "['name']", 'object_name': 'Campaign'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'campaigns'", 'to': "orm['vkontakte_ads.Account']"}),
            'all_limit': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'client': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'campaigns'", 'null': 'True', 'to': "orm['vkontakte_ads.Client']"}),
            'day_limit': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('vkontakte_ads.fields.CharRangeLengthField', [], {'max_length': '60'}),
            'remote_id': ('django.db.models.fields.BigIntegerField', [], {'unique': 'True'}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'status': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'stop_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True'})
        },
        'vkontakte_ads.client': {
            'Meta': {'object_name': 'Client'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'remote_id': ('django.db.models.fields.BigIntegerField', [], {'unique': 'True'})
        },
        'vkontakte_ads.layout': {
            'Meta': {'ordering': "['remote_id']", 'object_name': 'Layout'},
            'campaign': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['vkontakte_ads.Campaign']"}),
            'description': ('vkontakte_ads.fields.CharRangeLengthField', [], {'max_length': '60'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link_domain': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'link_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'preview_link': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'remote_id': ('django.db.models.fields.BigIntegerField', [], {'unique': 'True'}),
            'title': ('vkontakte_ads.fields.CharRangeLengthField', [], {'max_length': '25'})
        },
        'vkontakte_ads.report': {
            'Meta': {'unique_together': "(('campaign', 'day'),)", 'object_name': 'Report'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'reports'", 'to': "orm['vkontakte_ads.Account']"}),
            'campaign': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'reports'", 'to': "orm['vkontakte_ads.Campaign']"}),
            'campaign_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'clicks': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'client': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['vkontakte_ads.Client']", 'null': 'True'}),
            'client_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'ctr': ('django.db.models.fields.DecimalField', [], {'max_digits': '4', 'decimal_places': '3'}),
            'day': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'group_ads': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True'}),
            'group_time': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'impressions': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'money': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'month': ('django.db.models.fields.CharField', [], {'max_length': '7', 'null': 'True'}),
            'stats_type': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True'}),
            'time_from': ('django.db.models.fields.DateTimeField', [], {}),
            'time_to': ('django.db.models.fields.DateTimeField', [], {})
        },
        'vkontakte_ads.stat': {
            'Meta': {'object_name': 'Stat'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['vkontakte_ads.Account']"}),
            'ad': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['vkontakte_ads.Ad']", 'null': 'True'}),
            'campaign': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['vkontakte_ads.Campaign']", 'null': 'True'}),
            'clicks': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'data': ('annoying.fields.JSONField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'impressions': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'money': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'month': ('django.db.models.fields.CharField', [], {'max_length': '7'}),
            'period': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
        },
        'vkontakte_ads.targeting': {
            'Meta': {'ordering': "['remote_id']", 'object_name': 'Targeting'},
            'age_from': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'age_to': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'approved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'birthday': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'browsers': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '100'}),
            'campaign': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['vkontakte_ads.Campaign']"}),
            'cities': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '100'}),
            'cities_not': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '100'}),
            'count': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'country': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'districts': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '100'}),
            'group_types': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '100'}),
            'groups': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interests': ('vkontakte_ads.fields.CommaSeparatedCharField', [], {'max_length': '500'}),
            'operators': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '100'}),
            'positions': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '100'}),
            'religions': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '100'}),
            'remote_id': ('django.db.models.fields.BigIntegerField', [], {'unique': 'True'}),
            'school_from': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'school_to': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'schools': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '100'}),
            'sex': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'stations': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '100'}),
            'statuses': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '100'}),
            'streets': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '100'}),
            'tags': ('vkontakte_ads.fields.CommaSeparatedCharField', [], {'max_length': '200'}),
            'travellers': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'uni_from': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'uni_to': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['vkontakte_ads']
