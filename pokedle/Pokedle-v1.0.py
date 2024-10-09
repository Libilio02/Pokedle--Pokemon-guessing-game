import pypokedex
import requests
import random 
from pathlib import Path
import os
from PIL import Image

#Pokedex: es del 1 al 1025
current_directory = Path(__file__).parent  
    
def buscar(num:str):
    global respuesta_num
    global respuesta_nombre
    if num.isnumeric():
        try:
            respuesta_nombre = pypokedex.get(dex=int(num)).name
            respuesta_num = num
        except:
            print("Warning, the number introduced doesn`t match with any dex pokemon")
            exit()
    elif num.isalpha():
        try:
            respuesta_num = pypokedex.get(name=num).dex
            respuesta_nombre = num
        except:
            print("Warning, the name introduced doesn`t match with any dex pokemon")
            exit()
    else: 
        try:
            respuesta_num = pypokedex.get(name=num).dex
            respuesta_nombre = num
        except:
            print("Error, make sure that the information given does not contain spaces, or key combinations with numbers")
            exit()

def habilidad(respuesta_num):
    global lista
    lista = []
    ability = pypokedex.get(dex= int(respuesta_num)).abilities
    for i in range(len(ability)): 
        lista.append(ability[i].name)
    
def tipos(respuesta_num):
    global tipo
    tipo = pypokedex.get(dex= int(respuesta_num)).types
    if len(tipo) <=1:
        tipo.append("none")

def gen(i):
    global generacion
    if i <= 151:
        generacion = 1
    elif i <= 251:
        generacion = 2
    elif i <= 386:
        generacion = 3
    elif i <= 493:
        generacion = 4
    elif i <= 649:
        generacion = 5
    elif i <= 721:
        generacion = 6
    elif i <= 809:
        generacion = 7
    elif i <= 905:
        generacion = 8
    else:
        print("Unkown error")

