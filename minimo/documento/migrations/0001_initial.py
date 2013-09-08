# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Pagamento'
        db.create_table(u'documento_pagamento', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nome', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('giorni', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'documento', ['Pagamento'])

        # Adding model 'Documento'
        db.create_table(u'documento_documento', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('tipo', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('numero', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('data', self.gf('django.db.models.fields.DateField')()),
            ('data_consegna', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('ragione_sociale', self.gf('django.db.models.fields.CharField')(max_length=70, null=True, blank=True)),
            ('via', self.gf('django.db.models.fields.CharField')(max_length=70, null=True, blank=True)),
            ('cap', self.gf('django.db.models.fields.CharField')(max_length=6, null=True, blank=True)),
            ('citta', self.gf('django.db.models.fields.CharField')(max_length=70, null=True, blank=True)),
            ('provincia', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('cod_fiscale', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('p_iva', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('stato', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('template', self.gf('django.db.models.fields.related.ForeignKey')(related_name='documento_template', null=True, on_delete=models.SET_NULL, to=orm['template.TemplateDocumento'])),
            ('descrizione_ritenuta', self.gf('django.db.models.fields.CharField')(max_length=70, null=True, blank=True)),
            ('ritenuta', self.gf('django.db.models.fields.IntegerField')(default=None, null=True, blank=True)),
            ('bollo', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('valore_bollo', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('pagamento', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['documento.Pagamento'], null=True, blank=True)),
            ('riferimento', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['documento.Documento'], null=True, blank=True)),
            ('note', self.gf('django.db.models.fields.TextField')(max_length=1024, null=True, blank=True)),
            ('sconto', self.gf('django.db.models.fields.IntegerField')(default=None, null=True, blank=True)),
        ))
        db.send_create_signal(u'documento', ['Documento'])

        # Adding model 'Riga'
        db.create_table(u'documento_riga', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('codice', self.gf('django.db.models.fields.CharField')(default=None, max_length=70, null=True, blank=True)),
            ('descrizione', self.gf('django.db.models.fields.TextField')()),
            ('quantita', self.gf('django.db.models.fields.FloatField')()),
            ('importo_unitario', self.gf('django.db.models.fields.FloatField')(default=1)),
            ('descrizione_imposta', self.gf('django.db.models.fields.CharField')(default=None, max_length=70, null=True, blank=True)),
            ('imposta', self.gf('django.db.models.fields.IntegerField')(default=None, null=True, blank=True)),
            ('documento', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['documento.Documento'])),
        ))
        db.send_create_signal(u'documento', ['Riga'])


    def backwards(self, orm):
        # Deleting model 'Pagamento'
        db.delete_table(u'documento_pagamento')

        # Deleting model 'Documento'
        db.delete_table(u'documento_documento')

        # Deleting model 'Riga'
        db.delete_table(u'documento_riga')


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
        u'documento.documento': {
            'Meta': {'ordering': "['data']", 'object_name': 'Documento'},
            'bollo': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'cap': ('django.db.models.fields.CharField', [], {'max_length': '6', 'null': 'True', 'blank': 'True'}),
            'citta': ('django.db.models.fields.CharField', [], {'max_length': '70', 'null': 'True', 'blank': 'True'}),
            'cod_fiscale': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'data': ('django.db.models.fields.DateField', [], {}),
            'data_consegna': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'descrizione_ritenuta': ('django.db.models.fields.CharField', [], {'max_length': '70', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'note': ('django.db.models.fields.TextField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'numero': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'p_iva': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'pagamento': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['documento.Pagamento']", 'null': 'True', 'blank': 'True'}),
            'provincia': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'ragione_sociale': ('django.db.models.fields.CharField', [], {'max_length': '70', 'null': 'True', 'blank': 'True'}),
            'riferimento': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['documento.Documento']", 'null': 'True', 'blank': 'True'}),
            'ritenuta': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'sconto': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'stato': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'template': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'documento_template'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['template.TemplateDocumento']"}),
            'tipo': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'valore_bollo': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'via': ('django.db.models.fields.CharField', [], {'max_length': '70', 'null': 'True', 'blank': 'True'})
        },
        u'documento.pagamento': {
            'Meta': {'object_name': 'Pagamento'},
            'giorni': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'documento.riga': {
            'Meta': {'object_name': 'Riga'},
            'codice': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '70', 'null': 'True', 'blank': 'True'}),
            'descrizione': ('django.db.models.fields.TextField', [], {}),
            'descrizione_imposta': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '70', 'null': 'True', 'blank': 'True'}),
            'documento': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['documento.Documento']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'importo_unitario': ('django.db.models.fields.FloatField', [], {'default': '1'}),
            'imposta': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'quantita': ('django.db.models.fields.FloatField', [], {})
        },
        u'template.templatedocumento': {
            'Meta': {'object_name': 'TemplateDocumento'},
            'descrizione': ('django.db.models.fields.CharField', [], {'max_length': '70', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '70'}),
            'template': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        }
    }

    complete_apps = ['documento']