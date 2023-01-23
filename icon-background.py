#!/usr/bin/env python3

"""
    Anthony Nelzin-Santos
    anthony@nelzin.fr
    https://anthony.nelzin.fr

    European Union Public License 1.2
"""

import argparse, biplist, os, sys
from collections import Counter
from PIL import Image, ImageDraw
from random import randrange
from sklearn.cluster import KMeans

# EXTRACTION DE L'ICÔNE
# L'icône ne possède pas un chemin fixe, mais un chemin défini
# par le développeur dans le plist. Parfois, le développeur oublie
# même de spécifier l'extension. Il faut donc reconstruire le chemin
# sans oublier d'ajouter l'extension.
def extract_icon(app_path):
    plist_path = os.path.join(app_path, "Contents", "Info.plist")
    plist = biplist.readPlist(plist_path)
    icon_ref = plist["CFBundleIconFile"]
    icon_name, icon_extension = os.path.splitext(icon_ref)
    if not icon_extension:
        icon_extension = ".icns"
    icon_path = icon_name + icon_extension
    
    return os.path.join(app_path, "Contents", "Resources", icon_path)

# ÉVALUATION DE LA COULEUR DOMINANTE DE L'ICÔNE
# Les icônes possède un masque de transparence, qu'il faut aplatir.
# Les zones noires issues de l'applatissement faussent les calculs.
# Mieux vaut donc extraire une section plus ou moins centrale de
# l'icône. Un nombre tiré au hasard permet de décaler la zone d’extraction d'un essai à l'autre, ce qui peut produire des résultats différents.
# (La ligne 54 peut être décommentée pour observer les variations.)
# On transforme ensuite l'image en liste de pixels, que l'on regroupe
# en clusters. On trouve le centre des clusters, puis on sélectionne
# le cluster dominant.
def get_color(icon_path, k, img_size, random):
    icon = Image.open(icon_path)
    icon = icon.convert("RGB")

    width, height = icon.size
    random = randrange(-random, random)
    left = (width - img_size)/2+random
    top = (height - img_size)/2+random
    right = (width + img_size)/2+random
    bottom = (height + img_size)/2+random
    crop = icon.crop((left, top, right, bottom))
    #crop.save("output.jpg")
    
    pixels = list(crop.getdata())
    cluster = KMeans(n_clusters = k)
    labels = cluster.fit_predict(pixels)
    count = Counter(labels)
    dominant = cluster.cluster_centers_[count.most_common(1)[0][0]]

    return list(dominant)

# CRÉATION DE L'ARRIÈRE-PLAN
# À partir de la couleur dominante, on crée un arrière-plan.
def create_bg(color, bg_width):
    red = int(color[0])
    green = int(color[1])
    blue = int(color[2])
    bg = Image.new("RGB", (bg_width, int(bg_width//1.6)), (red, green, blue))

    return bg

# ASSEMBLAGE FINAL
# Enfin, on réunit l'icône et l'arrière-plan. On repart de l'icône originale
# avec son masque de transparence. On la cale au milieu de l'arrière-plan, 
# et on colle les deux. Le résultat est écrit sur le disque.
def paste_icon(bg, icon_path, i):
    icon = Image.open(icon_path)
    
    position = ((bg.width - icon.width) // 2, (bg.height - icon.height) // 2)
    bg.paste(icon, position, icon)
    bg.save("output-" + str(i) + ".png")

def main():
    parser = argparse.ArgumentParser(description="Create a hero image from a macOS app or an app icon.")
    parser.add_argument("-a", "--app", help="Path to the macOS app.")
    parser.add_argument("-i", "--icon", help="Path to an icon (PNG or ICNS file with alpha layer).")
    parser.add_argument("-n", "--number", help="Number of iterations (default = 1).")
    args = parser.parse_args()

    # Convertit le namespace args en dict, puis vérifie les valeurs.
    # any() retourne Faux si aucune valeur n'est itérable, autrement
    # dit si aucun argument n'a été défini. On peut alors interrompre
    # l’exécution. Sinon, on poursuit en définissant le chemin de
    # l'icône, extraite d'une app ou piochée parmi les fichiers.
    if not any(vars(args).values()):
        sys.exit("\nYou must specify the path to an app (-a) or an icon (-i).\nCheck `icon-background.py -h` for more info.\n")
    elif args.app:
        icon_path = extract_icon(args.app)
    elif args.icon:
        icon_path = args.icon

    # L'icône passe alors par les différentes étapes d'assemblage.
    # La taille du fichier final (et la finesse du clustering) dépend
    # de la taille de l'icône, une approche naïve faute de mieux.
    if args.number:
        number = int(args.number)
    else:
        number = 1
    
    for i in range(number):
    	icon = Image.open(icon_path)
    	width = icon.width
    	
    	if width <= 256:
            color = get_color(icon_path, 2, 50, 50)
            bg = create_bg(color, 500)
    	elif 256 < width <= 512:
            color = get_color(icon_path, 3, 100, 100)
            bg = create_bg(color, 1000)
    	else:
            color = get_color(icon_path, 5, 250, 250)
            bg = create_bg(color, 2000)
    
    	paste_icon(bg, icon_path, i)

if __name__ == '__main__':
    main()