def imagen_ascii(i):
    global image_path
    global pokemonDex
    
    current_directory = Path(__file__).parent  
    output_folder = Path(current_directory) / "output" 
    imgs_folder = output_folder / "imgs"
    imgs_folder.mkdir(parents=True, exist_ok=True) 
    log_file = output_folder / "log.txt"
    pokemonArg = i
    pokemonDex = pypokedex.get(name=pokemonArg)

    if pokemonDex.dex < 10:
        pokeoutput = '00' + str(pokemonDex.dex)
    elif pokemonDex.dex < 100:
        pokeoutput = '0' + str(pokemonDex.dex)
    else:
        pokeoutput = str(pokemonDex.dex)

    base_image_url = "http://www.serebii.net/swordshield/pokemon/"
    full_image_url = base_image_url + pokeoutput + ".png"
    response = requests.get(full_image_url)
    image_path = imgs_folder / f"{pokemonDex.name.lower()}.png" 
    with open(image_path, 'wb') as file:
        file.write(response.content)
    with open(log_file, 'a') as logfile:
        logfile.write(f"{pokemonDex.name.lower()}\n")
    
 
    img = Image.open(image_path)
    width, height = img.size
    aspect_ratio = height / width
    new_width = 120
    new_height = int(aspect_ratio * new_width * 0.55)
    img = img.resize((new_width, new_height))
    pixels = img.getdata()
    chars = ["█", "█", "█", "█", "█", "█", "█", "█", "█", "█", "█"]

    def rgb_to_ansi(r, g, b):
        return f"\033[38;2;{r};{g};{b}m"

    ascii_image = ""
    for i, pixel in enumerate(pixels):
        r, g, b = pixel[:3]  
        brightness = int((r + g + b) / 3)  # Calculamos la luminancia promedio
        char = chars[brightness // 100]
        ansi_color = rgb_to_ansi(r, g, b)
        ascii_image += f"{ansi_color}{char}"
        if (i + 1) % new_width == 0:
            ascii_image += "\033[0m\n"  

    print(ascii_image)

def etapa_evo(pokemon_name):
    global stage
    species_url = f"https://pokeapi.co/api/v2/pokemon-species/{pokemon_name.lower()}"
    species_response = requests.get(species_url)
    species_data = species_response.json()
    evolution_chain_url = species_data['evolution_chain']['url']
    evolution_chain_response = requests.get(evolution_chain_url)
    evolution_chain_data = evolution_chain_response.json()
    chain = evolution_chain_data['chain']
    def find_stage(chain, name, stage=1):
        if chain['species']['name'] == name:
            return stage
        for evolution in chain['evolves_to']:
            result = find_stage(evolution, name, stage + 1)
            if result:
                return result
        return None
    stage = find_stage(chain, pokemon_name.lower())
    return stage

#====================================================================================================

def info(num):
    buscar(num)
    habilidad(respuesta_num)
    tipos(respuesta_num)
    gen(int(respuesta_num))
    etapa_evo(respuesta_nombre)

def guess(random):
    global name_guess
    global gen_guess
    global ability_guess
    global tipos_guess
    global etapa_guess
    info(random)
    name_guess = respuesta_nombre
    gen_guess = generacion
    ability_guess = lista
    tipos_guess = tipo
    etapa_guess = stage

def comparador(name):
    #tipos:
    print(f"\033[1;36m"+"Types:"+"\033[0m", end = " ")
    for i in range(0,2):
        z = 0
        for j in range(0,2):
            if tipo[i] == tipos_guess[j]:
                if i == j:
                    print("\033[1;32m"+tipo[i]+"\033[0m", end = " ")
                    z += 1
                    break
                if i != j:
                    print("\033[1;33m"+tipo[i]+"\033[0m", end = " ")
                    z += 1
                    break
        if z == 0:
            print("\033[1;31m"+tipo[i]+"\033[0m", end = " ")
    #generacion
    if gen_guess == generacion:
        print(f"\033[1;36m"+" Gen: "+"\033[1;32m"+str(gen_guess)+"\033[0m", end = " ")
    elif gen_guess < generacion:
        print(f"\033[1;36m"+" Gen: "+"\033[1;33m"+str(generacion)+"⬇"+"\033[0m", end = " ")
    elif gen_guess > generacion:
        print(f"\033[1;36m"+" Gen: "+"\033[1;33m"+str(generacion)+"⬆"+"\033[0m", end = " ")
    #Etapa evolutiva
    if etapa_guess == stage:
        print(f"\033[1;36m"+" Stage: "+"\033[1;32m"+str(etapa_guess)+"\033[0m", end = "  ")
    elif etapa_guess < stage:
        print(f"\033[1;36m"+" Stage: "+"\033[1;33m"+str(stage)+"⬇"+"\033[0m", end = "  ")
    elif etapa_guess > stage:
        print(f"\033[1;36m"+" Stage: "+"\033[1;33m"+str(stage)+"⬆"+"\033[0m", end = "  ")
    #Habilidades
    print("\033[1;36m"+"Abilities: "+"\033[0m", end = " ")
    for i in range(len(lista)):
        z = 0
        for j in range(len(ability_guess)):
            if lista[i] == ability_guess[j]:
                if i == j:
                    print("\033[1;32m"+lista[i]+"\033[0m", end = " ")
                    z += 1
                    break
                if i != j:
                    print("\033[1;33m"+lista[i]+"\033[0m", end = " ")
                    z += 1
                    break
            else:
                None
        if z == 0:
            print("\033[1;31m"+lista[i]+"\033[0m", end = " ")
    #Pendiente de cambiar formato de texto

#==============================================================================================

#Preparacion de juego
guess(str(random.randint(0,904)))
respuesta_nombre = ""
info(str(input("Start by guessing a pokemon(from gen 1 to pokemon arceus, at the time just gen 9 missing): ")))
if respuesta_nombre == name_guess:
    imagen_ascii(name_guess)
    print("Wow that was lucky, you have guessed the pokemon!")
    exit()
while respuesta_nombre != name_guess:
    comparador(respuesta_nombre)
    info(str(input("Nice try! Keep trying: ")))
imagen_ascii(name_guess)
print("Congratulations, you have guessed the pokemon!")
