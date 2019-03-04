# @class_declaration interna_tallas #
import importlib

from YBUTILS.viewREST import helpers

from models.flfactalma import models as modelos


class interna_tallas(modelos.mtd_tallas, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration elganso_crm_tallas #
class elganso_crm_tallas(interna_tallas, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration tallas #
class tallas(elganso_crm_tallas, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    def getIface(self=None):
        return form.iface


definitions = importlib.import_module("models.flfactalma.tallas_def")
form = definitions.FormInternalObj()
form._class_init()
form.iface.ctx = form.iface
form.iface.iface = form.iface
