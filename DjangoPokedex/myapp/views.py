from django.http import HttpResponse
from django.shortcuts import render
import random
import requests as re


def translate(num_pok, content, nameEn):
    # Traduction dynamique avec les csv data sur github

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
            break
        x += 1
    if nameFr == '':
        nameFr = nameEn

    return nameFr


def translate_name():
    # Traduction des noms grâce à l'api
    url = "https://pokeapi.co/api/v2/pokemon-species/?offset=0&limit=1500"
    r = re.get(url)
    response = r.json()
    nameFr = []
    for pokemon in response["results"]:
        r = re.get(pokemon['url'])
        response_Fr = r.json()
        nameFr.append(response_Fr['names'][4]['name'])

    return nameFr


def find_num_pok(nameEn):
    # Trouver l'id du pokemon lors de la recherche
    try:
        nameEn = int(nameEn)
        if nameEn > 10220:
            nameEn = 10220
        elif 898 <= nameEn <= 10001:
            a = nameEn - 898
            b = 10001 - nameEn
            if a < b:
                nameEn = 898
            else:
                nameEn = 10001
        elif nameEn <= 0:
            nameEn = 1
    except:
        nameEn = str(nameEn)
        print(nameEn)

    url = "https://pokeapi.co/api/v2/pokemon/"
    r = re.get(url + str(nameEn))
    if str(r) == "<Response [404]>":
        if nameEn == "sus":
            num_pok = "ඞ"
        else:
            num_pok = 1
    else:
        response = r.json()
        num_pok = int(response['id'])
    return num_pok


def init_pokemon(num_pok):
    url = "https://pokeapi.co/api/v2/pokemon/"
    name_url = "https://pokeapi.co/api/v2/pokemon-species/"
    type_url = "https://pokeapi.co/api/v2/type/"
    nameEn = ''
    img = ''
    poids = ''
    image = ''
    typeFr = ''
    taille = ''
    nameFr = ''
    shiny = ''
    if isinstance(num_pok, int):
        if 1 <= num_pok <= 898 or 10001 <= num_pok <= 10220:
            r = re.get(url + str(num_pok))
            response = r.json()
            nameEn = response['name']
            img = response['sprites']['front_default']
            poids = int(response['weight']) / 10
            image = response['sprites']['other']['official-artwork']['front_default']
            type = response['types']
            taille = int(response['height']) / 10
            shiny = response['sprites']['front_shiny']

            # Traduction avec l'api des types
            typeFr = []
            for types in type:
                r_type = re.get(type_url + str(types['type']['name']))
                response_type = r_type.json()
                typeFr.append(response_type['names'][2]['name'])

            # Traduction avec l'api des noms
            r_nameFr = re.get(name_url + str(num_pok))
            if str(r_nameFr) == "<Response [404]>":
                # delete les noms anglais avec des tirets pour traduire la 1ere partie de leur nom

                # new_nameEn = nameEn.split("-", 1)
                # new_nameEn = new_nameEn[0]
                #
                # r_nameFr = re.get(name_url + str(new_nameEn))
                # response_Fr = r_nameFr.json()
                # nameFr = response_Fr['names'][4]['name']
                #
                # if str(r_nameFr) == "<Response [404]>":
                #     nameFr = nameEn
                nameFr = nameEn
            else:
                response_Fr = r_nameFr.json()
                nameFr = response_Fr['names'][4]['name']
    else:
        nameEn = 'ඞ'
        img = ''
        poids = 'ඞ'
        image = 'https://i.kym-cdn.com/photos/images/original/002/099/612/83c.png'
        typeFr = 'ඞ'
        taille = 'ඞ'
        nameFr = 'ඞ'

    tab_num_pok = {'nameEn': nameEn, 'img': img, 'poids': poids, 'image': image, 'type': typeFr, 'taille': taille,
                   'nameFr': nameFr, 'shiny': shiny}
    return tab_num_pok


# Create your views here.
def index(request):
    if request.method == 'POST':
        if request.POST.get("Pokemon") is not None and request.POST.get("Pokemon_Team") is None:
            num_pok = int(request.POST.get("Pokemon"))
        elif request.POST.get("Random") is not None:
            num_pok = random.randint(1, 800)
        elif request.POST.get("Pokemon_Name") is not None:
            num_pok = str(request.POST.get("Pokemon_Name"))
            pokemon_name = str(num_pok)
            num_pok = find_num_pok(pokemon_name)
        elif request.POST.get("Pokemon_Team") is not None:
            text = "<h1>Pokemon : none </p>"
            return render(request, 'myapp/temp.html')
            # test de session de merde

            # x =-1
            # if request.session.get(0, True):
            #     for pok in request.session[0]:
            #         x+=1
            #     request.session[0] = str(request.POST.get("Pokemon_Team"))
            # else:
            #     request.session[0] = "rien pd"
            #
            # #print(request.session[0])
            num_pok = find_num_pok(request.POST.get("Pokemon"))
        else:
            num_pok = 1
    else:
        num_pok = 1

    # fix de l'api qui pue la merde vers la fin
    if isinstance(num_pok, int):
        num_pok = int(num_pok)
        if num_pok == 10001:
            num_pok0 = 898
        else:
            num_pok0 = num_pok - 1
        if num_pok == 898:
            num_pok1 = 10001
        else:
            num_pok1 = num_pok + 1
    else:
        num_pok0 = 0
        num_pok1 = 0
    # pokemon précedent
    tab_pok0 = init_pokemon(num_pok0)
    # pokémon actuel
    tab_pok = init_pokemon(num_pok)

    # pokémon suivant
    tab_pok1 = init_pokemon(num_pok1)

    # Récupération de tous les pokémons pour la barre de recherche
    all_pok_url = "https://pokeapi.co/api/v2/pokemon/?offset=0&limit=1500"
    all_pokemon = []
    r = re.get(all_pok_url)
    response = r.json()
    for pokemon in response["results"]:
        all_pokemon.append(pokemon['name'])

    # Traduire les noms des pokémons
    # name = re.get(
    #     "https://raw.githubusercontent.com/PokeAPI/pokeapi/master/data/v2/csv/pokemon_species_names.csv").text
    # nameFr = translate(num_pok, name, tab_pok['nameEn'])
    # nameFr0 = translate(num_pok0, name, tab_pok0['nameEn'])
    # nameFr1 = translate(num_pok1, name, tab_pok1['nameEn'])

    # Traduire les types des pokémons
    # type = re.get("https://raw.githubusercontent.com/veekun/pokedex/master/pokedex/data/csv/type_names.csv").text
    # typeFr = []
    # for types in tab_pok['type']:
    #     typeFr.append(translate(num_pok, type, types['type']['name']))

    # Traduire tous les pokemons

    # all_pokemon = translate_name()
    # all_pokemonFr = []
    # for pokemons in all_pokemon:
    #     all_pokemon.append(translate(0, name, pokemons))

    context = {'name': tab_pok['nameFr'], 'name0': tab_pok0['nameFr'], 'name1': tab_pok1['nameFr'],
               'img0': tab_pok0['img'], 'img': tab_pok['img'],
               'img1': tab_pok1['img'],
               'image': tab_pok['image'], 'poids': tab_pok['poids'], 'num_pok': num_pok, 'num_pok0': num_pok0,
               'num_pok1': num_pok1,
               'type': tab_pok["type"],
               'taille': tab_pok['taille'], 'all_pokemon': all_pokemon,
               'shiny': tab_pok['shiny']}

    return render(request, 'myapp/index.html', context)


def team(request):
    return render(request, 'myapp/temp.html')
