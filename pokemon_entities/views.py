import folium
import json

from django.http import HttpResponseNotFound
from django.shortcuts import render
from .models import PokemonEntity
from django.utils.timezone import localtime, now
import datetime


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):    
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    tomorrow_day = localtime(now()).date()+datetime.timedelta(days=1)
    today_day=localtime(now()).date()
    pokemons = PokemonEntity.objects.filter(disappered_data__gte=tomorrow_day, appeared_date__gte=today_day)
    for pokemon_entity in pokemons:
        add_pokemon(
            folium_map, pokemon_entity.lat,
            pokemon_entity.lon,
            request.build_absolute_uri(pokemon_entity.pokemon.photo.url)
        )

    pokemons_on_page = []
    for pokemon_entity in pokemons:
        pokemons_on_page.append({
            'pokemon_id': pokemon_entity.id,
            'img_url': pokemon_entity.pokemon.photo.url,
            'title_ru': pokemon_entity.pokemon.title_ru,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):

    pokemons = PokemonEntity.objects.filter(id=pokemon_id)
    for pokemon in pokemons:
        requested_pokemon = pokemon
        break
    else:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    add_pokemon(
        folium_map, requested_pokemon.lat,
        requested_pokemon.lon,
        request.build_absolute_uri(requested_pokemon.pokemon.photo.url)
    )

    previous_pokemon = requested_pokemon.pokemon.previous_evolution
    previous_pokemon_dict = {}
    if previous_pokemon != None:
        previous_pokemon_dict = {
            'title_ru': previous_pokemon.title_ru, 
            'pokemon_id': previous_pokemon.id, 
            'img_url': previous_pokemon.photo.url
        }

    # print(previous_pokemon.id)
    # print(type(previous_pokemon))

    # with open('pokemon_entities/pokemons.json', encoding='utf-8') as database:
    #     pokemons_json = json.load(database)['pokemons']
    # previous_evolution = {}    
    # for pokemon_json in pokemons_json:
    #     if pokemon_json.get("previous_evolution") != None:           
    #         previous_evolution[pokemon_json.get("title_ru")] = pokemon_json.get("previous_evolution")
    # try:
    #     previous_evolution_pokemon = previous_evolution[requested_pokemon.pokemon.title_ru]
    # except KeyError:
    #     previous_evolution_pokemon = None
    # print(previous_evolution_pokemon)
    # for key in previous_evolution:
    #     if previous_evolution[key]['title_ru'] == requested_pokemon.pokemon.title_ru:
    #         next_evolution_pokemon_key = key
    #         break
    # else:
    #     next_evolution_pokemon = None

    # for pokemon_json in pokemons_json:
    #     if pokemon_json.get("title_ru") == next_evolution_pokemon_key:
    #         next_evolution_pokemon = pokemon_json
    #         break      

    # print("!!!")
    # print(previous_evolution_pokemon)
    # print(type(previous_evolution_pokemon))
    pokemons_on_page = {
        'pokemon_id': requested_pokemon.id,
        'title_ru': requested_pokemon.pokemon.title_ru,
        "title_en": requested_pokemon.pokemon.title_en,
        "title_jp": requested_pokemon.pokemon.title_jp,
        'img_url': requested_pokemon.pokemon.photo.url,
        "description": requested_pokemon.pokemon.description,
        "previous_evolution": previous_pokemon_dict
    }

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemons_on_page
    })
