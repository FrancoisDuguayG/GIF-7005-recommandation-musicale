import csv
import os
import sqlite3
import zipfile
from pathlib import Path

import requests

data_folder = Path("data")
file = Path("data/mxm_dataset_train.txt")

# télécharge le fichier mxm_dataset_train.txt.zip
if not file.is_file():
    url = "http://millionsongdataset.com/sites/default/files/AdditionalFiles/mxm_dataset_train.txt.zip"
    os.makedirs(data_folder, exist_ok=True)
    print(f"Dowloading {url}")
    response = requests.get(url)
    zip_filename = url.split("/")[-1]
    zip_path = os.path.join(data_folder, zip_filename)

    with open(zip_path, "wb") as file:
        file.write(response.content)

    print("Extracting the zip file...")
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(data_folder)

file = Path("data/track_metadata.db")

# télécharge le fichier track_metadata.db
if not file.is_file():
    url = "http://millionsongdataset.com/sites/default/files/AdditionalFiles/track_metadata.db"
    print(f"Dowloading {url}")
    response = requests.get(url)
    filename = url.split("/")[-1]
    path = os.path.join(data_folder, filename)

    with open(path, "wb") as file:
        file.write(response.content)

# Lire le fichier contenant les données d'entraînement des paroles
with open('data/mxm_dataset_train.txt') as f:
    content = f.readlines()

# Extraction des 5000 mots de référence à partir des lignes commençant par '%'
for c in content:
    if c[0] == '#':  # Ignorer les lignes de commentaire commençant par '#'
        continue
    elif c[0] == '%':  # Ligne contenant les mots de référence
        words = c[1:].strip().split(',')
        break

track_lyrics = []

# Parcourir les lignes de contenu pour extraire les paroles de chaque chanson
for c in content:
    track = []
    if c[0] == '#' or c[0] == '%':  # Ignorer les lignes de commentaire ou de référence
        continue
    else:
        words_list = ""  # Stocker les paroles reconstruites pour une piste
        song = c.strip().split(',')
        track.append(song[0])
        track.append(song[1])
        for i in range(2, len(song)):  # Parcourir les mots encodés
            s = song[i].strip().split(':')
            t = ' '.join([words[int(s[0]) - 1]] * int(s[1]))
            words_list += ' ' + t
        track.append(words_list.strip())
    track_lyrics.append(track)  # Ajouter les informations de la piste à la liste principale

# Connexion à la base de données SQLite contenant les métadonnées des pistes
con = sqlite3.connect("data/track_metadata.db")
cur = con.cursor()

# Récupérer les titres et les noms d'artistes associés aux IDs de pistes
res = cur.execute("SELECT track_id, title, artist_name FROM songs")

id_name = {}  # Dictionnaire pour associer track_id à (titre, artiste)
for i in res:
    id_name[i[0]] = i[1:3]

# Ajouter le titre et l'artiste à chaque piste dans la liste track_lyrics
for i in track_lyrics:
    name_artist = id_name[i[0]]  # Récupérer les métadonnées via track_id
    i.append(name_artist[0])
    i.append(name_artist[1])

header = 1

# Écrire les données transformées dans un fichier CSV
with open("data/lyric_dataset.csv", "w+", newline='') as f:
    writer = csv.writer(f, quoting=csv.QUOTE_ALL)
    if header == 1:
        # Écrire l'en-tête au début du fichier
        writer.writerow(["track_id", "mxm_track_id", "lyric_word", "title", "artist_name"])
        header = 0
    writer.writerows(track_lyrics)  # Écrire toutes les lignes de données
