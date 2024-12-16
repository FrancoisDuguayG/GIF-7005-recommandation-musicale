import pandas as pd
from numpy import load

# Charger le dataset des paroles et la matrice de similarité cosinus pré-calculée
df = pd.read_csv('data/lyric_dataset.csv', encoding='latin-1')
cosine_sim = load('data/tfidf_matrix.npy')

indices = pd.Series(df.index, index=df['track_id']).drop_duplicates()


def get_id(name):
    return df.query(f'title == "{name}"').get('track_id').values[0]


def get_name(id):
    return df.query(f'track_id == "{id}"').get('title').values[0]


def get_recommendations(id, cosine_sim=cosine_sim, num_recommend=10):
    """
    Renvoie une liste des chansons similaires à celle identifiée par `id`.

    :param id: Identifiant de la chanson pour laquelle obtenir des recommandations.
    :param cosine_sim: Matrice de similarité cosinus.
    :param num_recommend: Nombre de recommandations souhaitées.
    :return: DataFrame contenant les titres et artistes des chansons recommandées.
    """
    idx = indices[id]
    sim_scores = list(enumerate(cosine_sim[idx]))
    # Trier les chansons par similarité décroissante
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    # Sélectionner les indices des `num_recommend` chansons les plus similaires (en excluant elle-même)
    top_similar = sim_scores[1:num_recommend + 1]
    song_indices = [i[0] for i in top_similar]
    return df[['title', 'artist_name']].iloc[song_indices]

# Exemple d'utilisation : obtenir des recommandations pour une chanson donnée
track_id = "TREYHAY128F42B7D39"

# Obtenir 3 recommandations pour la chanson cible
recommendations = get_recommendations(track_id, num_recommend=3)

# Afficher les résultats
n = 1
print(f"Search: {get_name(track_id)}")
for index, song_info in recommendations.iterrows():
    print(f"{n}: {song_info.get('title')} ({song_info.get('artist_name')})")
    n += 1
