# @class_declaration interna #
from YBLEGACY import qsatype
from YBLEGACY.constantes import *


class interna(qsatype.objetoBase):

    ctx = qsatype.Object()

    def __init__(self, context=None):
        self.ctx = context


# @class_declaration elganso_crm #
class elganso_crm(interna):

    def elganso_crm_formRecordcrm_campanas(self, fN, dict, prefix, pk):
        if fN == "recuentoDestinatarios":
            curCampana = qsatype.FLSqlCursor("crm_campanas")
            curCampana.select("codcampana='" + pk + "'")
            curCampana.first()
            curCampana.setModeAccess(curCampana.Browse)
            curCampana.refreshBuffer()
            from models.flcrm_mark.crm_campanas import crm_campanas
            suscritos = False
            if "solosuscritos" in dict["otros"]:
                suscritos = dict["otros"]["solosuscritos"]
            dest = crm_campanas.recontarDestinatarios(curCampana, suscritos)
            dict["labels"]["recuentoDestinatarios"] = "Destinatarios: " + str(dest)

            if dest > 0:
                if "groupBoxAcciones" not in dict["drawIf"]:
                    dict["drawIf"]["groupBoxAcciones"] = {}
                dict["drawIf"]["groupBoxAcciones"]["generaCSVButton"] = True
                dict["drawIf"]["groupBoxAcciones"]["salesButton"] = True

        return dict

    def __init__(self, context=None):
        super().__init__(context)

    def formRecordcrm_campanas(self, fN, dict, prefix, pk):
        return self.elganso_crm_formRecordcrm_campanas(fN, dict, prefix, pk)


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
