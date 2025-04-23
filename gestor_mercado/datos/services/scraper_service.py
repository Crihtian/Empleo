# datos/services/scraper_service.py
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from django.utils.timezone import make_aware
from urllib.parse import urljoin
from datos.models import OfertaEmpleo, Habilidad

class ScraperUnificado:
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    def __init__(self):
        self.scrapers = {
            'TECNO': self.scrape_tecnoempleo,
            'INFO': self.scrape_infojobs
        }
    
    def ejecutar_scraping(self, plataformas=None, paginas=2):
        resultados = []
        plataformas = plataformas or ['TECNO', 'INFO']
        
        for plataforma in plataformas:
            if plataforma in self.scrapers:
                resultados += self.scrapers[plataforma](paginas)
        
        return resultados
    
    def _normalizar_habilidad(self, nombre):
        nombre = nombre.strip().lower()
        habilidad, _ = Habilidad.objects.get_or_create(nombre=nombre)
        return habilidad
    
    def _parsear_fecha(self, texto_fecha):
        hoy = datetime.now()
        texto_fecha = texto_fecha.lower()
        
        if 'hace' in texto_fecha:
            cantidad = int(''.join(filter(str.isdigit, texto_fecha)))
            if 'día' in texto_fecha:
                return hoy - timedelta(days=cantidad)
            elif 'hora' in texto_fecha:
                return hoy - timedelta(hours=cantidad)
        elif 'ayer' in texto_fecha:
            return hoy - timedelta(days=1)
        
        try:
            return datetime.strptime(texto_fecha, "%d/%m/%Y")
        except:
            return hoy
    
    def _guardar_oferta(self, datos):
        oferta, creada = OfertaEmpleo.objects.update_or_create(
            url=datos['url'],
            defaults={
                'titulo': datos['titulo'],
                'empresa': datos['empresa'],
                'ubicacion': datos['ubicacion'],
                'fecha_publicacion': make_aware(datos['fecha']),
                'salario': datos['salario'],
                'plataforma': datos['plataforma']
            }
        )
        
        if 'habilidades' in datos:
            habilidades = [self._normalizar_habilidad(h) for h in datos['habilidades']]
            oferta.habilidades.set(habilidades)
        
        return oferta  # Return the OfertaEmpleo object instead of just saving it

    def scrape_tecnoempleo(self, paginas=2):
        ofertas = []
        for pagina in range(1, paginas + 1):
            url = f"https://www.tecnoempleo.com/busqueda-empleo.aspx?pagina={pagina}"
            response = requests.get(url, headers=self.HEADERS)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            for trabajo in soup.select('article.element-vacancy'):
                datos = {
                    'plataforma': 'TECNO',
                    'titulo': trabajo.select_one('a.title').get_text(strip=True),
                    'empresa': trabajo.select_one('span.name').get_text(strip=True),
                    'ubicacion': trabajo.select_one('li.location').get_text(strip=True),
                    'fecha': self._parsear_fecha(trabajo.select_one('time').get_text(strip=True)),
                    'salario': trabajo.select_one('li.salary').get_text(strip=True),
                    'url': urljoin(url, trabajo.select_one('a.title')['href']),
                    'habilidades': [tag.get_text(strip=True) 
                                  for tag in trabajo.select('li.tags span')]
                }
                ofertas.append(self._guardar_oferta(datos))
        
        return ofertas

    def scrape_infojobs(self, paginas=2):
        ofertas = []
        base_url = "https://www.infojobs.net"
        
        for pagina in range(1, paginas + 1):
            params = {'page': pagina}
            response = requests.get(f"{base_url}/oferta-trabajo", params=params, headers=self.HEADERS)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            for card in soup.select('div.ij-OfferCardContent'):
                datos = {
                    'plataforma': 'INFO',
                    'titulo': card.select_one('h2 a').get_text(strip=True),
                    'empresa': card.select_one('span.ij-OfferCardContent-description-company').get_text(strip=True),
                    'ubicacion': card.select_one('span.ij-OfferCardContent-description-location').get_text(strip=True),
                    'fecha': self._parsear_fecha(card.select_one('span.ij-OfferCardContent-description-date').get_text(strip=True)),
                    'salario': card.select_one('span.ij-OfferCardContent-description-salary').get_text(strip=True),
                    'url': urljoin(base_url, card.select_one('h2 a')['href']),
                    'habilidades': [tag.get_text(strip=True) 
                                  for tag in card.select('div.ij-OfferCardContent-description-tags span')]
                }
                ofertas.append(self._guardar_oferta(datos))
        
        return ofertas

# Uso:
# scraper = ScraperUnificado()
# resultados = scraper.ejecutar_scraping(paginas=3)