
# @class_declaration elganso_crm_crm_campanas #
class elganso_crm_crm_campanas(flcrm_mark_crm_campanas, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    @helpers.decoradores.accion(aqparam=["oParam"])
    def publicarPromocionCampana(self, oParam):
        return form.iface.publicarPromocionCampana(self, oParam)

    @helpers.decoradores.accion(aqparam=["oParam", "cursor"])
    def sendSalesApi(self, oParam, cursor):
        return form.iface.sendSalesApi(self, oParam, cursor)

    def generaCSVDestinatarios(cursor=None, params=None):
        return form.iface.generaCSVDestinatarios(cursor, params)

    def recontarDestinatarios(cursor=None, soloSuscritos=False):
        return form.iface.recontarDestinatarios(cursor, soloSuscritos)

    def insertarPromoPuntosComanda(self, cursor, curPromocion):
        return form.iface.insertarPromoPuntosComanda(self, cursor, curPromocion)

