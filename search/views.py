import requests
from django.shortcuts import render
from SearchKSA.settings import BASE_DIR
from ksalib.ksalib.Auth import Auth
from ksalib.ksalib.gaonnuri import get_board_names, get_special_links, board_url
from . import scrap, search
from .search import TIME, RELEVANCE, DEFAULT

def update_all():
    auth = Auth()
    auth.lms_auth(*scrap.read_id_pw(BASE_DIR/'search/auth_data/lms_data.txt'))
    scrap.save_all_lms_board(auth)
    scrap.save_all_lms_post(auth)
    auth.gaonnuri_auth(*scrap.read_id_pw(BASE_DIR/'search/auth_data/gaonnuri.txt'))
    scrap.save_all_gaonnuri_page(auth)
    scrap.save_all_gaonnuri_post(auth)

def scrap_page(request):
    scrap.save_all_ksa_page()
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
