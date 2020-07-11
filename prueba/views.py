from django.http import HttpResponse
from django.template import Template, Context
from django.template.loader import get_template
from django.shortcuts import render
import requests
import json


class Episode:

    def __init__(self, ident, name, air_date, episode, characters, created):
        self.id = ident
        self.name = name
        self.air_date = air_date
        self.episode = episode
        self.characters = characters
        self.created = created

class Character:

    def __init__(self, ident, name, status, species, tipo, gender, origin, location, image, episode, created):
        self.id = ident
        self.name = name
        self.status = status
        self.species = species
        self.type = tipo
        self.gender = gender
        self.origin = origin
        self.location = location
        self.image = image
        self.episode = episode
        self.created = created

class Location:
    def __init__(self, ident, name):
        self.id = ident
        self.name = name
        self.dimension = ""
        self.tipo = ""
        self.personajes = []

def principal(request):
    response = requests.get("https://integracion-rick-morty-api.herokuapp.com/graphql/?query={episodes{info{count,pages,next},results{id}}}")
    data = json.loads(response.text.encode("utf-8"))
    episode_list = []
    for x in range(0, data["data"]["episodes"]["info"]["pages"]):
        pagina = str(x+1)
        response = requests.get("https://integracion-rick-morty-api.herokuapp.com/graphql/?query={episodes(page:"+pagina+"){info{count,pages,next},results{id, name, air_date, episode, characters{id, name, status, species, type, gender, origin{id},location{id}, image, episode{id}, created}, created }}}")
        data = json.loads(response.text.encode("utf-8"))
        episodio = data["data"]["episodes"]["results"]
        for episode in episodio:
            new_episode = Episode(episode["id"], episode["name"], episode["air_date"], episode["episode"], episode["characters"], episode["created"])
            episode_list.append(new_episode)
    principal_template = get_template("principal.html")
    document = principal_template.render({"episodios":episode_list})
    queryset = request.GET.get("buscar")
    if queryset:
        lista_resultados_episodios = []
        lista_resultados_personajes = []
        lista_resultados_lugares = []
        response = requests.get("https://integracion-rick-morty-api.herokuapp.com/graphql/?query={episodes{info{pages},results{id}}}")
        data = json.loads(response.text.encode("utf-8"))
        for x in range(0, data["data"]["episodes"]["info"]["pages"]):
            pagina = str(x+1)
            response = requests.get("https://integracion-rick-morty-api.herokuapp.com/graphql/?query={episodes(page:"+pagina+"){info{pages},results{id, name, air_date, episode, characters{id, name, status, species, type, gender, origin{id},location{id}, image, episode{id}, created}, created }}}")
            data = json.loads(response.text.encode("utf-8"))
            episodio = data["data"]["episodes"]["results"]
            for episode in episodio:
                if queryset in episode["name"]:
                    new_episode = Episode(episode["id"], episode["name"], episode["air_date"], episode["episode"], episode["characters"], episode["created"])
                    lista_resultados_episodios.append(new_episode)
        print(lista_resultados_episodios)
        response = requests.get("https://integracion-rick-morty-api.herokuapp.com/graphql/?query={characters{info{pages},results{id}}}")
        data = json.loads(response.text.encode("utf-8"))
        for x in range(0, data["data"]["characters"]["info"]["pages"]):
            pagina = str(x+1)
            response = requests.get("https://integracion-rick-morty-api.herokuapp.com/graphql/?query={characters(page:"+pagina+"){info{pages},results{id, name, status, species, type, gender, origin{id},location{id}, image, episode{id}, created}}}")
            data = json.loads(response.text.encode("utf-8"))
            personajes = data["data"]["characters"]["results"]
            
            for personaje in personajes:
                if queryset in personaje["name"]:
                    new_character = Character(personaje["id"], personaje["name"],personaje["status"],personaje["species"],personaje["type"], personaje["gender"],personaje["origin"],personaje["location"], personaje["image"], personaje["episode"], personaje["url"])
                    lista_resultados_personajes.append(new_character)
        print(lista_resultados_personajes)

        response = requests.get("https://integracion-rick-morty-api.herokuapp.com/graphql/?query={locations{info{pages},results{id}}}")
        data = json.loads(response.text.encode("utf-8"))

        for x in range(0, data["data"]["locations"]["info"]["pages"]):
            pagina = str(x+1)
            response = requests.get("https://integracion-rick-morty-api.herokuapp.com/graphql/?query={locations(page:"+pagina+"){info{count},results{id, name, type, dimension, residents{id}, created}}}")
            data = json.loads(response.text.encode("utf-8"))
            locacion = data["data"]["locations"]["results"]
            for lugar in locacion:
                if queryset in lugar["name"]:
                    new_location = Location(lugar["name"], lugar["url"])
                    new_location.dimension = lugar["dimension"]
                    new_location.tipo = lugar["type"]
                    new_location.personajes = lugar["residents"]
                    new_location.id = lugar["id"]
                    lista_resultados_lugares.append(new_location)
        print(lista_resultados_lugares)
        document = principal_template.render({"episodios":episode_list, "busqueda_personajes": lista_resultados_personajes, "busqueda_episodios": lista_resultados_episodios, "busqueda_lugares":lista_resultados_lugares})
    return HttpResponse(document)

