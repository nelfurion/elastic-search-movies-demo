from django.shortcuts import render

from .services.elasticsearch import ElasticSearchService

def index(request):
    skip = int(request.GET.get('skip', 0))
    take = int(request.GET.get('take', 10))
    search = request.GET.get('search', None)

    es_service = ElasticSearchService('http://127.0.0.1:9200')

    if search:
        result = es_service.full_text_search(search, take, skip)
    else:
        result = es_service.get_movies(take, skip)

    movies_result = result['hits']['hits']
    total_movies = result['hits']['total']
    movies = []

    for movie in movies_result:
        movie['_source']['actor_string'] = ', '.join(movie['_source']['actors'])
        movies.append(movie['_source'])

    last_skip = skip - take
    if last_skip < 0:
        last_skip = 0

    pages_count = int(total_movies / take)
    last_page = int(skip / 10 - 1)
    if last_page < 0:
        last_page = 0

    return render(request, 'movies/index.html', {
        'movies': movies,
        'pages_count': pages_count,
        'skipped': skip,
        'last_skip': last_skip,
        'next_skip': skip + take,
        'last_page': last_page,
        'current_page': int(skip / 10),
        'next_page': int(skip / 10 + 1),
        'pages_range': range(pages_count)
    })
