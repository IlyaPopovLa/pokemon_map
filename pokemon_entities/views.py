import os
import folium
from django.http import HttpResponseNotFound
from django.shortcuts import render, get_object_or_404
from django.conf import settings
from .models import Pokemon, PokemonEntity


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_path=None):
    if image_path and os.path.exists(image_path):
        icon = folium.features.CustomIcon(
            image_path,
            icon_size=(50, 50),
        )
    else:
        icon = folium.Icon(icon='info-sign', color='blue')

    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    pokemon_entities = PokemonEntity.objects.all()

    for pokemon_entity in pokemon_entities:
        image_path = None
        if pokemon_entity.pokemon.image:
            # Получаем абсолютный путь к файлу
            image_path = pokemon_entity.pokemon.image.path

        add_pokemon(
            folium_map,
            pokemon_entity.lat,
            pokemon_entity.lon,
            image_path
        )

    pokemons_on_page = []
    for pokemon in Pokemon.objects.all():
        if pokemon.image:
            img_url = request.build_absolute_uri(pokemon.image.url)
        else:
            img_url = DEFAULT_IMAGE_URL

        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': img_url,
            'title_ru': pokemon.title,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    pokemon = get_object_or_404(Pokemon, id=pokemon_id)

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    pokemon_entities = PokemonEntity.objects.filter(pokemon=pokemon)

    for entity in pokemon_entities:
        image_path = pokemon.image.path if pokemon.image else None
        add_pokemon(
            folium_map,
            entity.lat,
            entity.lon,
            image_path
        )

    pokemon_data = {
        'pokemon_id': pokemon.id,
        'img_url': request.build_absolute_uri(pokemon.image.url) if pokemon.image else DEFAULT_IMAGE_URL,
        'title_ru': pokemon.title,
        'title_en': pokemon.title_en,
        'title_jp': pokemon.title_jp,
        'description': pokemon.description,
    }

    if pokemon.previous_evolution:
        prev_evolution_img = request.build_absolute_uri(
            pokemon.previous_evolution.image.url
        ) if pokemon.previous_evolution.image else DEFAULT_IMAGE_URL

        pokemon_data['previous_evolution'] = {
            'title_ru': pokemon.previous_evolution.title,
            'pokemon_id': pokemon.previous_evolution.id,
            'img_url': prev_evolution_img
        }

    next_evolutions = pokemon.next_evolutions.all()
    if next_evolutions:
        next_evolution = next_evolutions.first()
        next_evolution_img = request.build_absolute_uri(
            next_evolution.image.url
        ) if next_evolution.image else DEFAULT_IMAGE_URL

        pokemon_data['next_evolution'] = {
            'title_ru': next_evolution.title,
            'pokemon_id': next_evolution.id,
            'img_url': next_evolution_img
        }

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(),
        'pokemon': pokemon_data
    })