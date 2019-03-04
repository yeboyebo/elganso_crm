# @class_declaration interna_eg_promospersonales #
import importlib

from YBUTILS.viewREST import helpers

from models.flcrm_mark import models as modelos


class interna_eg_promospersonales(modelos.mtd_eg_promospersonales, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration elganso_crm_eg_promospersonales #
class elganso_crm_eg_promospersonales(interna_eg_promospersonales, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration eg_promospersonales #
class eg_promospersonales(elganso_crm_eg_promospersonales, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    def getIface(self=None):
        return form.iface


definitions = importlib.import_module("models.flcrm_mark.eg_promospersonales_def")
form = definitions.FormInternalObj()
form._class_init()
form.iface.ctx = form.iface
form.iface.iface = form.iface
