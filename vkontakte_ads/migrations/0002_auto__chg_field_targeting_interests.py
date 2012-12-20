# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'Targeting.interests'
        db.alter_column('vkontakte_ads_targeting', 'interests', self.gf('vkontakte_ads.fields.CommaSeparatedCharField')(max_length=500))


    def backwards(self, orm):
        
        # Changing field 'Targeting.interests'
        db.alter_column('vkontakte_ads_targeting', 'interests', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=100))


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
            'campaign': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['vkontakte_ads.Campaign']"}),
            'cost_type': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'cpc': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'cpm': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'description': ('vkontakte_ads.fields.CharRangeLengthField', [], {'max_length': '60'}),
            'disclaimer': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True'}),
            'hash': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link_domain': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'link_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'name': ('vkontakte_ads.fields.CharRangeLengthField', [], {'max_length': '60'}),
            'photo': ('django.db.models.fields.TextField', [], {}),
            'photo_hash': ('django.db.models.fields.TextField', [], {}),
            'remote_id': ('django.db.models.fields.BigIntegerField', [], {'unique': 'True'}),
            'server': ('django.db.models.fields.TextField', [], {}),
            'status': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'targeting': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'ad'", 'unique': 'True', 'null': 'True', 'to': "orm['vkontakte_ads.Targeting']"}),
            'title': ('vkontakte_ads.fields.CharRangeLengthField', [], {'max_length': '25'})
        },
        'vkontakte_ads.campaign': {
            'Meta': {'ordering': "['name']", 'object_name': 'Campaign'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['vkontakte_ads.Account']"}),
            'all_limit': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'client': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['vkontakte_ads.Client']", 'null': 'True'}),
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
