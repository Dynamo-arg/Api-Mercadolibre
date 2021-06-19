from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.template.defaulttags import register


import meli
import json
import requests
import sqlite3
from meli.rest import ApiException


@login_required(login_url='login')
def tendencias(request):

    # Recolecto info de las tendencias MERCADO LIBRE
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
    url = "https://api.mercadolibre.com/trends/MLA"
    res = requests.get(url, headers=headers).json()

    link = []
    key = []

    for i in range(0, 11):
        key.append(res[i]['keyword'])
        link.append(res[i]['url'])

    url = "https://api.mercadolibre.com/sites/MLA/categories"
    res = requests.get(url, headers=headers).json()

    id_categoria = []
    categoria = []
    links = []

    for i in range(0, len(res)):

        id_categoria.append(res[i]['id'])
        categoria.append(res[i]['name'])
        url = "https://api.mercadolibre.com/trends/MLA/" + id_categoria[i]
        resultados = requests.get(url, headers=headers).json()

        for a in range(0, 10):
            try:
                links.append(resultados[a]['keyword'])
            except:
                links.append("-")

    return render(request, 'tendencias.html', locals())
