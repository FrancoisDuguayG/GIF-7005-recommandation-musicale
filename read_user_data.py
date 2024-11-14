from pathlib import Path
import pandas as pd
from scipy.sparse import save_npz, load_npz, coo_array


# Charger les données
file_path = Path('./data/train_triplets_small.txt')
data = pd.read_csv(file_path, sep='\t', header=None, names=['user_id', 'song_id', 'play_count'])

# mapper les IDs à des index uniques
user_ids = data['user_id'].astype('category').cat.codes
song_ids = data['song_id'].astype('category').cat.codes

# Créer la matrice
sparse_matrix = coo_array((data['play_count'], (user_ids, song_ids)))

# Sauvegarder la matrice
save_npz(Path('./data/user_song_matrix.npz'), sparse_matrix)

matrix = load_npz(Path('./data/user_song_matrix.npz'))

