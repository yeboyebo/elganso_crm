# @class_declaration interna_eg_tipospromocion #
import importlib

from YBUTILS.viewREST import helpers

from models.flcrm_mark import models as modelos


class interna_eg_tipospromocion(modelos.mtd_eg_tipospromocion, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration elganso_crm_eg_tipospromocion #
class elganso_crm_eg_tipospromocion(interna_eg_tipospromocion, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration eg_tipospromocion #
class eg_tipospromocion(elganso_crm_eg_tipospromocion, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    def getIface(self=None):
        return form.iface


definitions = importlib.import_module("models.flcrm_mark.eg_tipospromocion_def")
form = definitions.FormInternalObj()
form._class_init()
form.iface.ctx = form.iface
form.iface.iface = form.iface
