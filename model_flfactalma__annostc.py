# @class_declaration interna_annostc #
import importlib

from YBUTILS.viewREST import helpers

from models.flfactalma import models as modelos


class interna_annostc(modelos.mtd_annostc, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration elganso_crm_annostc #
class elganso_crm_annostc(interna_annostc, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration annostc #
class annostc(elganso_crm_annostc, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    def getIface(self=None):
        return form.iface


definitions = importlib.import_module("models.flfactalma.annostc_def")
form = definitions.FormInternalObj()
form._class_init()
form.iface.ctx = form.iface
form.iface.iface = form.iface
