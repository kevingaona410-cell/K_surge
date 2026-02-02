import time #Nos permite manipular valores de tiempo

from config import CATEGORIAS, MAX_RESULTADOS
from services import buscar_lugares, obtener_detalles
from database import LugarDB
from models import Lugar
#Estiramos clases, funciones y variables que creamos en los otros archivos

#La funcion principal del programa
def main():

    db = LugarDB()

    for categoria, tipos in CATEGORIAS.items(): #Busca 

        print(f"\nBuscando: {categoria.upper()}")

        contador = 0

        for tipo in tipos:

            if contador >= MAX_RESULTADOS:
                break

            lugares_api = buscar_lugares(
                tipo,
                MAX_RESULTADOS - contador
            )

            for lugar_api in lugares_api:

                detalles = obtener_detalles(
                    lugar_api["place_id"]
                )

                lugar = Lugar(
                    lugar_api,
                    categoria,
                    detalles
                )

                db.guardar(lugar)

                contador += 1

                if contador >= MAX_RESULTADOS:
                    break

            time.sleep(0.5)


if __name__ == "__main__":
    main()
