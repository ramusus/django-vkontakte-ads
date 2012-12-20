# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'Targeting.groups'
        db.alter_column('vkontakte_ads_targeting', 'groups', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=500))

        # Changing field 'Targeting.streets'
        db.alter_column('vkontakte_ads_targeting', 'streets', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=500))

        # Changing field 'Targeting.religions'
        db.alter_column('vkontakte_ads_targeting', 'religions', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=500))

        # Changing field 'Targeting.browsers'
        db.alter_column('vkontakte_ads_targeting', 'browsers', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=500))

        # Changing field 'Targeting.cities_not'
        db.alter_column('vkontakte_ads_targeting', 'cities_not', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=500))

        # Changing field 'Targeting.statuses'
        db.alter_column('vkontakte_ads_targeting', 'statuses', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=500))

        # Changing field 'Targeting.operators'
        db.alter_column('vkontakte_ads_targeting', 'operators', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=500))

        # Changing field 'Targeting.schools'
        db.alter_column('vkontakte_ads_targeting', 'schools', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=500))

        # Changing field 'Targeting.cities'
        db.alter_column('vkontakte_ads_targeting', 'cities', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=500))

        # Changing field 'Targeting.group_types'
        db.alter_column('vkontakte_ads_targeting', 'group_types', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=500))

        # Changing field 'Targeting.stations'
        db.alter_column('vkontakte_ads_targeting', 'stations', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=500))

        # Changing field 'Targeting.districts'
        db.alter_column('vkontakte_ads_targeting', 'districts', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=500))

        # Changing field 'Targeting.positions'
        db.alter_column('vkontakte_ads_targeting', 'positions', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=500))


    def backwards(self, orm):
        
        # Changing field 'Targeting.groups'
        db.alter_column('vkontakte_ads_targeting', 'groups', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=100))

        # Changing field 'Targeting.streets'
        db.alter_column('vkontakte_ads_targeting', 'streets', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=100))

        # Changing field 'Targeting.religions'
        db.alter_column('vkontakte_ads_targeting', 'religions', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=100))

        # Changing field 'Targeting.browsers'
        db.alter_column('vkontakte_ads_targeting', 'browsers', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=100))

        # Changing field 'Targeting.cities_not'
        db.alter_column('vkontakte_ads_targeting', 'cities_not', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=100))

        # Changing field 'Targeting.statuses'
        db.alter_column('vkontakte_ads_targeting', 'statuses', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=100))

        # Changing field 'Targeting.operators'
        db.alter_column('vkontakte_ads_targeting', 'operators', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=100))

        # Changing field 'Targeting.schools'
        db.alter_column('vkontakte_ads_targeting', 'schools', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=100))

        # Changing field 'Targeting.cities'
        db.alter_column('vkontakte_ads_targeting', 'cities', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=100))

        # Changing field 'Targeting.group_types'
        db.alter_column('vkontakte_ads_targeting', 'group_types', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=100))

        # Changing field 'Targeting.stations'
        db.alter_column('vkontakte_ads_targeting', 'stations', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=100))

        # Changing field 'Targeting.districts'
        db.alter_column('vkontakte_ads_targeting', 'districts', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=100))

        # Changing field 'Targeting.positions'
        db.alter_column('vkontakte_ads_targeting', 'positions', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=100))


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
            'cpc': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'cpm': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'disclaimer': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'hash': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'layout': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'ad'", 'unique': 'True', 'null': 'True', 'to': "orm['vkontakte_ads.Layout']"}),
            'name': ('vkontakte_api.fields.CharRangeLengthField', [], {'max_length': '60'}),
            'photo': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'photo_hash': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'remote_id': ('django.db.models.fields.BigIntegerField', [], {'unique': 'True'}),
            'server': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
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
            'name': ('vkontakte_api.fields.CharRangeLengthField', [], {'max_length': '60'}),
            'remote_id': ('django.db.models.fields.BigIntegerField', [], {'unique': 'True'}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'status': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'stop_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True'})
        },
        'vkontakte_ads.client': {
            'Meta': {'object_name': 'Client'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'clients'", 'to': "orm['vkontakte_ads.Account']"}),
            'all_limit': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'day_limit': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'remote_id': ('django.db.models.fields.BigIntegerField', [], {'unique': 'True'})
        },
        'vkontakte_ads.layout': {
            'Meta': {'ordering': "['remote_id']", 'object_name': 'Layout'},
            'campaign': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['vkontakte_ads.Campaign']"}),
            'description': ('vkontakte_api.fields.CharRangeLengthField', [], {'max_length': '60'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link_domain': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'link_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'preview_link': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'remote_id': ('django.db.models.fields.BigIntegerField', [], {'unique': 'True'}),
            'title': ('vkontakte_api.fields.CharRangeLengthField', [], {'max_length': '25'})
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
            'birthday': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '100', 'blank': 'True'}),
            'browsers': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '500', 'blank': 'True'}),
            'campaign': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['vkontakte_ads.Campaign']"}),
            'cities': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '500', 'blank': 'True'}),
            'cities_not': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '500', 'blank': 'True'}),
            'count': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'country': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'districts': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '500', 'blank': 'True'}),
            'group_types': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '500', 'blank': 'True'}),
            'groups': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '500', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interests': ('vkontakte_api.fields.CommaSeparatedCharField', [], {'max_length': '500', 'blank': 'True'}),
            'operators': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '500', 'blank': 'True'}),
            'positions': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '500', 'blank': 'True'}),
            'religions': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '500', 'blank': 'True'}),
            'remote_id': ('django.db.models.fields.BigIntegerField', [], {'unique': 'True'}),
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
        }
    }

    complete_apps = ['vkontakte_ads']
