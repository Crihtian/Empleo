# En management/commands/scrape_jobs.py
from django.core.management.base import BaseCommand
from datos.services.scraper_service import ScraperUnificado

class Command(BaseCommand):
    help = 'Ejecuta scrapers de empleo'
    
    def add_arguments(self, parser):
        parser.add_argument('--pages', type=int, default=2, help='Número de páginas a scrapear')
        parser.add_argument('--platform', type=str, help='Filtrar por plataforma (e.g., TECNO, INFO)')
        parser.add_argument('--location', type=str, help='Filtrar por ubicación')

    def handle(self, *args, **options):
        pages = options['pages']
        platform = options.get('platform')
        location = options.get('location')
        
        scraper = ScraperUnificado()
        resultados = scraper.ejecutar_scraping(plataformas=[platform] if platform else None, paginas=pages)
        
        self.stdout.write(f'Iniciando scraper: {type(scraper).__name__}')
        try:
            if location:
                resultados = [r for r in resultados if location.lower() in r.ubicacion.lower()]
            
            for oferta in resultados:
                self.stdout.write(f"➤ {oferta.titulo} - {oferta.empresa} ({oferta.ubicacion})")
                self.stdout.write(f"  Fecha: {oferta.fecha_publicacion}, Salario: {oferta.salario}")
                self.stdout.write(f"  URL: {oferta.url}")
                self.stdout.write(f"  Habilidades: {', '.join(h.nombre for h in oferta.habilidades.all())}")
                self.stdout.write("-" * 80)
            
            self.stdout.write(self.style.SUCCESS(f'➤ {len(resultados)} ofertas procesadas'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✖ Error: {str(e)}'))