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
            'title_ru': pokemon_entity.pokemon.title,
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
    print(requested_pokemon.pokemon.title)
    add_pokemon(
        folium_map, requested_pokemon.lat,
        requested_pokemon.lon,
        request.build_absolute_uri(requested_pokemon.pokemon.photo.url)
    )

    pokemons_on_page = {
        'pokemon_id': requested_pokemon.id,
        'title_ru': requested_pokemon.pokemon.title,
        'img_url': requested_pokemon.pokemon.photo.url,
        "description": requested_pokemon.pokemon.description
    }

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemons_on_page
    })
