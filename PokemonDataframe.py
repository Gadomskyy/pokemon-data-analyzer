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


def get_primary_types(pokemon):
    df = pd.json_normalize(pokemon['types'])
    primary_type = df[f'type.name'].tolist()[0]
    return primary_type

def get_secondary_types(pokemon):
    df = pd.json_normalize(pokemon['types'])
    primary_type = df[f'type.name'].tolist()
    if len(primary_type) > 1:
        return primary_type[1]
    else:
        return None

def get_forms(pokemon):
    df = pd.json_normalize(pokemon['forms'])
    forms = df['name'].tolist()
    return forms


def get_stat(pokemon, name):
    df = pd.json_normalize(pokemon['stats'])
    stat = df.loc[df['stat.name'] == name, 'base_stat'].iloc[0]
    return stat


def get_generation(id):
    if id <= 151:
        return 1
    elif id <= 251:
        return 2
    elif id <= 386:
        return 3
    elif id <= 493:
        return 4
    elif id <= 649:
        return 5
    elif id <= 721:
        return 6
    elif id <= 809:
        return 7
    elif id <= 905:
        return 8
    elif id <= 1025:
        return 9
    else:
        return 0


def all_pokemon_data_to_df():
    pokemon_number = 1025

    df = pd.DataFrame(
        columns=['name',
                 'height',
                 'weight',
                 'generation',
                 'moves',
                 'forms',
                 'hp',
                 'attack',
                 'defense',
                 'special_attack',
                 'special_defense',
                 'speed',
                 'abilities',
                 'primary_type',
                 'secondary_type'])
    for i in range(1, pokemon_number + 1):
        pokemon = get_pokemon_data(i)
        pokemon_normalized = pd.json_normalize(pokemon)[
            ['name',
             'height',
             'weight']]
        pokemon_normalized['generation'] = [get_generation(i)]
        pokemon_normalized['moves'] = [get_attribute_names(pokemon, 'moves', 'move')]
        pokemon_normalized['forms'] = [get_forms(pokemon)]
        pokemon_normalized['hp'] = get_stat(pokemon, 'hp')
        pokemon_normalized['attack'] = get_stat(pokemon, 'attack')
        pokemon_normalized['defense'] = get_stat(pokemon, 'defense')
        pokemon_normalized['special_attack'] = get_stat(pokemon, 'special-attack')
        pokemon_normalized['special_defense'] = get_stat(pokemon, 'special-defense')
        pokemon_normalized['speed'] = get_stat(pokemon, 'speed')
        pokemon_normalized['abilities'] = [get_attribute_names(pokemon, 'abilities', 'ability')]
        pokemon_normalized['primary_type'] = [get_primary_types(pokemon)]
        pokemon_normalized['secondary_type'] = [get_secondary_types(pokemon)]
        df = pd.concat([df, pokemon_normalized])
        df.reset_index(drop=True, inplace=True)
        df.index += 1
        df.index.rename('id', inplace=True)
    return df


all_pokemon_data_to_df().to_excel("result.xlsx")
