from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required


from django.contrib import messages
from django.contrib.auth.models import User
import meli
from meli.rest import ApiException
import json
import requests
from datetime import date
from datetime import datetime
from .views2 import *
from .views_home import *


def registerPage(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')

    context = {'form': form}
    return render(request, 'register.html', context)


def loginPage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'username or password is incorrect')

    context = {}
    return render(request, 'login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def homepage(request):
    username = "sebas"
    context = {'username': username}
    datos = [1000, 2000, 3000, 4000, 5000, 6000, 7000]

    hoy = date.today()
    dia = str(hoy.year) + "-" + str(hoy.month) + "-" + \
        str(hoy.day) + "T00:00:00.000-00:00"

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

    # try:
        api_response = api_instance.get_token(grant_type=grant_type, client_id=client_id,
                                              client_secret=client_secret, redirect_uri=redirect_uri, code=code, refresh_token=refresh_token)

    # except:
    #   pass

    # Almaceno Access Token
    tok = str("Bearer ") + api_response.get("access_token")

    url = "https://api.mercadolibre.com/orders/search?seller=184827283&order.date_created.from=" + dia

    headers = {"Authorization": tok}

    res = requests.get(url, headers=headers).json()
    results = res["results"]

    ventas_diarias = len(results)
    facturacion = []

    for i in range(0, len(results)):
        facturacion.append(results[i]['total_amount'])

    total = sum(facturacion)
    cant = len(facturacion)
    promedio = round(total / cant)

    return render(request, 'home.html', locals())
