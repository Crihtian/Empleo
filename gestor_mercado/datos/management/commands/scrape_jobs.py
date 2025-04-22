# En management/commands/scrape_jobs.py
from django.core.management.base import BaseCommand
from datos.services.scraper_service import ScraperUnificado

class Command(BaseCommand):
    help = 'Ejecuta scrapers de empleo'
    
    def add_arguments(self, parser):
        parser.add_argument('--pages', type=int, default=2, help='Número de páginas a scrapear')

    def handle(self, *args, **options):
        pages = options['pages']
        
        scrapers = [
            ScraperUnificado(),
        ]
        
        for scraper in scrapers:
            self.stdout.write(f'Iniciando scraper: {type(scraper).__name__}')
            try:
                results = scraper.scrape(max_pages=pages)
                self.stdout.write(self.style.SUCCESS(f'➤ {len(results)} ofertas procesadas'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'✖ Error: {str(e)}'))