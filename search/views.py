import requests
from django.shortcuts import render
from ksalib.ksalib.Auth import Auth
from ksalib.ksalib.gaonnuri import get_board_names, get_special_links, board_url
from . import scrap, search
from .search import TIME, RELEVANCE, DEFAULT

def scrap_page(request):
    auth = Auth()
    auth.gaonnuri_auth('ksa20017', 'CEHJtTF94h7senQ')
    #scrap.save_all_gaonnuri_post(auth)
    scrap.save_all_gaonnuri_page(auth)
    return render(request, 'scrap.html')

def search_page(request):
    website_limit = 5
    if 'key' in request.GET.keys():
        s = request.GET.get('key')
        if 'mode' in request.GET.keys():
            get_mode = request.GET.get('mode')
            if get_mode == 'time':
                mode = TIME
            elif get_mode == 'relevance':
                mode = RELEVANCE
            else:
                mode = DEFAULT
        else:
            mode = DEFAULT
        if 'website' in request.GET.keys():
            pages = search.search_pages(s, mode, request.GET.get('website'))
            context = {'pages': pages}
            return render(request, 'results_site.html', context=context)
        else:
            result = search.search_pages(s, mode)
            context = {'result': result, 'website_limit': website_limit}
            return render(request, 'results.html', context=context)
    else:
        return render(request, 'search.html')
