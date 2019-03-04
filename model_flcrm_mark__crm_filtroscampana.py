# @class_declaration interna_crm_filtroscampana #
import importlib

from YBUTILS.viewREST import helpers

from models.flcrm_mark import models as modelos


class interna_crm_filtroscampana(modelos.mtd_crm_filtroscampana, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration elganso_crm_crm_filtroscampana #
class elganso_crm_crm_filtroscampana(interna_crm_filtroscampana, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    @helpers.decoradores.accion()
    def dameTemplateFiltro(self):
        return form.iface.dameTemplateFiltro(self)

    @helpers.decoradores.accion(aqparam=["oParam"])
    def insertaListas(self, oParam):
        return form.iface.insertaListas(self, oParam)

    def queryGrid_filtroCiudades(self):
        return form.iface.queryGrid_filtroCiudades(self)


# @class_declaration crm_filtroscampana #
class crm_filtroscampana(elganso_crm_crm_filtroscampana, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    def getIface(self=None):
        return form.iface


definitions = importlib.import_module("models.flcrm_mark.crm_filtroscampana_def")
form = definitions.FormInternalObj()
form._class_init()
form.iface.ctx = form.iface
form.iface.iface = form.iface
