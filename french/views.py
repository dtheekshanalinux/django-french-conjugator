from django.shortcuts import render
import requests
from requests.compat import quote_plus # this thing add  sign to spaces
from bs4 import BeautifulSoup
from . import models

BASE_CONJUGATOR_URL = 'https://conjugator.reverso.net/conjugation-french-verb-{}.html'

def home(request):
    return render(request, 'base.html')

def new_search(request):
    search = request.POST.get('search')
    models.search.objects.create(search=search)
    print(quote_plus(search))
    Final_url = BASE_CONJUGATOR_URL.format(quote_plus(search))
    print(Final_url)
    response = requests.get(Final_url)
    data = response.text
    soup = BeautifulSoup(data, features='html.parser')

    card_listings = soup.find_all('div', {'class':'result-block-api'})
    #all content we want
    card_postings = []
    
    #post_title_listings = post_title_detail()

    # body card detail 
    card_detail = soup.find_all('div',{'class':'word-wrap-title'})
    for card in card_detail:
        card_title = card.find('h4').text

        card_postings.append((card_title))
    print(card_postings)

    # post title
     
    # this function is for get that how many cards for specific title 


    stuff_for_frontend = {
    'search':search,
    'card_postings':card_postings,
    }
    return render(request, 'index.html', stuff_for_frontend)
    
# this function is for get that how many cards for specific title 