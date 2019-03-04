from YBLEGACY import qsatype
from AQNEXT.celery import app
from YBUTILS import notifications
from YBLEGACY.constantes import *
import hashlib
import time


@app.task
def sendPostRequest(obj):
    resul = notifications.post_request(obj['endpoint'], obj['header'], obj['data'])
    if not resul:
        qsatype.debug("Error " + obj['data']['contact'])
    elif "success" in resul and not resul['success']:
        qsatype.debug("Error " + obj['data']['contact'])
    else:
        qsatype.debug(ustr("Email sincronizado", resul, obj['data']['contact']))


@app.task
def publicarCampana(obj):
    # ------Datos salesmanago---------
    clientId = '409m1j5tggvfrpsx'
    apiKey = '123loquesea321'
    apiSecret = 'r7qcegeijs94lpsbmgg2kpqixx1q7kvd'
    endpoint = 'www.salesmanago.pl'
    # endpoint = 'dev.yeboyebo.es'
    owner = 'salesmanago@elganso.com'
    # --------------------------------

    # Hash key
    hasstr = apiKey + clientId + apiSecret
    sha = hashlib.sha1()
    sha.update(hasstr.encode('utf-8'))

    # Datos destinatarios
    where = obj['where']
    where += " GROUP BY in_h_clientescrm.d_nombre, in_h_clientescrm.d_email, in_h_clientescrm.d_telefono, in_h_clientescrm.d_codtarjetapuntos"

    query = qsatype.FLSqlQuery("qryDestinatarios", "elgansobi")
    query.setTablesList(u"in_h_ventascrm,in_h_clientescrm")
    query.setSelect(u"DISTINCT in_h_clientescrm.d_nombre as Nombre, in_h_clientescrm.d_email as Email, in_h_clientescrm.d_telefono as Telefono, in_h_clientescrm.d_codtarjetapuntos as Tarjeta")
    query.setFrom(u"in_h_ventascrm INNER JOIN in_h_clientescrm ON in_h_ventascrm.d_mailcliente = in_h_clientescrm.d_email")
    query.setWhere(where)

    if not query.exec_():
        qsatype.debug("Campaña " + obj['campana'] + " error consulta")

    data = {}
    data['clientId'] = clientId
    data['apiKey'] = apiKey
    data['requestTime'] = str(qsatype.Date())
    data['sha'] = sha.hexdigest()
    data['upsertDetails'] = []
    data['owner'] = owner
    # -----Request Header-------------
    header = {
        "Content-Type": "application/json",
        "Content-Length": str(len(str(data)))
    }
    i = 0
    perdidos = []
    while query.next():
        upsertDetails = {}
        upsertDetails['contact'] = {}
        upsertDetails['contact']['email'] = query.value('email')
        upsertDetails['contact']['name'] = query.value('nombre')
        upsertDetails['contact']['phone'] = query.value('telefono')
        upsertDetails['tags'] = [obj['campana']]
        # upsertDetails['removeTags'] = ["ES_ESPAÑA"]
        # upsertDetails['contact']['email'] = "javier.yeboyebo@gmail.com"
        data['upsertDetails'].append(upsertDetails)
        i = i + 1
        if i == 600:
            # resul = notifications.post_request('https://' + endpoint + '/models/REST/factrascli/csr/pruebacsr', header, data)
            resul = notifications.post_request('http://' + endpoint + '/api/contact/batchupsert', header, data)
            i = 0
            if not resul:
                qsatype.debug(ustr("Error", resul, i))
                perdidos.append(data['upsertDetails'])
            elif "success" in resul and not resul['success']:
                qsatype.debug(ustr("Error", resul, i))
                perdidos.append(data['upsertDetails'])
            else:
                qsatype.debug(ustr("Sincronizado"))
            data['upsertDetails'] = []

    # -----Peticion POST--------------
    if i > 0:
        # resul = notifications.post_request('https://' + endpoint + '/models/REST/facturascli/csr/pruebacsr', header, data)
        resul = notifications.post_request('http://' + endpoint + '/api/contact/batchupsert', header, data)
        if not resul:
            qsatype.debug(ustr("Error", resul, i))
            perdidos.append(data['upsertDetails'])
        elif "success" in resul and not resul['success']:
            qsatype.debug(ustr("Error", resul, i))
            perdidos.append(data['upsertDetails'])
        else:
            qsatype.debug(ustr("Sincronizado"))

    if len(perdidos) > 0:
        time.sleep(180)
        for upsert in perdidos:
            data['upsertDetails'] = upsert
            resul = notifications.post_request('http://' + endpoint + '/api/contact/batchupsert', header, data)
            time.sleep(60)
            if not resul:
                qsatype.debug(ustr("Error", resul))
            elif "success" in resul and not resul['success']:
                qsatype.debug(ustr("Error", resul))
            else:
                qsatype.debug(ustr("Sincronizado"))

    qsatype.debug("Campaña " + obj['campana'] + " todo Ok")
