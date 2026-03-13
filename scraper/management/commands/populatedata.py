from django.core.management.base import BaseCommand
import xml.etree.ElementTree as ET

from scraper.models import WikiData
from pathlib import Path

class Command(BaseCommand):
    help = 'Populates the database with data from the XML file'

    BASE_DIR = Path(__file__).resolve().parent.parent.parent


    def handle(self, *args, **options):
        wiki = []
        for event, element in ET.iterparse(self.BASE_DIR / 'assets' / 'wikipedia.xml', events=('end',)):
            if element.tag == '{http://www.mediawiki.org/xml/export-0.11/}page':
                title = element.find('{http://www.mediawiki.org/xml/export-0.11/}title').text
                text_el = element.find('{http://www.mediawiki.org/xml/export-0.11/}revision/{http://www.mediawiki.org/xml/export-0.11/}text')
                content = text_el.text if text_el is not None else '' 
                content = content if content else ''

                wiki.append(WikiData(title=title, content=content))
                print(f"Parsed: {title}")

                if len(wiki) >= 1000:
                    WikiData.objects.bulk_create(wiki, ignore_conflicts=True)
                    print(f"Inserted batch of 1000 records into the database.")
                    wiki = []  
                element.clear()  # Clear the element to save memory
        if wiki:
            WikiData.objects.bulk_create(wiki, ignore_conflicts=True)
        
        self.stdout.write(self.style.SUCCESS('Successfully populated the database with Wikipedia data.'))