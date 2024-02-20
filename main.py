import requests
import pandas as pd
import json


def get_pokemon_data(number):
    url = f"http://pokeapi.co/api/v2/pokemon/{number}/"
    payload = ""
    response = requests.request("GET", url, data=payload)
    data = response.json()
    return data


def all_pokemon_data_to_df():
    df = pd.DataFrame(columns=['id', 'name'])
    for i in range(1, 10):
        pokemon = get_pokemon_data(i)
        pokemon_normalized = pd.json_normalize(pokemon)[['id', 'name']]
        df = pd.concat([df, pokemon_normalized])
    return df



print(all_pokemon_data_to_df())

