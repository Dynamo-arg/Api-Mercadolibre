from django.db import models
import meli
from meli.rest import ApiException
from pprint import pprint
import json
import requests
import os
from datetime import date
from datetime import datetime

class ML(models.Model):
    def mlhoy():

        hoy = date.today()
        dia = str(hoy.year) + "-" + str(hoy.month) + "-" + \
            str(hoy.day) + "T00:00:00.000-00:00"

        configuration = meli.Configuration(
            host="https://api.mercadolibre.com"
        )

        with meli.ApiClient() as api_client:

            api_instance = meli.OAuth20Api(api_client)
            grant_type = 'refresh_token'  # or 'refresh_token' if you need get one new token
            client_id = '1168054310416447'
            client_secret = 'kdxgHYxI8enxKZOVUdazyzq3VabrqD8D'
            redirect_uri = 'https://mercadolibre.com.ar'
            code = ''  # The parameter CODE, empty if your send a refresh_token
            refresh_token = 'TG-609bd7844b82520007fbb796-184827283'  # Your refresh_token

        try:
            api_response = api_instance.get_token(grant_type=grant_type, client_id=client_id,
                                                client_secret=client_secret, redirect_uri=redirect_uri, code=code, refresh_token=refresh_token)
            pprint(api_response)

        except ApiException as e:
            print("Excepción al llamar OAuth20Api->get_token: %s\n" % e)

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

        return (facturacion)



 
# Create your models here.
