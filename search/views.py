from django.shortcuts import render, get_object_or_404
from scraper.models import WikiData
from django.http import HttpResponse


# Create your views here.
def basic_search(request, title):
    wiki = WikiData.objects.filter(title__icontains=title)
    if not wiki.exists():
        return HttpResponse("No results found.")

    return render(request, 'basic_search.html', {'wiki': wiki})

def get_wiki(request, id):
    wiki = get_object_or_404(WikiData, id=id)
    print(wiki)
    return render(request, 'wiki_detail.html', {'wiki': wiki})