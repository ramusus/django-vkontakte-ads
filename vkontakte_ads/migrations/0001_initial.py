# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Account'
        db.create_table('vkontakte_ads_account', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('remote_id', self.gf('django.db.models.fields.BigIntegerField')(unique=True)),
            ('account_id', self.gf('django.db.models.fields.BigIntegerField')(unique=True)),
            ('account_status', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('access_role', self.gf('django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal('vkontakte_ads', ['Account'])

        # Adding model 'Client'
        db.create_table('vkontakte_ads_client', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('remote_id', self.gf('django.db.models.fields.BigIntegerField')(unique=True)),
        ))
        db.send_create_signal('vkontakte_ads', ['Client'])

        # Adding model 'Campaign'
        db.create_table('vkontakte_ads_campaign', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('remote_id', self.gf('django.db.models.fields.BigIntegerField')(unique=True)),
            ('account', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['vkontakte_ads.Account'])),
            ('client', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['vkontakte_ads.Client'], null=True)),
            ('name', self.gf('vkontakte_ads.fields.CharRangeLengthField')(max_length=60)),
            ('day_limit', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('all_limit', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('start_time', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('stop_time', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('status', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('vkontakte_ads', ['Campaign'])

        # Adding model 'Targeting'
        db.create_table('vkontakte_ads_targeting', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('remote_id', self.gf('django.db.models.fields.BigIntegerField')(unique=True)),
            ('campaign', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['vkontakte_ads.Campaign'])),
            ('sex', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('age_from', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('age_to', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('birthday', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('country', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('cities', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=100)),
            ('cities_not', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=100)),
            ('statuses', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=100)),
            ('group_types', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=100)),
            ('groups', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=100)),
            ('districts', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=100)),
            ('stations', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=100)),
            ('streets', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=100)),
            ('schools', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=100)),
            ('positions', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=100)),
            ('religions', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=100)),
            ('interests', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=100)),
            ('browsers', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=100)),
            ('travellers', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('school_from', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('school_to', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('uni_from', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('uni_to', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('tags', self.gf('vkontakte_ads.fields.CommaSeparatedCharField')(max_length=200)),
            ('approved', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('count', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('operators', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=100)),
        ))
        db.send_create_signal('vkontakte_ads', ['Targeting'])

        # Adding model 'Ad'
        db.create_table('vkontakte_ads_ad', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('remote_id', self.gf('django.db.models.fields.BigIntegerField')(unique=True)),
            ('campaign', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['vkontakte_ads.Campaign'])),
            ('cost_type', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('cpc', self.gf('django.db.models.fields.PositiveIntegerField')(null=True)),
            ('cpm', self.gf('django.db.models.fields.PositiveIntegerField')(null=True)),
            ('name', self.gf('vkontakte_ads.fields.CharRangeLengthField')(max_length=60)),
            ('title', self.gf('vkontakte_ads.fields.CharRangeLengthField')(max_length=25)),
            ('description', self.gf('vkontakte_ads.fields.CharRangeLengthField')(max_length=60)),
            ('link_url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('link_domain', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('hash', self.gf('django.db.models.fields.TextField')()),
            ('photo_hash', self.gf('django.db.models.fields.TextField')()),
            ('photo', self.gf('django.db.models.fields.TextField')()),
            ('server', self.gf('django.db.models.fields.TextField')()),
            ('all_limit', self.gf('django.db.models.fields.PositiveIntegerField')(null=True)),
            ('status', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('disclaimer', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True)),
            ('targeting', self.gf('django.db.models.fields.related.OneToOneField')(related_name='ad', unique=True, null=True, to=orm['vkontakte_ads.Targeting'])),
            ('approved', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('vkontakte_ads', ['Ad'])


    def backwards(self, orm):
        
        # Deleting model 'Account'
        db.delete_table('vkontakte_ads_account')

        # Deleting model 'Client'
        db.delete_table('vkontakte_ads_client')

        # Deleting model 'Campaign'
        db.delete_table('vkontakte_ads_campaign')

        # Deleting model 'Targeting'
        db.delete_table('vkontakte_ads_targeting')

        # Deleting model 'Ad'
        db.delete_table('vkontakte_ads_ad')


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
            'interests': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '100'}),
            'operators': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '100'}),
            'positions': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '100'}),
            'religions': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '100'}),
            'remote_id': ('django.db.models.fields.BigIntegerField', [], {'unique': 'True'}),
            'school_from': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'school_to': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'schools': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '100'}),
            'sex': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
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
