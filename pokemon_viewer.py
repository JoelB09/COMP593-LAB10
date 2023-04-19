import poke_api
from tkinter import *
from tkinter import ttk 
import os
import ctypes

# Get the path of the script and its parent directory
script_path = os.path.abspath(__file__)
script_dir = os.path.dirname(script_path)
image_cache_dir = os.path.join(script_dir, 'images')

#Make image cache folder if it dont exist
if not os.path.isdir(image_cache_dir):
    os.makedirs(image_cache_dir)

# Create the main window
root = Tk()
root.title("Pokemon image viewer")
root.minsize(600, 500)


# Set the window icon
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('COMP593.PokeImageViewer') 
icon_path = os.path.join(script_dir, 'Poke-Ball.ico')
root.iconbitmap(icon_path)
root.columnconfigure(0, weight=1) 
root.rowconfigure(0, weight=1)

#Create Frame
frame = ttk.Frame(root)
frame.grid(row=0, column=0, padx=10, pady=10, sticky=NSEW)
frame.columnconfigure(0, weight=1)
frame.rowconfigure(0, weight=1)

#Add the image 
img_poke = PhotoImage(file=os.path.join(script_dir, 'Pokemon_Logo.png'))
lbl_poke_image = ttk.Label(frame, image=img_poke)
lbl_poke_image.grid(row=0, column=0)

#Add pokemon name pull down-list 
pokemon_name_list = sorted(poke_api.get_pokemon_names())
cbox_poke_names = ttk.Combobox(frame, values=pokemon_name_list, state='readonly')
cbox_poke_names.set("Select a Pokemon")
cbox_poke_names.grid(row=1, column=0, padx=10, pady=10) 

def handle_pokemon_sel(event):
   # Get name of selected pokemon
   pokemon_name = cbox_poke_names.get()

   # Download and save artwork of selected pokemon 
   global image_path
   image_path =  poke_api.download_pokemon_artwork(pokemon_name, image_cache_dir)

   # Display pokemon artwork 
   if image_path is not None: 
      img_poke['file'] = image_path
   
cbox_poke_names.bind('<<ComboboxSelected>>', handle_pokemon_sel)

def set_desktop_image():

    # Accessing global image and checking wether the image path is the right one
    global image_path
    if image_path is not None: 
        return True 
        
        # Getting selected Pokemon from the list 
        pokemon_name = cbox_poke_names.get()

        # Sets desktop background to the image selected
        SPI_SETDESKWALLPAPER = 20
        ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, image_path, 0)

# labeling and padding clickable button
btn_set_desktop = ttk.Button(frame, text='Set as Desktop Image', command=set_desktop_image) 
btn_set_desktop.grid(row=2, column=0, padx=10, pady=10)




root.mainloop()
