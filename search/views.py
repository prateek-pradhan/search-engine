from django.shortcuts import render, get_object_or_404
from scraper.models import WikiData
from django.http import HttpResponse
from search.services import normalize_token
from search.models import InvertedIndex

# Create your views here.
def basic_search(request, title):
    wiki = WikiData.objects.filter(title__icontains=title)
    if not wiki.exists():
        return HttpResponse("No results found.")

    return render(request, 'basic_search.html', {'wiki': wiki})

def tokenized_query(request, title):
    tokens = title.split()
    wiki_list = set()
    for token in tokens:
        normalized_token = normalize_token(token)

        token_data = InvertedIndex.objects.filter(token=normalized_token).first()
        if token_data is None:
            wiki_list = set()
            break   
        wiki_ids = token_data.wiki
        if wiki_list:
            wiki_list = wiki_list.intersection(set(wiki_ids))
        else:
            wiki_list = set(wiki_ids)
    wiki = WikiData.objects.filter(id__in=list(wiki_list))
    print(wiki)
    if not wiki:
        return HttpResponse("No results found.")
    return render(request, 'basic_search.html', {'wiki': list(wiki)})        

    

def get_wiki(request, id):
    wiki = get_object_or_404(WikiData, id=id)
    print(wiki)
    return render(request, 'wiki_detail.html', {'wiki': wiki})