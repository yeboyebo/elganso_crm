# @class_declaration interna_gruposmoda #
import importlib

from YBUTILS.viewREST import helpers

from models.flfactalma import models as modelos


class interna_gruposmoda(modelos.mtd_gruposmoda, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration elganso_crm_gruposmoda #
class elganso_crm_gruposmoda(interna_gruposmoda, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration gruposmoda #
class gruposmoda(elganso_crm_gruposmoda, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    def getIface(self=None):
        return form.iface


definitions = importlib.import_module("models.flfactalma.gruposmoda_def")
form = definitions.FormInternalObj()
form._class_init()
form.iface.ctx = form.iface
form.iface.iface = form.iface
