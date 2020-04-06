from django.http import HttpResponse
from django.template import Template, Context
from django.template.loader import get_template
from django.shortcuts import render
import requests
import json


class Episode:

    def __init__(self, ident, name, air_date, episode, characters, url, created):
        self.id = ident
        self.name = name
        self.air_date = air_date
        self.episode = episode
        self.characters = characters
        self.url = "https://integracion-rick-morty-api.herokuapp.com/api/episode{}".format(id)
        self.created = created

class Character:

    def __init__(self, ident, name, status, species, tipo, gender, origin, location, image, episode, url):
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
        self.url = url

class Location:
    
    def __init__(self, name, url):
        self.name = name
        self.url = url
        self.dimension = ""
        self.tipo = ""
        self.personajes = []
        self.id = ""

def principal(request):
    response = requests.get(f"https://integracion-rick-morty-api.herokuapp.com/api/episode/")
    data = json.loads(response.text.encode("utf-8"))
    data = data["results"]
    episode_list = []
    for episode in data:
        new_episode = Episode(episode["id"], episode["name"], episode["air_date"], episode["episode"], episode["characters"], episode["url"], episode["created"])
        episode_list.append(new_episode)
    response = requests.get(f"https://integracion-rick-morty-api.herokuapp.com/api/episode/?page=2")
    data = json.loads(response.text.encode("utf-8"))
    data = data["results"]
    for episode in data:
        new_episode = Episode(episode["id"], episode["name"], episode["air_date"], episode["episode"], episode["characters"], episode["url"], episode["created"])
        episode_list.append(new_episode)
    principal_template = get_template("principal.html")
    document = principal_template.render({"episodios":episode_list})
    queryset = request.GET.get("buscar")
    if queryset:
        lista_resultados_episodios = []
        lista_resultados_personajes = []
        lista_resultados_lugares = []
        print(queryset)
        print("ahyak")
        response = requests.get(f"https://integracion-rick-morty-api.herokuapp.com/api/episode")
        data = json.loads(response.text.encode("utf-8"))
        data = data["results"]
        for episode in data:
            if queryset in episode["name"]:
                new_episode = Episode(episode["id"], episode["name"], episode["air_date"], episode["episode"], episode["characters"], episode["url"], episode["created"])
                lista_resultados_episodios.append(new_episode)
        response = requests.get(f"https://integracion-rick-morty-api.herokuapp.com/api/episode/?page=2")
        data = json.loads(response.text.encode("utf-8"))
        data = data["results"]
        for episode in data:
            if queryset in episode["name"]:
                new_episode = Episode(episode["id"], episode["name"], episode["air_date"], episode["episode"], episode["characters"], episode["url"], episode["created"])
                lista_resultados_episodios.append(new_episode)
    
        response = requests.get(f"https://integracion-rick-morty-api.herokuapp.com/api/character")
        data = json.loads(response.text.encode("utf-8"))
        data = data["results"]
        for personaje in data:
            if queryset in personaje["name"]:
                new_character = Character(personaje["id"], personaje["name"],personaje["status"],personaje["species"],personaje["type"], personaje["gender"],personaje["origin"],personaje["location"], personaje["image"], personaje["episode"], personaje["url"])
                lista_resultados_personajes.append(new_character)
        for x in range(2,20):
            url = "https://integracion-rick-morty-api.herokuapp.com/api/character/?page="+str(x)
            response = requests.get(url)
            data = json.loads(response.text.encode("utf-8"))
            data = data["results"]
            for personaje in data:
                if queryset in personaje["name"]:
                    new_character = Character(personaje["id"], personaje["name"],personaje["status"],personaje["species"],personaje["type"], personaje["gender"],personaje["origin"],personaje["location"], personaje["image"], personaje["episode"], personaje["url"])
                    lista_resultados_personajes.append(new_character)
        
        response = requests.get(f"https://integracion-rick-morty-api.herokuapp.com/api/location")
        data = json.loads(response.text.encode("utf-8"))
        data = data["results"]
        for lugar in data:
            if queryset in lugar["name"]:
                new_location = Location(lugar["name"], lugar["url"])
                new_location.dimension = lugar["dimension"]
                new_location.tipo = lugar["type"]
                new_location.personajes = lugar["residents"]
                new_location.id = lugar["id"]
                lista_resultados_lugares.append(new_location)
        for x in range(2,4):
            url = "https://integracion-rick-morty-api.herokuapp.com/api/location/?page="+str(x)
            response = requests.get(url)
            data = json.loads(response.text.encode("utf-8"))
            data = data["results"]
            for lugar in data:
                if queryset in lugar["name"]:
                    new_location = Location(lugar["name"], lugar["url"])
                    new_location.dimension = lugar["dimension"]
                    new_location.tipo = lugar["type"]
                    new_location.personajes = lugar["residents"]
                    new_location.id = lugar["id"]
                    lista_resultados_lugares.append(new_location)
        document = principal_template.render({"episodios":episode_list, "busqueda_personajes": lista_resultados_personajes, "busqueda_episodios": lista_resultados_episodios, "busqueda_lugares":lista_resultados_lugares})
    return HttpResponse(document)

