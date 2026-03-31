from django.core.management.base import BaseCommand
from search.models import InvertedIndex
from scraper.models import WikiData
from search.services import normalize_token, clean_content
from pathlib import Path

class Command(BaseCommand):

    BASE_DIR = Path(__file__).resolve().parent.parent.parent

    def handle(self, *args, **options):
        indexes = {}

        stop_words = set()
        self.load_stop_words(stop_words)

        print_counter = 0
        
        for wiki in WikiData.objects.all().iterator():
            title = wiki.title
            content = clean_content(wiki.content)
            title_tokens = title.split()
            content_tokens = content.split()
            print(f"Processing WikiData ID: {wiki.id}, Title: {wiki.title}")
            for token in title_tokens:
                self.rank_token(token, wiki.id, indexes, 10, stop_words)

            for token in content_tokens:
                self.rank_token(token, wiki.id, indexes, 1, stop_words)
            
            if len(indexes) == 1000 * print_counter:
                print(f"Processed {print_counter * 1000} tokens.")
                print_counter += 1
                
        inverted_index = []
        for token, wiki_ids in indexes.items():
            inverted_index.append(InvertedIndex(token=token, wiki=wiki_ids))

            if len(inverted_index) >= 1000:
                InvertedIndex.objects.bulk_create(inverted_index, ignore_conflicts=True)
                print(f"Inserted batch of 1000 records into the inverted index.")
                inverted_index = []
        if inverted_index:
            InvertedIndex.objects.bulk_create(inverted_index, ignore_conflicts=True) 

        self.stdout.write(self.style.SUCCESS('Successfully created the inverted index.'))
        


    def rank_token(self, token, wiki_id, indexes, rank, stop_words=None):
        normalized_token = normalize_token(token)

        if normalized_token in stop_words or normalized_token == "" or len(normalized_token) > 255:
            return

        if normalized_token not in indexes:
            indexes[normalized_token] = dict()
        if wiki_id not in indexes[normalized_token]:
            indexes[normalized_token][wiki_id] = rank
        else:
            indexes[normalized_token][wiki_id] += rank
    
    def load_stop_words(self, stop_words):
        file_path = self.BASE_DIR / 'assets' / 'stopwords.txt'

        try:
            with open(file_path, 'r') as file:
                for line in file:
                    stop_words.add(line.strip())
        except FileNotFoundError:
            print(f"Error: The file at {file_path} was not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

