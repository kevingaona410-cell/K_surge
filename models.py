#Importacion de un formato de fecha y hora
from datetime import datetime

#La clase Lugar crea instancias para las entradas que obtenemos de la API
class Lugar:

    def __init__(self, lugar_api, categoria, detalles):

        self.place_id = lugar_api["place_id"]                       #ID del lugar
        self.nombre = lugar_api["name"]                             #Nombre del lugar
        self.direccion = lugar_api.get("vicinity", "")              #Direccion

        self.lat = lugar_api["geometry"]["location"]["lat"]         #Coordenadas de Latitud
        self.lng = lugar_api["geometry"]["location"]["lng"]         #Coordenadas de longitud

        self.categoria = categoria                                  #Categoria del lugar (Cultural, gastronomico, etc)

        self.tipos = ",".join(lugar_api.get("types", []))           #Etiquetas(tags) del lugar  

        self.rating = lugar_api.get("rating", "-")                    #Calificacion (segun google.places (maps))

        self.telefono = detalles.get("formatted_phone_number", "Sin numero")  #Numero de telefono 
        self.web = detalles.get("website", "")                      #Pagina web  ("" en caso de no tener)
        # HORARIOS
        horarios = detalles.get("opening_hours", {})
        self.horarios = "; ".join(
            horarios.get("weekday_text", [])
        )


        self.fecha = datetime.now().isoformat()                     #Fecha y hora de la ultima actualizacion 
