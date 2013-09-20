from django import template

register = template.Library()

@register.filter
def tot_imposta(instance,arg):
	return instance.calcola(arg)