def episode(request, id):
    url = "https://integracion-rick-morty-api.herokuapp.com/api/episode/"+id
    response = requests.get(url)
    data = json.loads(response.text.encode("utf-8"))
    information_list = []
    characters_list = []
    information_list.append(data["name"])
    information_list.append(data["air_date"])
    information_list.append(data["episode"])
    for personaje in data["characters"]:    
        response = requests.get(personaje)
        data = json.loads(response.text.encode("utf-8"))
        new_character = Character(data["id"], data["name"],data["status"],data["species"],data["type"], data["gender"],data["origin"],data["location"], data["image"], data["episode"], data["url"])
        characters_list.append(new_character)
    information_list.append(information_list)
    episode_template = get_template("episodio.html")
    document = episode_template.render({"episodio":information_list, "lista_personajes":characters_list})
    return HttpResponse(document)
    
def character(request, id):
    url = "https://integracion-rick-morty-api.herokuapp.com/api/character/"+id
    response = requests.get(url)
    data = json.loads(response.text.encode("utf-8"))
    information_list = []
    episode_list = []
    information_list.append(data["name"])
    information_list.append(data["status"])
    information_list.append(data["species"])
    information_list.append(data["type"])
    information_list.append(data["gender"])
    imagen = data["image"]
    lugar_origen = Location(data["origin"]["name"],data["origin"]["url"])
    respuesta = requests.get(data["origin"]["url"])
    datos = json.loads(respuesta.text.encode("utf-8"))
    lugar_origen.id = datos["id"]
    lugar_locacion = Location(data["location"]["name"], data["location"]["url"])
    response = requests.get(data["location"]["url"])
    datoss = json.loads(response.text.encode("utf-8"))
    lugar_locacion.id = datoss["id"]
    for episodio in data["episode"]:
        response = requests.get(episodio)
        data = json.loads(response.text.encode("utf-8"))
        new_episode = Episode(data["id"], data["name"], data["air_date"], data["episode"], data["characters"], data["url"], data["created"])
        episode_list.append(new_episode)
    character_template = get_template("personaje.html")
    document = character_template.render({"personaje":information_list, "lista_episodios":episode_list, "imagen": imagen, "lugar": lugar_origen, "location": lugar_locacion})
    return HttpResponse(document)

def locations(request, id):
    url = "https://integracion-rick-morty-api.herokuapp.com/api/location/"+id
    response = requests.get(url)
    data = json.loads(response.text.encode("utf-8"))
    new_location = Location(data["name"], data["url"])
    new_location.dimension = data["dimension"]
    new_location.tipo = data["type"]
    new_location.personajes = data["residents"]
    new_location.id = data["id"]
    character_list = []
    for personaje in new_location.personajes:
        response = requests.get(personaje)
        data = json.loads(response.text.encode("utf-8"))
        new_character = Character(data["id"], data["name"],data["status"],data["species"],data["type"], data["gender"],data["origin"],data["location"], data["image"], data["episode"], data["url"])
        character_list.append(new_character)
    character_template = get_template("lugar.html")
    document = character_template.render({"lugar":new_location, "lista_personajes":character_list})
    return HttpResponse(document)


