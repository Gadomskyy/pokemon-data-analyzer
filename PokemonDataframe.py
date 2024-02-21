import requests
import pandas as pd


def get_pokemon_data(number):
    url = f"http://pokeapi.co/api/v2/pokemon/{number}/"
    payload = ""
    response = requests.request("GET", url, data=payload)
    data = response.json()
    return data

def get_ability_names(pokemon):
    abilities_df = pd.json_normalize(pokemon['abilities'])
    ability_names = abilities_df['ability.name'].tolist()
    return ability_names


def all_pokemon_data_to_df():
    df = pd.DataFrame(
        columns=['id',
                 'name',
                 'height',
                 'weight',
                 'forms',
                 'moves',
                 'stats',
                 'types',
                 'abilities'])
    for i in range(1, 10):
        pokemon = get_pokemon_data(i)
        pokemon_normalized = pd.json_normalize(pokemon)[
            ['id',
             'name',
             'height',
             'weight',
             'forms',
             'moves',
             'stats',
             'types']]
        pokemon_normalized['abilities'] = [get_ability_names(pokemon)]
        df = pd.concat([df, pokemon_normalized])
    return df

all_pokemon_data_to_df().to_excel("result.xlsx")