def episode(request, id):
    url = "https://integracion-rick-morty-api.herokuapp.com/graphql/?query={episode(id:"+id+"){id, name, air_date, episode, characters{id, name, status, species, type, gender, origin{id},location{id}, image, episode{id}, created}, created }}"
    response = requests.get(url)
    data = json.loads(response.text.encode("utf-8"))
    datos = data["data"]["episode"]
    information_list = []
    characters_list = []
    information_list.append(datos["id"])
    information_list.append(datos["name"])
    information_list.append(datos["air_date"])
    information_list.append(datos["episode"])
    for personaje in datos["characters"]:    
        new_character = Character(personaje["id"], personaje["name"],personaje["status"],personaje["species"],personaje["type"], personaje["gender"],personaje["origin"],personaje["location"], personaje["image"], personaje["episode"], personaje["created"])
        characters_list.append(new_character)
    information_list.append(information_list)
    episode_template = get_template("episodio.html")
    document = episode_template.render({"episodio":information_list, "lista_personajes":characters_list})
    return HttpResponse(document)
    
def character(request, id):
    url = "https://integracion-rick-morty-api.herokuapp.com/graphql/?query={character(id:"+id+"){id, name, status, species, type, gender, origin{id, name},location{id, name}, image, episode{id, name, air_date, episode, characters{id}, created}, created}}"
    response = requests.get(url)
    data = json.loads(response.text.encode("utf-8"))
    data = data["data"]["character"]
    information_list = []
    episode_list = []
    information_list.append(data["name"])
    information_list.append(data["status"])
    information_list.append(data["species"])
    information_list.append(data["type"])
    information_list.append(data["gender"])
    imagen = data["image"]
    lugar_origen = Location(data["origin"]["id"], data["origin"]["name"])
    lugar_locacion = Location(data["location"]["id"], data["location"]["name"])
    for episodio in data["episode"]:
        new_episode = Episode(episodio["id"], episodio["name"], episodio["air_date"], episodio["episode"], episodio["characters"], episodio["created"])
        episode_list.append(new_episode)
    character_template = get_template("personaje.html")
    document = character_template.render({"personaje":information_list, "lista_episodios":episode_list, "imagen": imagen, "lugar": lugar_origen, "location": lugar_locacion})
    return HttpResponse(document)

def locations(request, id):
    url = "https://integracion-rick-morty-api.herokuapp.com/graphql/?query={location(id:"+id+"){id, name, type, dimension, residents{id, name, status, species, type, gender, origin{id, name},location{id, name}, image, episode{id, name, air_date, episode, characters{id}, created}, created}}}"
    response = requests.get(url)
    data = response.json()
    data = data["data"]["location"]
    new_location = Location(data["id"], data["name"])
    new_location.dimension = data["dimension"]
    new_location.tipo = data["type"]
    new_location.personajes = data["residents"]
    new_location.id = data["id"]
    character_list = []
    for personaje in new_location.personajes:
        data = personaje
        new_character = Character(data["id"], data["name"],data["status"],data["species"],data["type"], data["gender"],data["origin"],data["location"], data["image"], data["episode"], data["created"])
        character_list.append(new_character)
    character_template = get_template("lugar.html")
    document = character_template.render({"lugar":new_location, "lista_personajes":character_list})
    return HttpResponse(document)


