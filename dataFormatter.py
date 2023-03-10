#Reads through the different yaml files and creates a csv file with the data
import yaml
import csv

#Reads through the yaml file and returns a list of dictionaries
def readYamlFile(fileName):
    with open(fileName, 'r') as file:
        return yaml.safe_load(file)
def getGames():
    releases = readYamlFile("Data/releases.yaml")
    games = []
    for key, value in releases.items():
        games.append(value)
    return games
def getPokemonData():
    #Format Pokemon
    pokedex = readYamlFile("Data/pokemon-forms.yaml")
    pokemon = []
    for key, value in pokedex.items():
        #Check if name is already in pokemon, and can only be added if the preceding pokemon is galar/alolan forms
        if value['pokemonid'] not in [x['Name'] for x in pokemon]:
            #New Name Check if it is a galar/alolan form
            if(value['formid'] != None):
                if('mega' not in value['formid'] and 'eternamax' not in value['formid']):
                    pokemon.append({"Name": value['pokemonid'].title(), "Type1": value['type1'], "Type2": value['type2'], "Generation": value['gen'], "Weight": value['weight'], "Height": value['height']})
            else:
                pokemon.append({"Name": value['pokemonid'].title(), "Type1": value['type1'], "Type2": value['type2'], "Generation": value['gen'], "Weight": value['weight'], "Height": value['height']})
    return pokemon
def getTypeData():
    types = [{"Type": "Normal", "Weaknesses": ["Fighting"], "Resistances": [], "Immunities": ["Ghost"]},
            {"Type": "Fire", "Weaknesses": ["Water", "Ground", "Rock"], "Resistances": ["Fire", "Grass", "Ice", "Bug", "Steel", "Fairy", "Fighting", "Dragon"], "Immunities": []},
            {"Type": "Water", "Weaknesses": ["Electric", "Grass"], "Resistances": ["Water", "Fire", "Ice", "Steel"], "Immunities": []},
            {"Type": "Electric", "Weaknesses": ["Ground"], "Resistances": ["Electric", "Flying", "Steel"], "Immunities": []},
            {"Type": "Grass", "Weaknesses": ["Fire", "Ice", "Poison", "Flying", "Bug"], "Resistances": ["Water", "Electric", "Grass", "Ground"], "Immunities": []},
            {"Type": "Ice", "Weaknesses": ["Fire", "Fighting", "Rock", "Steel"], "Resistances": ["Ice"], "Immunities": []},
            {"Type": "Fighting", "Weaknesses": ["Flying", "Psychic", "Fairy"], "Resistances": ["Bug", "Rock", "Dark"], "Immunities": ["Ghost"]},
            {"Type": "Poison", "Weaknesses": ["Ground", "Psychic"], "Resistances": ["Fighting", "Poison", "Grass", "Fairy"], "Immunities": []},
            {"Type": "Ground", "Weaknesses": ["Water", "Grass", "Ice"], "Resistances": ["Poison", "Rock"], "Immunities": ["Electric"]},
            {"Type": "Flying", "Weaknesses": ["Electric", "Ice", "Rock"], "Resistances": ["Grass", "Fighting", "Bug"], "Immunities": ["Ground"]},
            {"Type": "Psychic", "Weaknesses": ["Bug", "Ghost", "Dark"], "Resistances": ["Fighting", "Psychic"], "Immunities": []},
            {"Type": "Bug", "Weaknesses": ["Fire", "Flying", "Rock"], "Resistances": ["Grass", "Fighting", "Ground"], "Immunities": []},
            {"Type": "Rock", "Weaknesses": ["Water", "Grass", "Fighting", "Ground", "Steel"], "Resistances": ["Normal", "Fire", "Poison", "Flying"], "Immunities": []},
            {"Type": "Ghost", "Weaknesses": ["Ghost", "Dark"], "Resistances": ["Poison", "Bug"], "Immunities": ["Normal", "Fighting"]},
            {"Type": "Dragon", "Weaknesses": ["Ice", "Dragon", "Fairy"], "Resistances": ["Fire", "Water", "Electric", "Grass"], "Immunities": []},
            {"Type": "Dark", "Weaknesses": ["Fighting", "Bug", "Fairy"], "Resistances": ["Ghost", "Dark"], "Immunities": ["Psychic"]},
            {"Type": "Steel", "Weaknesses": ["Fire", "Fighting", "Ground"], "Resistances": ["Normal", "Grass", "Ice", "Flying", "Psychic", "Bug", "Rock", "Dragon", "Steel", "Fairy"], "Immunities": ["Poison"]},
            {"Type": "Fairy", "Weaknesses": ["Poison", "Steel"], "Resistances": ["Fighting", "Bug", "Dark"], "Immunities": ["Dragon"]}
            ]
    typenames = [x['Type'] for x in types]
    return typenames, types