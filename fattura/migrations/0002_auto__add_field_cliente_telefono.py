# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Cliente.telefono'
        db.add_column(u'fattura_cliente', 'telefono',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Cliente.telefono'
        db.delete_column(u'fattura_cliente', 'telefono')


    models = {
        u'fattura.cliente': {
            'Meta': {'object_name': 'Cliente'},
            'cod_fiscale': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'indirizzo': ('django.db.models.fields.CharField', [], {'max_length': '70'}),
            'mail': ('django.db.models.fields.EmailField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'p_iva': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'ragione_sociale': ('django.db.models.fields.CharField', [], {'max_length': '70'}),
            'telefono': ('django.db.models.fields.IntegerField', [], {})
        },
        u'fattura.fattura': {
            'Meta': {'object_name': 'Fattura'},
            'cliente': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'fattura_cliente'", 'to': u"orm['fattura.Cliente']"}),
            'data': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'stato': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'template': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'fattura_template'", 'to': u"orm['fattura.TemplateFattura']"})
        },
        u'fattura.fatturaminimo': {
            'Meta': {'object_name': 'FatturaMinimo'},
            'bollo': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'valore_bollo': ('django.db.models.fields.IntegerField', [], {})
        },
        u'fattura.fatturastandard': {
            'IVA': ('django.db.models.fields.IntegerField', [], {'max_length': '30'}),
            'Meta': {'object_name': 'FatturaStandard', '_ormbases': [u'fattura.Fattura']},
            u'fattura_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['fattura.Fattura']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'fattura.prestazione': {
            'Meta': {'object_name': 'Prestazione'},
            'descrizione': ('django.db.models.fields.TextField', [], {}),
            'fattura': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'prestazione_fattura'", 'to': u"orm['fattura.Fattura']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'importo': ('django.db.models.fields.FloatField', [], {})
        },
        u'fattura.templatefattura': {
            'Meta': {'object_name': 'TemplateFattura'},
            'descrizione': ('django.db.models.fields.CharField', [], {'max_length': '70', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '70'}),
            'template': ('django.db.models.fields.files.FileField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['fattura']