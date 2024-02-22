import requests
import pandas as pd


def get_pokemon_data(number):
    url = f"http://pokeapi.co/api/v2/pokemon/{number}/"
    payload = ""
    response = requests.request("GET", url, data=payload)
    data = response.json()
    return data

def get_attribute_names(pokemon, attribute, attribute2):
    df = pd.json_normalize(pokemon[attribute])
    attribute_names = df[f'{attribute2}.name'].tolist()
    return attribute_names

def get_forms(pokemon):
    df = pd.json_normalize(pokemon['forms'])
    forms = df['name'].tolist()
    return forms

def get_stats(pokemon):
    df = pd.json_normalize(pokemon['stats'])
    dict_list = [{'stat': stat, 'value': value} for stat, value in zip(df['stat.name'], df['base_stat'])]
    return dict_list


def all_pokemon_data_to_df():
    df = pd.DataFrame(
        columns=['name',
                 'height',
                 'weight',
                 'stats',
                 'abilities',
                 'types'])
    for i in range(1, 10):
        pokemon = get_pokemon_data(i)
        pokemon_normalized = pd.json_normalize(pokemon)[
            ['name',
             'height',
             'weight']]
        pokemon_normalized['abilities'] = [get_attribute_names(pokemon, 'abilities', 'ability')]
        pokemon_normalized['types'] = [get_attribute_names(pokemon, 'types', 'type')]
        pokemon_normalized['moves'] = [get_attribute_names(pokemon, 'moves', 'move')]
        pokemon_normalized['forms'] = [get_forms(pokemon)]
        pokemon_normalized['stats'] = [get_stats(pokemon)]
        df = pd.concat([df, pokemon_normalized])
        df.reset_index(drop=True, inplace=True)
        df.index += 1
        df.index.rename('id', inplace=True)
    return df

