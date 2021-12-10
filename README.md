# Projet-Pokedex

Bienvenue sur le pokédex qui concurrencera Pokepédia

Ce pokedex utilisera l'api [pokeapi](https://pokeapi.co/)

## Installation
### Environnement Virtuel
 - Après avoir pull le dépot git, vous devez créer un environnement virtuel grâce à la commande suivante :

 **WARNING**: ne pas créer l'environnement virtuel dans le dossier Projet-Pokedex
```shell
py -m venv Pokedex
```
(ici "Pokedex" sera le nom de l'environnement que vous créerez)

 - Ensuite il faut activer cet environnement virtuel (il suffit juste de lancer le fichier activate) :
```shell
.\Pokedex\Scripts\activate
```

Un fois dans l'environnement virtuel nous pouvons installer nos packages/librairies

### Packages
 - Nous avons beaucoup de package dans notre projet et voici comment les installer :

```shell
#installation de Django
pip install django

#Pour aller dans le dossier de django et ainsi installer les dépendances dedans
cd .\Projet-Pokedex\DjangoPokedex\

#Installer le package requests
pip install requests
```

# Lancement
Vous pouvez lancer ce projet avec la commande :
````shell
py .\manage.py runserver
````

## Contributeurs
- Juliette Raynaud
- Mathys Vende
- Erwan Leblanc



