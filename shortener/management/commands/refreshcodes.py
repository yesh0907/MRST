from django.core.management.base import BaseCommand, CommandError
from shortener.models import ShortenURL

class Command(BaseCommand):
    help = 'Refreshes all Shortened URL shortcodes'

    def handle(self, *args, **options):
        print(options)
        return ShortenURL.objects.refresh_shortcodes()