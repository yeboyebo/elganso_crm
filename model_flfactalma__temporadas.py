# @class_declaration interna_temporadas #
import importlib

from YBUTILS.viewREST import helpers

from models.flfactalma import models as modelos


class interna_temporadas(modelos.mtd_temporadas, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration elganso_crm_temporadas #
class elganso_crm_temporadas(interna_temporadas, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration temporadas #
class temporadas(elganso_crm_temporadas, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    def getIface(self=None):
        return form.iface


definitions = importlib.import_module("models.flfactalma.temporadas_def")
form = definitions.FormInternalObj()
form._class_init()
form.iface.ctx = form.iface
form.iface.iface = form.iface
