import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from numpy import save

# Importe les 50 000 premières lignes du fichier sinon cela cause une erreur de dépassement de mémoire
df = pd.read_csv('data/lyric_dataset.csv', nrows=50000)

# Retirer les mots vides
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(df['lyric_word'])

# Calculer la matrice de proximité cosine
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

# Sauvegarde la matrice
save('data/tfidf_matrix.npy', cosine_sim)
