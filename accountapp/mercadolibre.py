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

"""
Archivo que se ejecuta una vez por dia.
Para recolectar datos de Mercado libre.
Tarea realizada en pythonanywhere
diariamente

"""
# Recolecto la info de la cuenta principal y almaceno a la base de dato

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

fecha_ayer = ultimo_ingreso + timedelta(days=1)

fecha = str(fecha_ayer.year) + "-0" + \
    str(fecha_ayer.month) + "-" + str(fecha_ayer.day)


desde = fecha + "T00:00:00.000-00:00"
hasta = fecha + "T23:59:00.000-00:00"


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

except:
    pass

# Almaceno Access Token
tok = str("Bearer ") + api_response.get("access_token")
headers = {"Authorization": tok}
url = "https://api.mercadolibre.com/sites/MLA/search?nickname=VINOTECA+BARI"
res = requests.get(url, headers=headers).json()
conteo = res['paging']['total']

url = "https://api.mercadolibre.com/orders/search?seller=184827283&order.date_created.from=" + \
    desde + "&order.date_created.to=" + hasta


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


for i in range(0, len(publicaciones)):
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    titulo = results[i]['payments'][0]['reason']
    total = results[i]['payments'][0]['total_paid_amount']

    sql_insert = "INSERT INTO ventas (fecha, producto, importe) values (?, ?, ?);"
    sql_datos = (fecha, titulo, total)
    c.execute(sql_insert, sql_datos)
    conn.commit()
    conn.close()


con = sqlite3.connect('db.sqlite3')
cursorObj = con.cursor()

cursorObj.execute('SELECT * FROM competidores')
competidores = cursorObj.fetchall()

fecha_hoy = datetime.datetime.now()
fecha = str(fecha_hoy.year) + "-" + \
    str(fecha_hoy.month) + "-" + str(fecha_hoy.day)

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

except:
    pass

tok = str("Bearer ") + api_response.get("access_token")
headers = {"Authorization": tok}

for a in range(0, len(competidores)):

    # Creo Tabla sino existe

    sql_create = "CREATE TABLE IF NOT EXISTS " + \
        "'" + str(competidores[a][1]) + "'"
    base = """(id integer ,title text NOT NULL,fecha text,price integer,available_quantity,sold_quantity integer);"""
    sql_final = sql_create + base
    con.execute(sql_final)

    # Almaceno publicaciones
    url = "https://api.mercadolibre.com/sites/MLA/search?nickname=" + \
        str(competidores[a][1])
    res = requests.get(url, headers=headers).json()
    conteo = res['paging']['total']
    indic = 0

    for e in range(0, conteo, 50):
        url = "https://api.mercadolibre.com/sites/MLA/search?nickname=" + str(competidores[a][1]) + \
            "&offset=" + str(e)

        res = requests.post(url, headers=headers).json()
        results = res["results"]

        for i in range(0, len(results)):
            id_ml = results[i]['id']
            title = results[i]['title']
            fecha = fecha
            price = results[i]['price']
            cantidad = results[i]['available_quantity']
            vendidas = results[i]['sold_quantity']

            conn = sqlite3.connect('db.sqlite3')
            c = conn.cursor()
            sql_insert = "INSERT INTO " + "'" + \
                str(competidores[a][1]) + "'" + \
                " (id, title, fecha, price, available_quantity,sold_quantity) values (?, ?, ?, ?, ?, ?);"
            sql_datos = (id_ml, title, fecha, price, cantidad, vendidas)
            c.execute(sql_insert, sql_datos)

            conn.commit()
            conn.close()
            indic = + 1
            print(str(competidores[a][1]), conteo)

# Almaceno en la base de datos todas las ventas diarias para comparar


fecha_actual = datetime.datetime.now()

fecha = str(fecha_actual.year) + "-" + \
    str(fecha_actual.month) + "-" + str(fecha_actual.day)

fecha_ayer = fecha_actual - timedelta(days=1)

fecha_anterior = str(fecha_ayer.year) + "-" + \
    str(fecha_ayer.month) + "-" + str(fecha_ayer.day)


con = sqlite3.connect('db.sqlite3')
cursorObj = con.cursor()

cursorObj.execute('SELECT * FROM competidores')
competidores = cursorObj.fetchall()

for x in range(0, len(competidores)):

    select = "SELECT * FROM " + "'" + str(competidores[x][1] + "'")
    cursorObj.execute(select)
    user = cursorObj.fetchall()

    ventas_hoy = []
    ventas_ayer = []

    for i in range(0, len(user)):

        while user[i][2] == fecha_anterior:
            ventas_ayer.append(user[i])
            break

        while user[i][2] == fecha:
            ventas_hoy.append(user[i])
            break

    dia_1 = []

    for i in range(0, len(ventas_hoy)):
        ml = ventas_hoy[i][0]
        titulo = ventas_hoy[i][1]
        precio = ventas_hoy[i][3]
        cantidad = ventas_hoy[i][4]
        cant_vendi = ventas_hoy[i][5]
        for a in range(0, len(ventas_ayer)):
            if ml == ventas_ayer[a][0]:
                if cant_vendi != ventas_ayer[a][5]:
                    ventas = cant_vendi - ventas_ayer[a][5]
                    dia_1.append([titulo, precio, ventas])

    unidades_vendidas = 0
    facturacion = 0
    cantidad = len(dia_1)
    for i in range(0, len(dia_1)):
        unidades_vendidas += dia_1[i][2]
        tot = dia_1[i][1] * dia_1[i][2]
        facturacion += tot

    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    sql_insert = "INSERT INTO analisis (competidor, fecha, unidades_vendidas, cantidad_ventas,facturacion) values (?, ?, ?, ?, ?);"
    sql_datos = (competidores[x][1], fecha,
                 unidades_vendidas, cantidad, facturacion)
    c.execute(sql_insert, sql_datos)

    conn.commit()
    conn.close()


""" ALmaceno los datos de la cuenta principal y
    las guardos en la base de datos para comparar
"""

fecha_actual = datetime.datetime.now()

fecha = str(fecha_actual.year) + "-" + \
    str(fecha_actual.month) + "-" + str(fecha_actual.day)

fecha_ayer = fecha_actual - timedelta(days=1)

fecha_anterior = str(fecha_ayer.year) + "-0" + \
    str(fecha_ayer.month) + "-" + str(fecha_ayer.day)

con = sqlite3.connect('db.sqlite3')
cursorObj = con.cursor()
indice = "SELECT * FROM ventas where fecha = " + "'" + fecha_anterior + "'"
cursorObj.execute(indice)

rows = cursorObj.fetchall()
total = 0
for i in range(0, len(rows)):
    total_ventas = len(rows)
    unidades_ventas = total_ventas * 13
    total += rows[i][3]

conn = sqlite3.connect('db.sqlite3')
c = conn.cursor()
sql_insert = "INSERT INTO analisis (competidor, fecha, unidades_vendidas, cantidad_ventas,facturacion) values (?, ?, ?, ?, ?);"
sql_datos = ("Vinoteca Bari", fecha,
             unidades_ventas, total_ventas, total)
c.execute(sql_insert, sql_datos)


conn.commit()
conn.close()
