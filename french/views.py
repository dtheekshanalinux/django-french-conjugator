from django.shortcuts import render
import requests
from requests.compat import quote_plus # this thing add  sign to spaces
from bs4 import BeautifulSoup
from . import models

def home(requests):
    return render(requests, 'base.html')

def new_search(requests):
    return render(requests, 'index.html')