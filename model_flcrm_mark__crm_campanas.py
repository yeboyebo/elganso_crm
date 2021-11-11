# @class_declaration elganso_crm_crm_campanas #
class elganso_crm_crm_campanas(flcrm_mark_crm_campanas, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    def getForeignFields(self, template=None):
        return form.iface.getForeignFields(self, template)

    def getFilters(self, name, template=None):
        return form.iface.getFilters(self, name, template)

    def initValidation(name, data):
        return form.iface.initValidation(name, data)

    def iniciaValoresLabel(self, template=None, cursor=None, data=None):
        return form.iface.iniciaValoresLabel(self, template, cursor)

    def bChLabel(fN=None, cursor=None):
        return form.iface.bChLabel(fN, cursor)

    @helpers.decoradores.accion(aqparam=["oParam"])
    def publicarPromocionCampana(self, oParam):
        return form.iface.publicarPromocionCampana(self, oParam)

    @helpers.decoradores.accion(aqparam=["oParam", "cursor"])
    def sendSalesApi(self, oParam, cursor):
        return form.iface.sendSalesApi(self, oParam, cursor)

    def generaCSVDestinatarios(cursor=None, params=None):
        return form.iface.generaCSVDestinatarios(cursor, params)

    # def dameWhereFiltros(self, codcampana=None, canal=None):
    #     return form.iface.dameWhereFiltros(self, codcampana, canal)

    def recontarDestinatarios(cursor=None, soloSuscritos=False, soloFidelizados=False):
        return form.iface.recontarDestinatarios(cursor, soloSuscritos, soloFidelizados)
        
    def insertarPromoPuntosComanda(self, cursor, curPromocion):
        return form.iface.insertarPromoPuntosComanda(self, cursor, curPromocion)

    def iniciaValoresCursor(cursor=None):
        return form.iface.iniciaValoresCursor(cursor)
