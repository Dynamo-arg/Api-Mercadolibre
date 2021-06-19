from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

import meli
import requests
import sqlite3
import datetime


@login_required(login_url='login')
def homepage(request):
    username = "sebas"
    context = {'username': username}

    con = sqlite3.connect('db.sqlite3')
    cursorObj = con.cursor()

    datos = []
    datos_anual = []

    cursorObj.execute(
        'SELECT * FROM ventas WHERE ROWID IN (SELECT max(ROWID) FROM ventas)')

    rows = cursorObj.fetchall()

    ultimo_ingreso = datetime.date(
        int(rows[0][1][0:4]),
        int(rows[0][1][5:7]),
        int(rows[0][1][8:10])
    )
    anio = cursorObj.fetchall()

    # obtengo los ultimos 7 dias
    for i in range(1, 8):

        if len(str(ultimo_ingreso.month)) == 1:
            mes = "-0" + str(ultimo_ingreso.month)
        else:
            mes = "0" + str(ultimo_ingreso.month)

        if len(str(ultimo_ingreso.day)) == 1:
            dia = "-0" + str(ultimo_ingreso.day)
        else:
            dia = "-" + str(ultimo_ingreso.day)

        dias_7 = "'"+str(ultimo_ingreso.year) + mes + dia + "'"
        select = "SELECT * FROM ventas WHERE fecha =" + dias_7
        cursorObj.execute(select)
        rows = cursorObj.fetchall()
        parcial = []

        for a in range(0, len(rows)):
            parcial.append(rows[a][3])

        datos.append(int(sum(parcial)))

        ultimo_ingreso = ultimo_ingreso - datetime.timedelta(days=i)

    # Obtengo los ultimos meses
    cursorObj.execute(
        'SELECT * FROM ventas WHERE ROWID IN (SELECT max(ROWID) FROM ventas)')
    anio = cursorObj.fetchall()
    for i in range(1, 13):
        parcial = []
        if len(str(i)) == 1:
            mes = "0" + str(i)
        else:
            mes = str(i)

        ultimo = "'%" + anio[0][1][0:4] + "-" + mes + "%'"

        select = "SELECT importe, fecha FROM ventas WHERE fecha LIKE  " + ultimo
        cursorObj.execute(select)
        rows = cursorObj.fetchall()
        for x in range(len(rows)):
            parcial.append(rows[x][0])

        datos_anual.append(int(sum(parcial)))

    # Obtengo Fecha de hoy y alamceno X Y
    fecha_hoy = datetime.datetime.now()
    dias_7 = []
    dicdias = {'MONDAY': 'Lun', 'TUESDAY': 'Mar', 'WEDNESDAY': 'Mier', 'THURSDAY': 'Jue',
               'FRIDAY': 'Vie', 'SATURDAY': 'Sab', 'SUNDAY': 'Dom'}
    ano, mes, dia = fecha_hoy.year, fecha_hoy.month, fecha_hoy.day

    fecha = datetime.date(ano, mes, dia)

    for i in range(1, 8):
        almacen = fecha - datetime.timedelta(days=i)
        dias_7.append(
            str(dicdias[almacen.strftime('%A').upper()]) + " " + str(almacen.day))

    dias_semanas = dias_7[::-1]

    # Guardo variables para parametros semana ML

    dia = str(ano) + "-" + str(mes) + "-" + \
        str(dia) + "T00:00:00.000-00:00"

    configuration = meli.Configuration(
        host="https://api.mercadolibre.com"
    )

    with meli.ApiClient() as api_client:

        api_instance = meli.OAuth20Api(api_client)
        grant_type = 'refresh_token'  # or 'refresh_token' if you need get one new token
        client_id = ''  # Reemplazar CLIENT ID dado por la Api de mercado libre
        client_secret = ''  # Reemplazar CLIENT SECRET dado por la Api de mercado libre
        redirect_uri = 'https://mercadolibre.com.ar'
        code = ''  # The parameter CODE, empty if your send a refresh_token
        refresh_token = ''  # Copiar refresh_token obtenido cuando se logea

        api_response = api_instance.get_token(grant_type=grant_type, client_id=client_id,
                                              client_secret=client_secret, redirect_uri=redirect_uri, code=code, refresh_token=refresh_token)

    # Almaceno Access Token
    tok = str("Bearer ") + api_response.get("access_token")
    headers = {"Authorization": tok}
    url = "https://api.mercadolibre.com/sites/MLA/search?nickname=VINOTECA+BARI"
    res = requests.get(url, headers=headers).json()
    conteo = res['paging']['total']

    url = "https://api.mercadolibre.com/orders/search?seller=184827283&order.date_created.from=" + dia

    res = requests.get(url, headers=headers).json()
    results = res["results"]

    publicaciones = []
    for i in range(0, len(results)):

        publicaciones.append([
            results[i]['last_updated'][0:10],
            results[i]['buyer']['nickname'],
            results[i]['payments'][0]['reason'],
            results[i]['total_amount']
        ])

    ventas_diarias = len(results)
    facturacion = []

    for i in range(0, len(results)):
        facturacion.append(results[i]['total_amount'])

    total = int(sum(facturacion))
    cant = len(facturacion)
    promedio = round(total / cant)
    maximo = round(max(datos) * 1.35)
    anual_maximo = round(max(datos_anual) * 1.10)

    return render(request, 'home.html', locals())
