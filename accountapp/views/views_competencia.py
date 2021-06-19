from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import meli
import json
import requests
import sqlite3
from meli.rest import ApiException
import datetime
from datetime import date, timedelta


@login_required(login_url='login')
def competencia(request):

    con = sqlite3.connect('db.sqlite3')
    cursorObj = con.cursor()

    cursorObj.execute('SELECT NICK FROM competidores')
    competidores = cursorObj.fetchall()
    a1 = competidores[0][0]
    a2 = competidores[1][0]
    a3 = competidores[2][0]
    user = "Vinoteca Bari"

    todos = [user, a1, a2, a3]

    # Almaceno los ultimos 7 dias
    fecha_hoy = datetime.datetime.now()
    dias_7 = []
    dicdias = {'MONDAY': 'Lun', 'TUESDAY': 'Mar', 'WEDNESDAY': 'Mier', 'THURSDAY': 'Jue',
               'FRIDAY': 'Vie', 'SATURDAY': 'Sab', 'SUNDAY': 'Dom'}
    ano, mes, dia = fecha_hoy.year, fecha_hoy.month, fecha_hoy.day

    fecha = datetime.date(ano, mes, dia)
    mes_actual = fecha_hoy.strftime("%b/%Y")

    almacenar_mes = str(ano) + "-" + str(mes)

    for i in range(1, 8):
        almacen = fecha - datetime.timedelta(days=i)
        dias_7.append(
            str(dicdias[almacen.strftime('%A').upper()]) + " " + str(almacen.day))

    dias_semanas = dias_7[::-1]

    cursorObj.execute('SELECT * FROM analisis')
    analisis = cursorObj.fetchall()

    principal, principal_ventas, principal_mensual = [], [], []
    user1_semana, user1_ventas, user1_mensual = [], [], []
    user2_semana, user2_ventas, user2_mensual = [], [], []
    user3_semana, user3_ventas, user3_mensual = [], [], []

    for i in range(0, len(analisis)):

        if str(analisis[i][0]) == user and str(almacenar_mes) in str(analisis[i][1]):
            principal_mensual.append(analisis[i][4])

        if str(analisis[i][0]) == a1 and str(almacenar_mes) in str(analisis[i][1]):
            user1_mensual.append(analisis[i][4])

        if str(analisis[i][0]) == a2 and str(almacenar_mes) in str(analisis[i][1]):
            user2_mensual.append(analisis[i][4])

        if str(analisis[i][0]) == a3 and str(almacenar_mes) in str(analisis[i][1]):
            user3_mensual.append(analisis[i][4])

    cursorObj.execute('SELECT * FROM analisis')
    analisis = cursorObj.fetchall()

    principal = []
    principal_ventas = []
    user1_semana = []
    user1_ventas = []
    user2_semana = []
    user2_ventas = []
    user3_semana = []
    user3_ventas = []

    fecha_hoy = datetime.datetime.now()

    for i in range(0, 7):
        fecha_ayer = fecha_hoy - timedelta(days=i)
        fecha = str(fecha_ayer.year) + "-" + \
            str(fecha_ayer.month) + "-" + str(fecha_ayer.day)

        for a in range(0, len(analisis)):
            if user == analisis[a][0] and fecha == analisis[a][1]:
                principal.append(round(analisis[a][4]))
                principal_ventas.append(analisis[a][3])

            if a1 == analisis[a][0] and fecha == analisis[a][1]:
                user1_semana.append(round(analisis[a][4]))
                user1_ventas.append(analisis[a][3]*10)

            if a2 == analisis[a][0] and fecha == analisis[a][1]:
                user2_semana.append(round(analisis[a][4]))
                user2_ventas.append(analisis[a][3]*10)

            if a3 == analisis[a][0] and fecha == analisis[a][1]:
                user3_semana.append(round(analisis[a][4]))
                user3_ventas.append(analisis[a][3]*10)

    user_01 = [round(sum(principal))]
    a1_total = [round(sum(user1_semana))]
    a2_total = [round(sum(user2_semana))]
    a3_total = [round(sum(user3_semana))]

    return render(request, 'competencia.html', locals())
