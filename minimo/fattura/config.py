from livesettings import config_register, ConfigurationGroup, PositiveIntegerValue, MultipleStringValue
from django.utils.translation import ugettext_lazy as _
from livesettings.values import *

# First, setup a grup to hold all our possible configs
FATTURA_GROUP = ConfigurationGroup(
    'Fattura',               # key: internal name of the group to be created
    _('Configurazione fattura'),  # name: verbose name which can be automatically translated
    ordering=0             # ordering: order of group in the list (default is 1)
    )

config_register(StringValue(
        FATTURA_GROUP,
        'RAGIONESOCIALE',
        description=_("ragione sociale azienda"),
        help_text=_("ragione sociale."),
        default=""
    ))

config_register(BooleanValue(
        FATTURA_GROUP,
        'Iscrizione a gestione separata ',
        description=_("iscrizione a gestione separata"),
        help_text=_("iscrizione a gestione separata."),
        default=False
    ))
