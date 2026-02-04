import requests
from bs4 import BeautifulSoup
from database import VillaMorraDB
from urllib.parse import urljoin

class QSurgeScraper:
    def __init__(self, api_key=None):
        self.db = VillaMorraDB()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        # Listas optimizadas para Asunción
        self.negra = ["privacidad", "términos", "cookies", "política", "contacto", "suscripción", "ingresar"]
        self.blanca = ["feria", "concierto", "show", "fiesta", "teatro", "asunción", "villa morra", "música", "arte", "evento", "cine", "festival", "taller"]

    def ejecutar_web(self):
        fuentes = [
            "https://www.abc.com.py/tag/agenda-cultural/",
            "https://www.ultimahora.com/agenda-cultural-uh",
            "https://www.cultura.gov.py/category/agenda/",
            "https://www.asuncion.live/eventos/lista/",
            "https://www.filmagic.com.py/"
        ]
        
        print(f"📡 Rastreo real en {len(fuentes)} fuentes locales...")
        eventos_encontrados = 0

        for url in fuentes:
            try:
                res = requests.get(url, headers=self.headers, timeout=10)
                if res.status_code != 200:
                    continue
                
                soup = BeautifulSoup(res.text, 'html.parser')
                # Buscamos en etiquetas comunes de títulos y enlaces
                elementos = soup.find_all(['a', 'h2', 'h3'])
                
                for el in elementos:
                    tit = el.get_text(strip=True)
                    tit_l = tit.lower()
                    
                    # Lógica de filtrado inteligente
                    if any(b in tit_l for b in self.blanca) and not any(n in tit_l for n in self.negra):
                        if len(tit) > 15: # Evitamos títulos demasiado cortos o ruidos
                            link = el.get('href') if el.name == 'a' else url
                            
                            # Validar y completar URL
                            if link and (link.startswith('/') or not link.startswith('http')):
                                link = urljoin(url, link)
                            
                            # Registro en la DB
                            self.db.registrar_evento(
                                tit.replace('"', '').replace("'", ""), # Limpieza básica
                                "Asunción / Villa Morra", 
                                "Consultar fecha en link", 
                                "Evento detectado automáticamente por QSurge", 
                                link
                            )
                            eventos_encontrados += 1

            except Exception as e:
                print(f"⚠️ Nota: No se pudo rastrear {url} (Tiempo de espera agotado)")

        print(f"✨ Rastreo finalizado. {eventos_encontrados} coincidencias procesadas.")

    def run(self):
        # Limpiamos para la presentación y volvemos a llenar
        self.db.obtener_conteo()
        self.ejecutar_web()