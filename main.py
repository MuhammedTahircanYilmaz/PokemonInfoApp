import requests
from tkinter import *
from tkinter import messagebox


def search_pokemon(pokemon):
    global results

    results.delete("1.0", END)
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon}"

    response = requests.get(url)
    response.raise_for_status()

    data = response.json()

    abilities = [ability['ability']['name'] for ability in data['abilities']]

    stats = {stat['stat']['name']: stat['base_stat'] for stat in data['stats']}

    types = [poke_type['type']['name'] for poke_type in data['types']]

    return {
        'Abilities': abilities,
        'Stats': stats,
        'Types': types
    }


def search_button_pressed():
    with open("Pokemonnames.txt", "r") as pokemonNames:
        name_list = pokemonNames.read().lower()

    if len(pokemon_name.get()) == 0:
        messagebox.showinfo(title="Warning!", message="Please enter the name of the Pokemon")
    if pokemon_name.get().lower() not in name_list:
        messagebox.showinfo(title="Warning!", message="Please enter a valid Pokemon name")
    else:
        pokemon = pokemon_name.get().lower()
        pokemon_info = search_pokemon(pokemon)
        results.delete(1.0, END)
        results.insert(END, f"Abilities: {', '.join(pokemon_info['Abilities'])}\n\n")
        results.insert(END, "Stats:\n")
        for stat, value in pokemon_info['Stats'].items():
            results.insert(END, f"{stat.capitalize()}: {value}\n")
        results.insert(END, f"\nTypes: {', '.join(pokemon_info['Types'])}")


if __name__ == '__main__':
    # Window
    window = Tk()
    window.title("Pokemon Search")
    window.minsize(300, 300)
    window.config(pady=10)
    # Pokemon Name
    label1 = Label(text="Please enter Pokemon name", pady=5)
    label1.pack()

    pokemon_name = Entry()
    pokemon_name.pack()

    # Search button
    button = Button(text="Search", pady=5, command=search_button_pressed)
    button.pack()

    # Results
    results = Text(height=12, width=30)
    results.pack()

    window.mainloop()
