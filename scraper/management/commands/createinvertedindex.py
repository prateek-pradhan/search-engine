from django.core.management.base import BaseCommand
from search.models import InvertedIndex
from scraper.models import WikiData
from search.services import normalize_token

class Command(BaseCommand):

    def handle(self, *args, **options):
        indexes = {}
        
        for wiki in WikiData.objects.all().iterator():
            title = wiki.title
            tokens = title.split()
            for token in tokens:
                normalized_token = normalize_token(token)
                if normalized_token:
                    if normalized_token not in indexes:
                        indexes[normalized_token] = set()
                    indexes[normalized_token].add(wiki.id)
        
        inverted_index = []
        for token, wiki_ids in indexes.items():
            inverted_index.append(InvertedIndex(token=token, wiki=list(wiki_ids)))

            if len(inverted_index) >= 1000:
                InvertedIndex.objects.bulk_create(inverted_index, ignore_conflicts=True)
                print(f"Inserted batch of 1000 records into the inverted index.")
                inverted_index = []
        if inverted_index:
            InvertedIndex.objects.bulk_create(inverted_index, ignore_conflicts=True) 

        self.stdout.write(self.style.SUCCESS('Successfully created the inverted index.'))
        


