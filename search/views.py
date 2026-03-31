from django.shortcuts import render, get_object_or_404
from scraper.models import WikiData
from search.services import normalize_token
from search.models import InvertedIndex

def tokenized_query(request):
    query = request.GET.get('query', '')
    
    if not query:
        return render(request, 'search_page.html')
    
    tokens = query.split()
    wiki_map = dict()

    normalized_tokens = []
    for token in tokens:
        normalized_token = normalize_token(token)
        if normalized_token:
            normalized_tokens.append(normalized_token)

    token_data = InvertedIndex.objects.filter(token__in=normalized_tokens)

    if not token_data:
        return render(request, 'search_page.html', {'query': query, "error_message": "No results found."})

    for wiki_token in token_data:
        for wiki_id, rank in wiki_token.wiki.items():
            wiki_map[wiki_id] = wiki_map.get(wiki_id, 0) + rank
    
    wiki = WikiData.objects.filter(id__in=wiki_map.keys()).only('id', 'title')

    if not wiki:
        return render(request, 'search_page.html', {'query': query, "error_message": "No results found."})
    
    sorted_wiki = sorted(wiki, key=lambda w: int(wiki_map[str(w.id)]), reverse=True)
    return render(request, 'search_page.html', {'wiki': sorted_wiki, 'query': query})        

    

def get_wiki(request, id):
    wiki = get_object_or_404(WikiData, id=id)
    return render(request, 'wiki_detail.html', {'wiki': wiki})