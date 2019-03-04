# @class_declaration interna #
from YBLEGACY import qsatype


class interna(qsatype.objetoBase):

    ctx = qsatype.Object()

    def __init__(self, context=None):
        self.ctx = context


# @class_declaration elganso_crm #
from YBLEGACY.constantes import *


class elganso_crm(interna):

    def elganso_crm_getDesc(self):
        return None

    def elganso_crm_dameTemplateFiltro(self, model):
        urlBase = '/crm/crm_filtroscampana/' + str(model.pk)
        urlMod = ""

        if model.tipofiltro == 'Tiendas':
            urlMod = '/tiendas_filtroscampana'
        elif model.tipofiltro == 'Fecha de Compra':
            urlMod = '/fecha_filtroscampana'
        elif model.tipofiltro == 'Importe':
            urlMod = '/cantidad_filtroscampana'
        elif model.tipofiltro == 'Cantidad':
            urlMod = '/cantidad_filtroscampana'
        elif model.tipofiltro == 'País':
            urlMod = '/paises_filtroscampana'
        elif model.tipofiltro == 'Edad':
            urlMod = '/cantidad_filtroscampana'
        elif model.tipofiltro == 'Género':
            urlMod = '/genero_filtroscampana'
        elif model.tipofiltro == 'Familias':
            urlMod = '/familias_filtroscampana'
        elif model.tipofiltro == 'Artículo':
            urlMod = '/articulo_filtroscampana'
        elif model.tipofiltro == 'Ciudad':
            urlMod = '/ciudades_filtroscampana'
        elif model.tipofiltro == 'GruposModa':
            urlMod = '/gruposmoda_filtroscampana'
        elif model.tipofiltro == 'Talla':
            urlMod = '/talla_filtroscampana'
        elif model.tipofiltro == 'Nº Tickets':
            urlMod = '/ntickets_filtroscampana'
        elif model.tipofiltro == 'Fecha Alta Tarjeta':
            urlMod = '/fechaalta_filtroscampana'
        else:
            return True

        return urlBase + urlMod

    def elganso_crm_insertaListas(self, model, oParam):
        if 'selecteds' in oParam:
            curFC = qsatype.FLSqlCursor(u"crm_filtroscampana")
            curFC.select(ustr(u"idfiltro = ", model.idfiltro, ""))
            if curFC.first():
                curFC.setModeAccess(curFC.Edit)
                curFC.refreshBuffer()
                curFC.setValueBuffer("listaselect", oParam['selecteds'])
            else:
                print("fallo cursor")
                return False
            if not curFC.commitBuffer():
                print("commit fallo")
                return False

        if 'genero' in oParam:
            curFC = qsatype.FLSqlCursor(u"crm_filtroscampana")
            curFC.select(ustr(u"idfiltro = ", model.idfiltro, ""))
            if curFC.first():
                curFC.setModeAccess(curFC.Edit)
                curFC.refreshBuffer()
                curFC.setValueBuffer("genero", oParam['genero'])
            else:
                print("fallo cursor")
                return False
            if not curFC.commitBuffer():
                print("commit fallo")
                return False

        return True

    def elganso_crm_queryGrid_filtroCiudades(self, model, filters=None):
        query = {}
        query["tablesList"] = u""
        query["selectcount"] = u"COUNT(DISTINCT in_h_clientescrm.d_ciudad) as count"
        query["select"] = u"DISTINCT(in_h_clientescrm.d_ciudad)"
        query["from"] = u"in_h_clientescrm"
        query["where"] = u"1 = 1"
        query["orderby"] = "in_h_clientescrm.d_ciudad"
        query["database"] = "elgansobi"

        # if where:
        #     query["where"] = where

        return query

    def __init__(self, context=None):
        super().__init__(context)

    def getDesc(self):
        return self.ctx.elganso_crm_getDesc()

    def dameTemplateFiltro(self, model):
        return self.ctx.elganso_crm_dameTemplateFiltro(model)

    def insertaListas(self, model, oParam):
        return self.ctx.elganso_crm_insertaListas(model, oParam)

    def queryGrid_filtroCiudades(self, model, filters=None):
        return self.ctx.elganso_crm_queryGrid_filtroCiudades(model, filters)


# @class_declaration head #
class head(elganso_crm):

    def __init__(self, context=None):
        super().__init__(context)


# @class_declaration ifaceCtx #
class ifaceCtx(head):

    def __init__(self, context=None):
        super().__init__(context)


# @class_declaration FormInternalObj #
class FormInternalObj(qsatype.FormDBWidget):
    def _class_init(self):
        self.iface = ifaceCtx(self)
