from django.http import HttpResponse
from django.shortcuts import render
import random
import requests as re


def translate(num_pok, content, nameEn):
    nameFr = ''
    nameEn = str(nameEn).capitalize()
    x = 0
    for line in content.splitlines():
        items = line.split(',')
        if items[1] == '9' and items[2] == nameEn:
            if num_pok != 0:
                nameFr = content.splitlines()[x - 4].split(',')[2]
            else:
                nameFr = 'none'
        x += 1
    if nameFr == '':
        nameFr = nameEn

    print(nameFr)
    return nameFr


def init_pokemon(url, num_pok):
    if num_pok != 0:
        r = re.get(url + str(num_pok))
        response = r.json()
        nameEn = response['name']
        img = response['sprites']['front_default']
        poids = int(response['weight']) / 10
        image = response['sprites']['other']['official-artwork']['front_default']
        type = response['types']

    else:
        nameEn = ''
        img = ''
        poids = ''
        image = ''
        type = ''

    tab_num_pok = {'nameEn': nameEn, 'img': img, 'poids': poids, 'image': image, 'type': type}
    return tab_num_pok


# Create your views here.
def index(request):
    url = "https://pokeapi.co/api/v2/pokemon/"

    if request.method == 'POST':
        if request.POST.get("Pokemon") is not None:
            num_pok = int(request.POST.get("Pokemon"))
        elif request.POST.get("Random") is not None:
            num_pok = random.randint(1, 800)
        else:
            num_pok = 1
    else:
        num_pok = 1

    num_pok0 = num_pok - 1
    num_pok1 = num_pok + 1

    tab_pok0 = init_pokemon(url, num_pok0)
    tab_pok = init_pokemon(url, num_pok)
    tab_pok1 = init_pokemon(url, num_pok1)

    name = re.get(
        "https://raw.githubusercontent.com/PokeAPI/pokeapi/master/data/v2/csv/pokemon_species_names.csv").text
    nameFr = translate(num_pok, name, tab_pok['nameEn'])
    nameFr0 = translate(num_pok0, name, tab_pok0['nameEn'])
    nameFr1 = translate(num_pok1, name, tab_pok1['nameEn'])

    type = re.get("https://raw.githubusercontent.com/veekun/pokedex/master/pokedex/data/csv/type_names.csv").text
    typeFr = []
    for types in tab_pok['type']:
        typeFr.append(translate(num_pok, type, types['type']['name']))

    context = {'name': nameFr, 'name0': nameFr0, 'name1': nameFr1, 'img0': tab_pok0['img'], 'img': tab_pok['img'],
               'img1': tab_pok1['img'],
               'image': tab_pok['image'], 'poids': tab_pok['poids'], 'pok0': num_pok0, 'pok1': num_pok1, 'type': typeFr}

    return render(request, 'myapp/index.html', context)


def accueil(request):
    text = "<h1>Bienvenue ! </h1> <p> Ma première application Django ! :D </p>"
    return HttpResponse(text)


def result(request, number):
    text = "Le résultat de la requête est %d" % number
    return HttpResponse(text)
