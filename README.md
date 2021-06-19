# Analisis Mercado Libre http://dynamoarg.pythonanywhere.com/

App creada para monitorear sus datos de Mercado libre, sus metricas de Ventas y sus rendimientos.
Captura datos de competidores y los compara con los propios.
Tambien se puede observar las palabras Claves mas buscadas, junto a los productos mas solicitados de todas las categorias.


### Pre-requisitos 📋

- asgiref==3.3.4  
- bootstrap4==0.1.0  
- certifi==2021.5.30
- cffi==1.14.5
- chardet==4.0.0
- cryptography==3.4.7
- DateTime==4.3
- Django==3.2.4
- idna==2.10
- json5==0.9.5
- meli @ git+https://github.com/mercadolibre/python-sdk.git@09406bd544b974b379fea4818bd1040c7f147a40
- melisdk==0.1.3
- mercadolibre-python==0.2.1
- oauthlib==3.1.1
- pycparser==2.20
- PyMySQL==1.0.2
- pyOpenSSL==20.0.1
- python-dateutil==2.8.1
- pytz==2021.1
- requests==2.25.1
- requests-oauthlib==1.3.0
- six==1.16.0
- sqlparse==0.4.1
- typing-extensions==3.10.0.0
- urllib3==1.26.5
- zope.interface==5.4.0

### 1) Ingreso 🔧

Se ingresa con los datos que proporcionados por su proveedor:

![image](https://user-images.githubusercontent.com/72266387/122656552-f4776480-d131-11eb-9365-2a1693716bbc.png)


## 2) Pagina Inicio ⚙️

En la pagina de inicio podemos observar los datos actualizados de las ventas del dia del usuario principal.
Las mismas se actualizan comunicandose con la Api de Mercado libre.

Se puede observar las ventas de los ultimos 7 dias, mensuales y anuales de la cuenta principal.

![image](https://user-images.githubusercontent.com/72266387/122656698-6c925a00-d133-11eb-923d-f6483c90030b.png)


## 3) Pagina Competidores ⚙️

En esta pagina se ve reflejado los datos de los competidores elegidos, comparandolos con la cuenta principal.

Se puede observar la facturacion, las cantidades de ventas, tanto semanales como mensueales.

![image](https://user-images.githubusercontent.com/72266387/122656687-4371c980-d133-11eb-9e36-6ab8f78c03af.png)
![image](https://user-images.githubusercontent.com/72266387/122656691-4967aa80-d133-11eb-906c-10db9dcb6305.png)
![image](https://user-images.githubusercontent.com/72266387/122656694-508eb880-d133-11eb-8352-1ddf66e91914.png)


## 3) Pagina Tendencias ⚙️

En esta pagina observamos las 10 palabras mas buscadas de las ultimas 24 horas de Mercado libre, comunicandose con la Api de ML.

Se puede observar las 10 mas buscadas separadas por categoria.

![image](https://user-images.githubusercontent.com/72266387/122656724-b7ac6d00-d133-11eb-8e19-640a8f3aa86f.png)
![image](https://user-images.githubusercontent.com/72266387/122656729-c430c580-d133-11eb-9f29-ec8b84a8ffc1.png)




---
