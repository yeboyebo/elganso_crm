# @class_declaration interna_eg_tiendaspromo #
import importlib

from YBUTILS.viewREST import helpers

from models.flcrm_mark import models as modelos


class interna_eg_tiendaspromo(modelos.mtd_eg_tiendaspromo, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration elganso_crm_eg_tiendaspromo #
class elganso_crm_eg_tiendaspromo(interna_eg_tiendaspromo, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration eg_tiendaspromo #
class eg_tiendaspromo(elganso_crm_eg_tiendaspromo, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    def getIface(self=None):
        return form.iface


definitions = importlib.import_module("models.flcrm_mark.eg_tiendaspromo_def")
form = definitions.FormInternalObj()
form._class_init()
form.iface.ctx = form.iface
form.iface.iface = form.iface
