from django.urls import path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('', RedirectView.as_view(url='search/')),
    path('scrap/', views.scrap_page, name='scrap'),
    path('search/', views.search_page, name='search'),
]
