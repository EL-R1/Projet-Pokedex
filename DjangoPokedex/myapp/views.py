from django.http import HttpResponse
from django.shortcuts import render
import random
import requests as re


# Create your views here.
def index(request):
    context = {'name': 'Titi', 'age': 49, 'citation': 'La terre est ronde'}
    return render(request, 'myapp/index.html', context)


def accueil(request):
    text = "<h1>Bienvenue ! </h1> <p> Ma première application Django ! :D </p>"
    return HttpResponse(text)


def result(request, number):
    text = "Le résultat de la requête est %d" % number
    return HttpResponse(text)


def pokemon(request):
    rand = random.randint(1, 800)
    url = "https://pokeapi.co/api/v2/pokemon/"
    r = re.get(url + str(rand))
    response = r.json()
    nameEn = response['name']
    nameEn = nameEn.capitalize()
    img = response['sprites']['other']['official-artwork']['front_default']
    poids = response['weight']

    nameFr = ''
    content = re.get(
        "https://raw.githubusercontent.com/PokeAPI/pokeapi/master/data/v2/csv/pokemon_species_names.csv").text
    x = 0
    for line in content.splitlines():
        items = line.split(',')
        if items[1] == '9' and items[2] == nameEn:
            nameFr = content.splitlines()[x - 4].split(',')[2]
        x += 1
    if nameFr == '':
        nameFr = nameEn
    context = {'name': nameFr, 'img': img, 'poids' : poids}
    return render(request, 'myapp/pokemon.html',context)
