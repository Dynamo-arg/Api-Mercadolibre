from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import meli
import json
import requests
import sqlite3
import datetime
from meli.rest import ApiException
from datetime import date, timedelta

try:

    con = sqlite3.connect('db.sqlite3')
    cursorObj = con.cursor()

    cursorObj.execute(
        'SELECT * FROM ventas WHERE ROWID IN (SELECT max(ROWID) FROM ventas)')

    rows = cursorObj.fetchall()

    ultimo_ingreso = datetime.date(
        int(rows[0][1][0:4]),
        int(rows[0][1][5:7]),
        int(rows[0][1][8:10])
    )
    fecha_hoy = datetime.datetime.now()
    actual = datetime.date(fecha_hoy.year, fecha_hoy.month, fecha_hoy.day)
    indice = actual - ultimo_ingreso

    try:
        for i in range(1, int(indice.days)):
            almacen = fecha_hoy - datetime.timedelta(days=i)
            if datetime.date(
                almacen.year, almacen.month, almacen.day
            ) == ultimo_ingreso:
                break

            else:

                ano, mes, dia = almacen.year, almacen.month, almacen.day
                inicio = str(ano) + "-" + str(mes) + "-" + \
                    str(dia) + "T23:59:00.000-00:00"

                final = str(ano) + "-" + str(mes) + "-" + \
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

                try:
                    api_response = api_instance.get_token(grant_type=grant_type, client_id=client_id,
                                                          client_secret=client_secret, redirect_uri=redirect_uri, code=code, refresh_token=refresh_token)

                except ApiException as e:
                    print("Excepción al llamar OAuth20Api->get_token: %s\n" % e)

                    # Almaceno Access Token
                tok = str("Bearer ") + api_response.get("access_token")

                url = "https://api.mercadolibre.com/orders/search?seller=184827283&order.date_created.from=" + \
                    final + "&order.date_created.to=" + inicio

                headers = {"Authorization": tok}

                res = requests.get(url, headers=headers).json()
                conteo = res['paging']['total']

                for a in range(0, conteo, 50):
                    url = "https://api.mercadolibre.com/orders/search?seller=184827283&order.date_created.from=" + \
                        final + "&order.date_created.to=" + inicio + \
                        "&offset=" + str(a)
                    headers = {"Authorization": tok}
                    res = requests.get(url, headers=headers).json()
                    results = res["results"]

                    for x in range(0, len(results)):

                        precio = results[x]['payments'][0]['total_paid_amount']
                        titulo = results[x]['payments'][0]['reason']
                        fecha_ML = results[x]['payments'][0]['date_created']
                        fecha_base = str(fecha_ML[0:4])+"-"+str(fecha_ML[5:7])+"-" + str(fecha_ML[8:10]
                                                                                         )

                        conn = sqlite3.connect('db.sqlite3')
                        c = conn.cursor()

                        c.execute("insert into ventas (fecha, importe, producto) values (?, ?, ?)",
                                  (fecha_base, precio, titulo))

                        conn.commit()
                        # close the connection
                        conn.close()

    except:
        pass
except:
    pass
