import requests
import image_lib
import os 

POKE_API_URL = 'https://pokeapi.co/api/v2/pokemon/'

def main():
    #poke_info = get_pokemon_info("Rockruff")
    #poke_info = get_pokemon_info(123)
    #names = get_pokemon_names()
    download_pokemon_artwork('dugtrio', r'C:\temp')

    return

def get_pokemon_info(pokemon_name):
    
    pokemon_name = str(pokemon_name).strip().lower()

    url = POKE_API_URL + pokemon_name

    print(f'Getting information for {pokemon_name}...', end='')
    resp_msg =  requests.get(url)

    if resp_msg.status_code == requests.codes.ok:
        print('success')
        return resp_msg.json()
    else:
        print('failure')
        print(f'Response code: {resp_msg.status_code} ({resp_msg.reason})')  
        return  

def get_pokemon_names(offset=0, limit=100000):

    query_str_params = {
        'offset' :offset,
        'limit' :limit
    }

    print(f'Getting list of pokemon names...', end='')
    resp_msg = requests.get(POKE_API_URL, params=query_str_params)

    if resp_msg.status_code == requests.codes.ok:
        print("success")
        pokemon_dict = resp_msg.json()
        pokemon_names_list = [p['name'] for p in pokemon_dict['results']]
        return pokemon_names_list

    else:
        print('failure')
        print(f'Response code: {resp_msg.status_code} ({resp_msg.reason})')  
        return
        

def download_pokemon_artwork(pokemon_name, save_dir):

    pokemon_info = get_pokemon_info(pokemon_name)
    if pokemon_info is None:
        return 
    
    artwork_url = pokemon_info['sprites']['other']['official-artwork']['front_default']

    
    image_bytes = image_lib.download_image(artwork_url)
    if image_bytes is None:
        return 

    file_ext = artwork_url.split('.')[-1]
    image_path = os.path.join(save_dir, f'{pokemon_name}.{file_ext}')
    if image_lib.save_image_file(image_bytes, image_path):
        return image_path

     

if __name__=='__main__':
    main()






    