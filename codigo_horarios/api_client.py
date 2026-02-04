import requests


def peticion_segura(url, params):

    try:
        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()
        return r.json()

    except requests.exceptions.RequestException as e:
        print("Error de red:", e)
        return None

#Encapsula todas las llamadas HTTP.

#En caso de cambiar de libreria, solo se modifica este archivo