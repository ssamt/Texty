import requests
from django.shortcuts import render
from ksalib.ksalib.Auth import Auth
from ksalib.ksalib.gaonnuri import get_board_names
from . import scrap, search
from .search import TIME, RELEVANCE

def scrap_page(request):
    auth = Auth()
    auth.gaonnuri_auth('ksa20017', 'CEHJtTF94h7senQ')
    board_names = get_board_names(auth)
    scrap.save_all_gaonnuri_post(auth, board_names)
    return render(request, 'scrap.html')

def search_page(request):
    website_limit = 5
    if 'key' in request.GET.keys():
        s = request.GET.get('key')
        if 'website' in request.GET.keys():
            pages = search.search_pages(s, TIME, request.GET.get('website'))
            context = {'pages': pages}
            return render(request, 'results_site.html', context=context)
        else:
            result = search.search_pages(s, RELEVANCE)
            context = {'result': result, 'website_limit': website_limit}
            return render(request, 'results.html', context=context)
    else:
        return render(request, 'search.html')
