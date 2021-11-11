# @class_declaration elganso_crm #
from YBLEGACY.constantes import *
from crm import tasks
from YBUTILS import notifications
import time

class elganso_crm(flcrm_mark):

    def elganso_crm_getForeignFields(self, model, template=None):
        return []

    def elganso_crm_getFilters(self, model, name, template=None):
        return []

    def elganso_crm_initValidation(self, name, data):
        response = True
        return response

    def elganso_crm_iniciaValoresLabel(self, model, template=None):
        labels = {}
        labels[u"recuentoDestinatarios"] = "Destinatarios: No hay destinatarios, pulse botón de recontar"
        return labels

    def elganso_crm_bChLabel(self, fN=None, cursor=None):
        # _i = self.iface

        labels = {}
        # if fN == u"recuentoDestinatarios":
        #     labels[u"recuentoDestinatarios"] = "Destinatarios: " + str(_i.recontarDestinatarios(cursor))

        return labels

    def elganso_crm_publicarPromocionCampana(self, model, oParam):
        curCampana = qsatype.FLSqlCursor(u"crm_campanas")
        curCampana.select(ustr(u"codcampana = '", codcampana, u"'"))

        if curCampana.first():
            # TODO: recoger param 'solosuscritos' y si True, añadir al where ' AND in_h_clientescrm.suscrito'
            return qsatype.FactoriaModulos.get('formRecordcrm_campanas').iface.publicarPromocionCampana(curCampana, oParam)

        return False

        # if cursor.valueBuffer(u'codpromocion'):
        #     curPromocion = qsatype.FLSqlCursor(u"eg_promospersonales")
        #     curPromocion.select(ustr(u"codpromocion = '", cursor.valueBuffer(u'codpromocion'), "'"))

        #     if not curPromocion.first():
        #         print("error codpromocion")
        #         return False

        #     if not curPromocion.valueBuffer(u"publicada"):
        #         if self.iface.insertarPromoPuntosComanda(cursor, curPromocion):
        #             curPromocion.setValueBuffer(u"publicada", True)
        #             if not curPromocion.commitBuffer():
        #                 print("error curpromocion")
        #                 return False
        #             return True

        # return False

    def elganso_crm_generaCSVDestinatarios(self, cursor=None, params=None):
        _i = self.iface

        queryParams = qsatype.Object()
        # Web / App
        if cursor.valueBuffer(u"canal") == 'Email':
            queryParams[u'columns'] = qsatype.Array([u'nombre', u'email', u'ntickets'])
        elif cursor.valueBuffer(u"canal") == "SMS":
            queryParams[u'columns'] = qsatype.Array([u'nombre', u'telefono', u'ntickets'])
        else:
            queryParams[u'columns'] = qsatype.Array([u'nombre', u'email', u'telefono', u'ntickets'])

        soloSuscritos = True if params and "solosuscritos" in params and (params["solosuscritos"] == "true" or params["solosuscritos"] is True) else False
        soloFidelizados = True if params and "solofidelizados" in params and (params["solofidelizados"] == "true" or params["solofidelizados"] is True) else False

        where = _i.dameWhereFiltros(cursor.valueBuffer(u"codcampana"), cursor.valueBuffer(u"canal"), soloSuscritos, soloFidelizados)
        where += " GROUP BY in_h_clientescrm.d_nombre, in_h_clientescrm.d_email, in_h_clientescrm.d_telefono, in_h_clientescrm.d_codtarjetapuntos"
        where += _i.dameHavingFiltros(cursor.valueBuffer("codcampana"), cursor.valueBuffer(u"canal"))

        sSelect = "DISTINCT in_h_clientescrm.d_nombre as nombre, in_h_clientescrm.d_email as email, in_h_clientescrm.d_telefono as telefono, in_h_clientescrm.d_codtarjetapuntos as tarjeta, 0 AS ntickets"
        sFrom = "in_h_clientescrm"
        if where.find("in_h_ventascrm") > 0:
            sSelect = "DISTINCT in_h_clientescrm.d_nombre as nombre, in_h_clientescrm.d_email as email, in_h_clientescrm.d_telefono as telefono, in_h_clientescrm.d_codtarjetapuntos as tarjeta, COUNT(DISTINCT(in_h_ventascrm.d_codcomanda)) AS ntickets"
            sFrom = "in_h_clientescrm INNER JOIN in_h_ventascrm ON in_h_ventascrm.d_mailcliente = in_h_clientescrm.d_email"

        q = qsatype.FLSqlQuery("qryDestinatarios", "elgansobi")
        q.setTablesList(u"in_h_ventascrm, in_h_clientescrm")
        q.setSelect(sSelect)
        q.setFrom(sFrom)
        q.setWhere(where)

        if not q.exec_():
            return False
        if q.size() == 0:
            return False

        queryParams[u'query'] = q
        return queryParams

    def elganso_crm_dameWhereFiltros(self, codcampana=None, canal=None, soloSuscritos=False, soloFidelizados=False):
        curFiltros = qsatype.FLSqlCursor(u"crm_filtroscampana")
        curFiltros.select(ustr(u"codcampana = '", codcampana, u"'"))
        where = u"1 = 1"

        if canal == u"SMS":
            where = u"in_h_clientescrm.d_telefono IS NOT NULL AND in_h_clientescrm.d_telefono not in ('0','.',',','*','-')"
        elif canal == u"Email":
            where = u"in_h_clientescrm.d_email IS NOT NULL AND in_h_clientescrm.d_email not in ('0','.',',','*','-')"
        elif canal == u"Web / App":
            where = u"in_h_clientescrm.d_email IS NOT NULL AND in_h_clientescrm.d_email not in ('0','.',',','*','-')"

        if soloSuscritos:
            where += " AND in_h_clientescrm.d_suscrito"

        if soloFidelizados:
            where += " AND d_codtarjetapuntos is not null"

        while curFiltros.next():
            if curFiltros.valueBuffer(u"wherefiltro"):
                where += curFiltros.valueBuffer(u"wherefiltro")

        where += " AND in_h_clientescrm.d_nombre not in ('0','.',',','*','-')"
        qsatype.debug("wherefiltro")
        qsatype.debug(where)
        return where

    def elganso_crm_dameHavingFiltros(self, codcampana=None, canal=None):
        curFiltros = qsatype.FLSqlCursor(u"crm_filtroscampana")
        curFiltros.select(ustr(u"codcampana = '", codcampana, u"'"))
        having = u" HAVING 1 = 1"

        while curFiltros.next():
            if curFiltros.valueBuffer(u"havingfiltro"):
                having += curFiltros.valueBuffer(u"havingfiltro")

        return having

    def elganso_crm_recontarDestinatarios(self, cursor, soloSuscritos=False, soloFidelizados=False):
        _i = self.iface

        where = _i.dameWhereFiltros(cursor.valueBuffer(u"codcampana"), cursor.valueBuffer(u"canal"), soloSuscritos, soloFidelizados)
        where += " GROUP BY in_h_clientescrm.d_nombre, in_h_clientescrm.d_email, in_h_clientescrm.d_telefono, in_h_clientescrm.d_codtarjetapuntos"
        where += _i.dameHavingFiltros(cursor.valueBuffer("codcampana"), cursor.valueBuffer(u"canal"))

        sFrom = "in_h_clientescrm"
        if where.find("in_h_ventascrm") > 0:
            sFrom = "in_h_clientescrm INNER JOIN in_h_ventascrm ON in_h_ventascrm.d_mailcliente = in_h_clientescrm.d_email"

        q = qsatype.FLSqlQuery("qryRecontar", "elgansobi")
        q.setTablesList(u"in_h_ventascrm, in_h_clientescrm")
        q.setSelect(u"count(*)")
        q.setFrom(sFrom)
        q.setWhere(where)
        print(where) 
        if not q.exec_():
            return False
        return q.size()

    def elganso_crm_insertarPromoPuntosComanda(self, model, cursor, curPromocion):
        _i = self.iface

        where = _i.dameWhereFiltros(cursor.valueBuffer(u"codcampana"), cursor.valueBuffer(u"canal"))
        where += " GROUP BY in_h_clientescrm.d_nombre, in_h_clientescrm.d_email, in_h_clientescrm.d_telefono, in_h_clientescrm.d_codtarjetapuntos"
        where += _i.dameHavingFiltros(cursor.valueBuffer("codcampana"), cursor.valueBuffer(u"canal"))

        q = qsatype.FLSqlQuery("qryPromoPuntos", "elgansobi")
        q.setTablesList(u"in_h_ventascrm, in_h_clientescrm")
        q.setSelect(u"in_h_clientescrm.d_nombre, in_h_clientescrm.d_email, in_h_clientescrm.d_telefono, in_h_clientescrm.d_codtarjetapuntos")
        q.setFrom(u"in_h_ventascrm INNER JOIN in_h_clientescrm ON in_h_ventascrm.d_mailcliente = in_h_clientescrm.d_email")
        q.setWhere(where)
        if not q.exec_():
            return False

        while q.next():
            sql = "INSERT INTO tpv_eg_promopuntoscomanda (tipopromo, codbarrastarjeta, activa, codpromocion, email) VALUES ('" + curPromocion.valueBuffer(u"codtipopromocion") + "', '" + q.value(u"d_codtarjetapuntos") + "', false, '" + cursor.valueBuffer(u"codpromocion") + "', '" + q.value(u"d_email") + "')"
            qsatype.FLSqlQuery().execSql(sql)

        return True

    def elganso_crm_sendSalesApi(self, model, params, cursor):
        _i = self.iface

        # Where destinatarios
        soloSuscritos = True if params and "solosuscritos" in params and (params["solosuscritos"] == "true" or params["solosuscritos"] is True) else False
        soloFidelizados = True if params and "solofidelizados" in params and (params["solofidelizados"] == "true" or params["solofidelizados"] is True) else False
        where = _i.dameWhereFiltros(cursor.valueBuffer(u"codcampana"), cursor.valueBuffer(u"canal"), soloSuscritos, soloFidelizados)
        obj = {}
        obj['where'] = where
        obj['campana'] = model.descripcion
        tasks.publicarCampana.delay(obj)
        return True

    def elganso_crm_iniciaValoresCursor(self, cursor=None):
        _i = self.iface

        date = str(qsatype.Date())
        cursor.setValueBuffer(u"codcampana", _i.obtenerCodigoCampana(cursor))
        cursor.setValueBuffer(u"fechainicio", date[:10])

    def elganso_crm_obtenerCodigoCampana(self, cursor=None):
        return qsatype.FLUtil().nextCounter(u"codcampana", cursor)

    def __init__(self, context=None):
        super(elganso_crm, self).__init__(context)

    def getForeignFields(self, model, template=None):
        return self.ctx.elganso_crm_getForeignFields(model, template)

    def getFilters(self, model, name, template=None):
        return self.ctx.elganso_crm_getFilters(model, name, template)

    def initValidation(self, name, data):
        return self.ctx.elganso_crm_initValidation(name, data)

    def iniciaValoresLabel(self, model=None, template=None, cursor=None):
        return self.ctx.elganso_crm_iniciaValoresLabel(model, template)

    def bChLabel(self, fN=None, cursor=None):
        return self.ctx.elganso_crm_bChLabel(fN, cursor)

    def publicarPromocionCampana(self, model, oParam):
        return self.ctx.elganso_crm_publicarPromocionCampana(model, oParam)

    def sendSalesApi(self, model, oParam, cursor):
        return self.ctx.elganso_crm_sendSalesApi(model, oParam, cursor)

    def generaCSVDestinatarios(self, cursor=None, params=None):
        return self.ctx.elganso_crm_generaCSVDestinatarios(cursor, params)

    def dameWhereFiltros(self, codcampana=None, canal=None, soloSuscritos=False, soloFidelizados=False):
        return self.ctx.elganso_crm_dameWhereFiltros(codcampana, canal, soloSuscritos, soloFidelizados)

    def dameHavingFiltros(self, codcampana=None, canal=None):
        return self.ctx.elganso_crm_dameHavingFiltros(codcampana, canal)

    def recontarDestinatarios(self, cursor, soloSuscritos=False, soloFidelizados=False):
        return self.ctx.elganso_crm_recontarDestinatarios(cursor, soloSuscritos, soloFidelizados)

    def insertarPromoPuntosComanda(self, model, cursor, curPromocion):
        return self.ctx.elganso_crm_insertarPromoPuntosComanda(model, cursor, curPromocion)

    def iniciaValoresCursor(self, cursor=None):
        return self.ctx.elganso_crm_iniciaValoresCursor(cursor)

    def obtenerCodigoCampana(self, cursor=None):
        return self.ctx.elganso_crm_obtenerCodigoCampana(cursor)
