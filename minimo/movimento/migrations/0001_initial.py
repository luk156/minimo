# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Movimento'
        db.create_table(u'movimento_movimento', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('tipo', self.gf('django.db.models.fields.CharField')(max_length=70)),
            ('data_movimento', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('descrizione', self.gf('django.db.models.fields.TextField')(max_length=1024, null=True, blank=True)),
            ('importo', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal(u'movimento', ['Movimento'])

        # Adding model 'FattureFornitore'
        db.create_table(u'movimento_fatturefornitore', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('tipo', self.gf('django.db.models.fields.CharField')(max_length=70)),
            ('data_documento', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('numero', self.gf('django.db.models.fields.CharField')(max_length=70)),
            ('scadenza_pagamento', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('descrizione', self.gf('django.db.models.fields.TextField')(max_length=1024, null=True, blank=True)),
            ('importo', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal(u'movimento', ['FattureFornitore'])


    def backwards(self, orm):
        # Deleting model 'Movimento'
        db.delete_table(u'movimento_movimento')

        # Deleting model 'FattureFornitore'
        db.delete_table(u'movimento_fatturefornitore')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'movimento.fatturefornitore': {
            'Meta': {'ordering': "['data_documento']", 'object_name': 'FattureFornitore'},
            'data_documento': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'descrizione': ('django.db.models.fields.TextField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'importo': ('django.db.models.fields.FloatField', [], {}),
            'numero': ('django.db.models.fields.CharField', [], {'max_length': '70'}),
            'scadenza_pagamento': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'tipo': ('django.db.models.fields.CharField', [], {'max_length': '70'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'movimento.movimento': {
            'Meta': {'ordering': "['data_movimento']", 'object_name': 'Movimento'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            'data_movimento': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'descrizione': ('django.db.models.fields.TextField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'importo': ('django.db.models.fields.FloatField', [], {}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'tipo': ('django.db.models.fields.CharField', [], {'max_length': '70'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        }
    }

    complete_apps = ['movimento']