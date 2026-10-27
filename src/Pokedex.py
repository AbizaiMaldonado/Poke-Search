
"""
POKEDEX INTERACTIVE - VERSION 1.1
Data source: PokeAPI
Interface: Terminal
Supported languages: English and Spanish
"""

import requests

API_URL = "https://pokeapi.co/api/v2"
TIMEOUT = 10

session = requests.Session()
cache = {}

LANGUAGES = {
    "en": {
        "name": "English",
        "menu": "POKEDEX INTERACTIVE",
        "search": "Search Pokemon",
        "language": "Change language",
        "info": "Project information",
        "exit": "Exit",
        "choice": "Select an option: ",
        "query": "Enter Pokemon name or ID: ",
        "invalid": "Invalid option. Try again.",
        "empty": "Please enter a Pokemon name or ID.",
        "not_found": "Pokemon not found.",
        "connection": "Connection error. Check your internet connection.",
        "api_error": "Unable to retrieve data from PokeAPI.",
        "loading": "Searching...",
        "goodbye": "Closing the Pokedex. Goodbye!",
        "language_title": "SELECT LANGUAGE",
        "language_changed": "Language changed to English.",
        "select_language": "Select language: ",
        "back": "Return to main menu",
        "number": "National Pokedex number",
        "category": "Category",
        "types": "Type(s)",
        "height": "Height",
        "weight": "Weight",
        "generation": "Generation",
        "region": "Origin region",
        "abilities": "ABILITIES",
        "stats": "BASE STATS",
        "description": "POKEDEX DESCRIPTION",
        "regional": "REGIONAL POKEDEX NUMBERS",
        "unavailable": "Not available",
        "no_description": "No description available.",
        "no_data": "No data available.",
        "hidden": "Hidden",
        "project_info": "PROJECT INFORMATION",
        "version": "Version",
        "source": "Data source",
        "interface": "Interface",
        "metric_height": "m",
        "metric_weight": "kg"
    },
    "es": {
        "name": "Espanol",
        "menu": "POKEDEX INTERACTIVA",
        "search": "Buscar Pokemon",
        "language": "Cambiar idioma",
        "info": "Informacion del proyecto",
        "exit": "Salir",
        "choice": "Selecciona una opcion: ",
        "query": "Introduce el nombre o ID del Pokemon: ",
        "invalid": "Opcion no valida. Intenta de nuevo.",
        "empty": "Introduce un nombre o ID.",
        "not_found": "Pokemon no encontrado.",
        "connection": "Error de conexion. Comprueba tu internet.",
        "api_error": "No se pudieron obtener los datos de PokeAPI.",
        "loading": "Buscando...",
        "goodbye": "Cerrando la Pokedex. Hasta pronto!",
        "language_title": "SELECCIONAR IDIOMA",
        "language_changed": "Idioma cambiado a Espanol.",
        "select_language": "Selecciona el idioma: ",
        "back": "Volver al menu principal",
        "number": "Numero nacional de Pokedex",
        "category": "Categoria",
        "types": "Tipo(s)",
        "height": "Altura",
        "weight": "Peso",
        "generation": "Generacion",
        "region": "Region de origen",
        "abilities": "HABILIDADES",
        "stats": "ESTADISTICAS BASE",
        "description": "DESCRIPCION DE LA POKEDEX",
        "regional": "NUMEROS DE POKEDEX REGIONALES",
        "unavailable": "No disponible",
        "no_description": "No hay descripcion disponible.",
        "no_data": "No hay datos disponibles.",
        "hidden": "Oculta",
        "project_info": "INFORMACION DEL PROYECTO",
        "version": "Version",
        "source": "Fuente de datos",
        "interface": "Interfaz",
        "metric_height": "m",
        "metric_weight": "kg"
    }
}

TYPE_NAMES = {
    "en": {
        "normal": "Normal", "fire": "Fire", "water": "Water",
        "electric": "Electric", "grass": "Grass", "ice": "Ice",
        "fighting": "Fighting", "poison": "Poison", "ground": "Ground",
        "flying": "Flying", "psychic": "Psychic", "bug": "Bug",
        "rock": "Rock", "ghost": "Ghost", "dragon": "Dragon",
        "dark": "Dark", "steel": "Steel", "fairy": "Fairy"
    },
    "es": {
        "normal": "Normal", "fire": "Fuego", "water": "Agua",
        "electric": "Electrico", "grass": "Planta", "ice": "Hielo",
        "fighting": "Lucha", "poison": "Veneno", "ground": "Tierra",
        "flying": "Volador", "psychic": "Psiquico", "bug": "Bicho",
        "rock": "Roca", "ghost": "Fantasma", "dragon": "Dragon",
        "dark": "Siniestro", "steel": "Acero", "fairy": "Hada"
    }
}

STAT_NAMES = {
    "en": {
        "hp": "HP", "attack": "Attack", "defense": "Defense",
        "special-attack": "Special Attack",
        "special-defense": "Special Defense", "speed": "Speed"
    },
    "es": {
        "hp": "PS", "attack": "Ataque", "defense": "Defensa",
        "special-attack": "Ataque especial",
        "special-defense": "Defensa especial", "speed": "Velocidad"
    }
}

REGIONS = {
    "generation-i": "Kanto",
    "generation-ii": "Johto",
    "generation-iii": "Hoenn",
    "generation-iv": "Sinnoh",
    "generation-v": "Unova / Teselia",
    "generation-vi": "Kalos",
    "generation-vii": "Alola",
    "generation-viii": "Galar",
    "generation-ix": "Paldea"
}


# ============================================================
# API ACCESS WITH IN-MEMORY CACHE
# ============================================================

