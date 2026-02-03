import time #Pausas necesarias para request a Google

from api_client import peticion_segura #Verificacion para los datos
from config import API_KEY, LAT, LNG, RADIO #Extrae los datos para

#Solicitud del back a la API
def buscar_lugares(tipo, maximo):

    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json" #URL al que se solicitan los datos

    resultados = []
    token = None

    while len(resultados) < maximo: #Estira resultados de una categoria hasta un maximo de resultados

        params = {
            "location": f"{LAT},{LNG}",
            "radius": RADIO,
            "type": tipo,
            "key": API_KEY
        }                       
        #Parametros de la busqueda.

        if token:
            params["pagetoken"] = token
            time.sleep(2)
            #Un retraso para las peticiones, evita que te bloqueen

        #Medidas de seguridad en caso de problemas de coneccion o corrupcion de datos
        data = peticion_segura(url, params)

        if not data or data["status"] != "OK":
            break

        resultados.extend(data["results"])

        token = data.get("next_page_token")

        if not token:
            break

    return resultados[:maximo]


#Obtencion de datos de contacto
def obtener_detalles(place_id):

    url = "https://maps.googleapis.com/maps/api/place/details/json"

    params = {
        "place_id": place_id,

        # AGREGAMOS opening_hours
        "fields": "formatted_phone_number,website,opening_hours",

        "key": API_KEY
    }

    data = peticion_segura(url, params)

    if not data or data["status"] != "OK":
        return {}

    return data["result"]
