import requests
from bs4 import BeautifulSoup
from database import VillaMorraDB
from urllib.parse import urljoin

class QSurgeScraper:
    def __init__(self, api_key=None):
        self.db = VillaMorraDB()
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        self.negra = ["privacidad", "términos", "cookies", "política", "contacto"]
        self.blanca = ["feria", "concierto", "show", "fiesta", "teatro", "asunción", "villa morra", "música", "arte", "evento", "cine"]

    def ejecutar_web(self):
        fuentes = [
            "https://www.abc.com.py/tag/agenda-cultural/",
            "https://www.ultimahora.com/agenda-cultural-uh",
            "https://www.cultura.gov.py/category/agenda/",
            "https://www.asuncion.live/eventos/lista/",
            "https://www.filmagic.com.py/"
        ]
        print(f"📡 Rastreo real en {len(fuentes)} fuentes locales...")
        for url in fuentes:
            try:
                res = requests.get(url, headers=self.headers, timeout=15)
                if res.status_code != 200: continue
                soup = BeautifulSoup(res.text, 'html.parser')
                elementos = soup.find_all(['a', 'h2', 'h3'])
                for el in elementos:
                    tit = el.get_text(strip=True)
                    tit_l = tit.lower()
                    if any(b in tit_l for b in self.blanca) and not any(n in tit_l for n in self.negra):
                        if len(tit) > 12:
                            link = el.get('href') if el.name == 'a' else url
                            if link and link.startswith('/'): link = urljoin(url, link)
                            self.db.registrar_evento(tit.capitalize(), "Asunción / Villa Morra", "Consultar sitio", "Agenda Real", link)
            except Exception as e:
                print(f"❌ Error en {url}: {e}")

    def run(self):
        self.db.borrar_todo()
        self.ejecutar_web()