def get_data(resource, language="en"):
    """Retrieve and cache a PokeAPI resource."""

    url = resource if resource.startswith("http") else (
        f"{API_URL}/{resource.strip('/')}/"
    )

    if url in cache:
        return cache[url]

    try:
        response = session.get(url, timeout=TIMEOUT)

        if response.status_code == 404:
            cache[url] = None
            return None

        response.raise_for_status()
        data = response.json()
        cache[url] = data
        return data

    except requests.exceptions.RequestException:
        print(f"\n{LANGUAGES[language]['connection']}")
    except ValueError:
        print(f"\n{LANGUAGES[language]['api_error']}")

    return None


# ============================================================
# POKEMON SEARCH AND DISPLAY
# ============================================================

def show_pokemon(identifier, language):
    """Search for a Pokemon and display its complete basic profile."""

    text = LANGUAGES[language]
    pokemon = get_data(f"pokemon/{identifier}", language)

    if pokemon is None:
        print(f"\n{text['not_found']}")
        return

    species = get_data(pokemon["species"]["url"], language)

    if species is None:
        print(f"\n{text['api_error']}")
        return

    # Select the description and category in the requested language.
    description = text["no_description"]
    category = text["unavailable"]

    for entry in species.get("flavor_text_entries", []):
        if entry["language"]["name"] == language:
            description = " ".join(
                entry["flavor_text"].replace("\f", " ").replace("\n", " ").split()
            )
            break

    for entry in species.get("genera", []):
        if entry["language"]["name"] == language:
            category = entry["genus"]
            break

    generation = species.get("generation", {}).get("name", "")
    region = REGIONS.get(generation, text["unavailable"])

    # Display the generation name.
    generation_number = generation.replace("generation-", "").upper()
    generation_label = (
        f"Generation {generation_number}"
        if language == "en"
        else f"Generacion {generation_number}"
    )

    types = [
        TYPE_NAMES[language].get(
            entry["type"]["name"], entry["type"]["name"].capitalize()
        )
        for entry in pokemon["types"]
    ]

    print("\n" + "=" * 58)
    print(f"                 {pokemon['name'].upper()}")
    print("=" * 58)
    print(f"{text['number']}: #{pokemon['id']:04d}")
    print(f"{text['category']}: {category}")
    print(f"{text['types']}: {' / '.join(types)}")
    print(f"{text['height']}: {pokemon['height'] / 10:.1f} {text['metric_height']}")
    print(f"{text['weight']}: {pokemon['weight'] / 10:.1f} {text['metric_weight']}")
    print(f"{text['generation']}: {generation_label}")
    print(f"{text['region']}: {region}")

    print(f"\n{text['abilities']}")
    print("-" * 58)

    for entry in pokemon["abilities"]:
        ability = get_data(entry["ability"]["url"], language)
        ability_name = entry["ability"]["name"].replace("-", " ").title()

        if ability:
            for name_entry in ability.get("names", []):
                if name_entry["language"]["name"] == language:
                    ability_name = name_entry["name"]
                    break

        if entry["is_hidden"]:
            ability_name += f" ({text['hidden']})"

        print(f"- {ability_name}")

    print(f"\n{text['stats']}")
    print("-" * 58)

    for entry in pokemon["stats"]:
        stat = entry["stat"]["name"]
        stat_name = STAT_NAMES[language].get(stat, stat.capitalize())
        print(f"{stat_name:<24}: {entry['base_stat']}")

    print(f"\n{text['description']}")
    print("-" * 58)
    print(description)

    print(f"\n{text['regional']}")
    print("-" * 58)

    regional_numbers = species.get("pokedex_numbers", [])

    if regional_numbers:
        for entry in regional_numbers:
            dex_name = entry["pokedex"]["name"].replace("-", " ").title()
            print(f"- {dex_name}: #{entry['entry_number']:03d}")
    else:
        print(text["no_data"])

    print("=" * 58)


# ============================================================
# MAIN MENU
# ============================================================

def main():
    """Run the interactive terminal application."""

    language = "en"

    while True:
        text = LANGUAGES[language]

        print("\n" + "=" * 45)
        print(f"       {text['menu']}")
        print("=" * 45)
        print(f"1. {text['search']}")
        print(f"2. {text['language']}")
        print(f"3. {text['info']}")
        print(f"4. {text['exit']}")

        option = input(f"\n{text['choice']}").strip()

        if option == "1":
            identifier = input(f"\n{text['query']}").strip().lower()

            if not identifier:
                print(f"\n{text['empty']}")
                continue

            if not identifier.isdigit():
                if not all(char.isalnum() or char == "-" for char in identifier):
                    print(f"\n{text['invalid']}")
                    continue
            elif int(identifier) < 1:
                print(f"\n{text['invalid']}")
                continue

            print(f"\n{text['loading']}")
            show_pokemon(identifier, language)

        elif option == "2":
            print(f"\n{text['language_title']}")
            print("1. English")
            print("2. Espanol")

            selection = input(text["select_language"]).strip()

            if selection == "1":
                language = "en"
            elif selection == "2":
                language = "es"
            else:
                print(f"\n{text['invalid']}")
                continue

            print(f"\n{LANGUAGES[language]['language_changed']}")

        elif option == "3":
            print("\n" + "=" * 45)
            print(text["project_info"])
            print("=" * 45)
            print(f"{text['version']}: 1.1")
            print(f"{text['source']}: PokeAPI")
            print(f"{text['interface']}: Terminal")
            print(f"{text['name']}: {text['name']}")

        elif option == "4":
            print(f"\n{text['goodbye']}")
            break

        else:
            print(f"\n{text['invalid']}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProgram interrupted by user.")
    finally:
        session.close()
