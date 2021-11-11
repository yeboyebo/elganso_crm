# @class_declaration interna #
from YBLEGACY import qsatype


class interna(qsatype.objetoBase):

    ctx = qsatype.Object()

    def __init__(self, context=None):
        self.ctx = context


# @class_declaration elganso_crm #
from django.http import HttpResponse
from models.flfactppal.paises import paises
import csv


class elganso_crm(interna):

    def elganso_crm_getCSV(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="file.csv"'
        query = paises.objects.all()
        writer = csv.writer(response)

        columnas = []
        for field in paises._meta.fields:
            columnas.append(field.name)
        writer.writerow(columnas)

        for obj in query:
            row = []
            for field in columnas:
                val = getattr(obj, field)
                if callable(val):
                    val = val()
                if type(val) == 'unicode':
                    val = val.encode("utf-8")
                row.append(val)
            writer.writerow(row)

        return response

    def __init__(self, context=None):
        super(elganso_crm, self).__init__(context)

    def getCSV(self, request):
        return self.ctx.elganso_crm_getCSV(request)


# @class_declaration head #
class head(elganso_crm):

    def __init__(self, context=None):
        super(head, self).__init__(context)


# @class_declaration ifaceCtx #
class ifaceCtx(head):

    def __init__(self, context=None):
        super(ifaceCtx, self).__init__(context)


# @class_declaration FormInternalObj #
class FormInternalObj(qsatype.FormDBWidget):
    def _class_init(self):
        self.iface = ifaceCtx(self)
