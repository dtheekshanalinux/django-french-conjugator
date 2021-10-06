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
    #print(quote_plus(search))
    Final_url = BASE_CONJUGATOR_URL.format(str(quote_plus(search)))
    #print(Final_url)
    response = requests.get(Final_url)
    data = response.text
    soup = BeautifulSoup(data, features='html.parser')

    card_listings = soup.find_all('div', {'class':'result-block-api'})
    #all content we want
    card_postings = []
    
    # body card detail 
    card_detail = soup.find_all('div',{'class':'word-wrap-title'})
    for card in card_detail:
        card_title = card.find('h4').text

        card_postings.append((card_title))
    #print(card_postings)
    card_name = tuple(card_postings)
    

    num_list =[]
    
    # iterate posts inside card
    post_detail = soup.find_all('div',{'class':'blue-box-wrap'})
    for div in post_detail:
        post = div.find('p').text
        num_list.append((post))
    
    arrays = [[num_list[0]]] # array of sub-arrays (starts with first value)

    for i in range(1, len(num_list)): # go through each element after the first
        if num_list[i] != "Présent": # If it's larger than the previous
            arrays[len(arrays)-1].append(num_list[i]) # Add it to the last sub-array
        else: # otherwise
            arrays.append([num_list[i]])
    #convert array to a tuple
    post_title = tuple([tuple(e) for e in arrays])
    #print(post_title)
    #post content details
    parent_list = soup.find_all('ul',{'class':'wrap-verbs-listing'})  
    parent_final = []
    len_parent = []
    for lists in parent_list:
        check_list = lists.find_all('li')
        len_of_parent = len(check_list)
        len_parent.append(len_of_parent)
        for check in check_list:
            parentitem = check.get_text()
            parent_final.append(parentitem)
    #this is used to chunk that list
    data = parent_final 
    sizes = len_parent
    it = iter(data)
    post_content = ([[next(it) for _ in range(size)] for size in sizes])
    #convert list to tuple
    card_content = tuple([tuple(e) for e in post_content])
    whole_stuff = {card_name: {post_title: card_content}}
    print(whole_stuff)
    #this thing is used to return nested array with dictionary
    #dic_of_stuff = {tuple(card_postings): {post_title: card_content}}
    # this function is for get that how many cards for specific title 
    #print(dic_of_stuff)

    stuff_for_frontend = {
    'search':search,
    'card_postings':card_postings,
    'whole_stuff':whole_stuff,
    }
    return render(request, 'index.html', stuff_for_frontend)
    
# this function is for get that how many cards for specific title 