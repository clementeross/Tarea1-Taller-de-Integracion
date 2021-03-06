import requests


API_URL = 'https://tarea-1-breaking-bad.herokuapp.com/api/'


def generate_request(url, params={}):
    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()
    
    elif response.status_code == 429:
        return '429 ERROR'


def get_seasons(params={}):
    episodes = generate_request("%sepisodes" % API_URL, params)
    if episodes == '429 ERROR':
        return '429 ERROR'
    last_season = int(episodes[-1]["season"])
    seasons_list = [i for i in range(1, last_season + 1)]
    return seasons_list


def get_episodes(params={}):
    episodes = generate_request("%sepisodes" % API_URL, {'series': params['series']})
    if episodes == '429 ERROR':
        return '429 ERROR'
    filter_episodes = list(filter(lambda elem: int(elem["season"]) == params["season"], episodes))
    episodes_titles = [elem["title"] for elem in filter_episodes]
    episodes_id = [elem["episode_id"] for elem in filter_episodes]
    return list(zip(episodes_titles, episodes_id))


def get_episode_by_id(episode_id, params={}):
    episode_detail = generate_request("%sepisodes/%s" % (API_URL, episode_id), params)
    if episode_detail == '429 ERROR':
        return '429 ERROR'
    return episode_detail


def get_character_by_name(params={}):
    character_detail = generate_request("%scharacters" % API_URL, params)
    if character_detail == '429 ERROR':
        return '429 ERROR'
    return character_detail


def get_quotes_by_author(params={}):
    quotes = generate_request("%squote" % API_URL, params)
    if quotes == '429 ERROR':
        return '429 ERROR'
    return quotes


def get_characters_by_search(params={}):
    params['limit'] = 10
    params['offset'] = 0
    characters_list = []
    while True:
        sample_list = generate_request("%scharacters" % API_URL, params)
        if sample_list == '429 ERROR':
            return '429 ERROR'
        characters_list += sample_list
        if len(sample_list) < 10:
            break
        else:
            params['offset'] += 10
    return [elem['name'] for elem in characters_list]
