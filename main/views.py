from django.shortcuts import render
from .services import get_seasons, get_episodes, get_episode_by_id, get_character_by_name, get_characters_by_search, get_quotes_by_author
import datetime


def seasons(request):
    seasons_bb_list = get_seasons(params={"series": "Breaking Bad"})
    seasons_bcs_list = get_seasons(params={"series": "Better Call Saul"})
    if seasons_bb_list == '429 ERROR' or seasons_bcs_list == '429 ERROR':
        context = {
            'error_message': 'Lo siento, la API ha superado el límite de consultas, pruebe de nuevo más tarde.'
        }
    else:
        context = {
            'seasons_bb_list': seasons_bb_list,
            'seasons_bcs_list': seasons_bcs_list,
        }
    return render(request, 'main/seasons.html', context)


def episodes(request, series, season):
    episodes_zip = get_episodes(params={"series": series, "season": season})
    if episodes_zip == '429 ERROR':
        context = {
            'error_message': 'Lo siento, la API ha superado el límite de consultas, pruebe de nuevo más tarde.'
        }
    else:
        context = {
            'series': series,
            'season': season,
            'episodes_zip': episodes_zip,
        }
    return render(request, 'main/episodes.html', context)


def episode_detail(request, episode_id):
    episode_detail = get_episode_by_id(episode_id)
    if episode_detail:
        if episode_detail == '429 ERROR':
            context = {
                'error_message': 'Lo siento, la API ha superado el límite de consultas, pruebe de nuevo más tarde.'
        }
        else:
            episode_detail = episode_detail[0]
            context = {
                'episode_id': episode_detail['episode_id'],
                'title': episode_detail['title'],
                'season': episode_detail['season'],
                'air_date': datetime.datetime.strptime(episode_detail['air_date'],"%Y-%m-%dT%H:%M:%S.%fZ"),
                'characters': episode_detail['characters'],
                'episode': episode_detail['episode'],
                'series': episode_detail['series'],
            }
    else:
        context = {
            'episode_id': None,
        }
    return render(request, 'main/episode_detail.html', context)


def character_detail(request, name):
    character_detail = get_character_by_name(params={'name': name})
    if character_detail:
        if character_detail == '429 ERROR':
            context = {
                'error_message': 'Lo siento, la API ha superado el límite de consultas, pruebe de nuevo más tarde.'
        }
        else:
            character_detail = character_detail[0]

            quotes_info = get_quotes_by_author(params={'author': name})
            quotes = [elem['quote'] for elem in quotes_info]

            context = {
                'char_id': character_detail['char_id'],
                'name': character_detail['name'],
                'occupation': character_detail['occupation'],
                'img': character_detail['img'],
                'status': character_detail['status'],
                'nickname': character_detail['nickname'],
                'appearance': character_detail['appearance'],
                'portrayed': character_detail['portrayed'],
                'category': character_detail['category'],
                'better_call_saul_appearance': character_detail['better_call_saul_appearance'],
                'quotes': quotes,
            }
    else:
        context = {
            'char_id': None,
        }
    return render(request, 'main/character_detail.html', context)

def character_list(request):
    name = request.POST.get('name', '')
    if name:
        characters_list = get_characters_by_search(params={'name': name})
        if characters_list == '429 ERROR':
            context = {
                'error_message': 'Lo siento, la API ha superado el límite de consultas, pruebe de nuevo más tarde.'
        }
        else:
            context = {
                'characters_list': characters_list,
            }
    else:
        context = {
            'characters_list': None,
        }
    return render(request, 'main/character_list.html', context)