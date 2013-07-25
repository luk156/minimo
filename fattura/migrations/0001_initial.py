# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Cliente'
        db.create_table(u'fattura_cliente', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ragione_sociale', self.gf('django.db.models.fields.CharField')(max_length=70)),
            ('indirizzo', self.gf('django.db.models.fields.CharField')(max_length=70)),
            ('cod_fiscale', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('p_iva', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('mail', self.gf('django.db.models.fields.EmailField')(max_length=50, null=True, blank=True)),
        ))
        db.send_create_signal(u'fattura', ['Cliente'])

        # Adding model 'TemplateFattura'
        db.create_table(u'fattura_templatefattura', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nome', self.gf('django.db.models.fields.CharField')(max_length=70)),
            ('descrizione', self.gf('django.db.models.fields.CharField')(max_length=70, null=True, blank=True)),
            ('template', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
        ))
        db.send_create_signal(u'fattura', ['TemplateFattura'])

        # Adding model 'Fattura'
        db.create_table(u'fattura_fattura', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('data', self.gf('django.db.models.fields.DateField')()),
            ('cliente', self.gf('django.db.models.fields.related.ForeignKey')(related_name='fattura_cliente', to=orm['fattura.Cliente'])),
            ('stato', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('template', self.gf('django.db.models.fields.related.ForeignKey')(related_name='fattura_template', to=orm['fattura.TemplateFattura'])),
        ))
        db.send_create_signal(u'fattura', ['Fattura'])

        # Adding model 'FatturaMinimo'
        db.create_table(u'fattura_fatturaminimo', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('bollo', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('valore_bollo', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'fattura', ['FatturaMinimo'])

        # Adding model 'FatturaStandard'
        db.create_table(u'fattura_fatturastandard', (
            (u'fattura_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['fattura.Fattura'], unique=True, primary_key=True)),
            ('IVA', self.gf('django.db.models.fields.IntegerField')(max_length=30)),
        ))
        db.send_create_signal(u'fattura', ['FatturaStandard'])

        # Adding model 'Prestazione'
        db.create_table(u'fattura_prestazione', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('descrizione', self.gf('django.db.models.fields.TextField')()),
            ('importo', self.gf('django.db.models.fields.FloatField')()),
            ('fattura', self.gf('django.db.models.fields.related.ForeignKey')(related_name='prestazione_fattura', to=orm['fattura.Fattura'])),
        ))
        db.send_create_signal(u'fattura', ['Prestazione'])


    def backwards(self, orm):
        # Deleting model 'Cliente'
        db.delete_table(u'fattura_cliente')

        # Deleting model 'TemplateFattura'
        db.delete_table(u'fattura_templatefattura')

        # Deleting model 'Fattura'
        db.delete_table(u'fattura_fattura')

        # Deleting model 'FatturaMinimo'
        db.delete_table(u'fattura_fatturaminimo')

        # Deleting model 'FatturaStandard'
        db.delete_table(u'fattura_fatturastandard')

        # Deleting model 'Prestazione'
        db.delete_table(u'fattura_prestazione')


    models = {
        u'fattura.cliente': {
            'Meta': {'object_name': 'Cliente'},
            'cod_fiscale': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'indirizzo': ('django.db.models.fields.CharField', [], {'max_length': '70'}),
            'mail': ('django.db.models.fields.EmailField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'p_iva': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'ragione_sociale': ('django.db.models.fields.CharField', [], {'max_length': '70'})
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