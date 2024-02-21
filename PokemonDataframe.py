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


def all_pokemon_data_to_df():
    df = pd.DataFrame(
        columns=['id',
                 'name',
                 'height',
                 'weight',
                 'forms',
                 'stats',
                 'abilities',
                 'types'])
    for i in range(1, 10):
        pokemon = get_pokemon_data(i)
        pokemon_normalized = pd.json_normalize(pokemon)[
            ['id',
             'name',
             'height',
             'weight',
             'forms',
             'stats']]
        pokemon_normalized['abilities'] = [get_attribute_names(pokemon, 'abilities', 'ability')]
        pokemon_normalized['types'] = [get_attribute_names(pokemon, 'types', 'type')]
        pokemon_normalized['moves'] = [get_attribute_names(pokemon, 'moves', 'move')]
        df = pd.concat([df, pokemon_normalized])
    return df

all_pokemon_data_to_df().to_excel("result.xlsx")
