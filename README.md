# GIF-7005-recommandation-musicale
Projet Final du cours GIF-7005

[Proposition de projet google docs](https://docs.google.com/document/d/1YtSfVb9_rw-EmNcj6wlsOitzHu8TCMFM6mdDwm6SvnU/edit?usp=sharing)

[Million song data set website](http://millionsongdataset.com/)

### Données

Big file store with [git LFS](https://git-lfs.com/)

[Million song subset](http://millionsongdataset.com/pages/getting-dataset/#subset)

[Million user dataset](http://millionsongdataset.com/tasteprofile/#:~:text=Getting%20the-,dataset,-First%2C%20if%20you)



### Utilisation

Vous devez avoir le [mxm_dataset_train.txt](data/mxm_dataset_train.txt) et [track_metadata.db](data/track_metadata.db) de téléchargés.

Pour obtenir une recommandation vous devez exécuter dans l'ordre les fichiers suivant:

1. [lyric_extraction_csv.py](lyric_extraction_csv.py)
2. [lyrics_analyze_compute_tfidf_matrix.py](lyrics_analyze_compute_tfidf_matrix.py)
3. [lyrics_analyzer_find_recommendation.py](lyrics_analyzer_find_recommendation.py)

[lyrics_analyzer_find_recommendation.py](lyrics_analyzer_find_recommendation.py) peut être réutilisé en changeant l'id 
de la chanson pour obtenir d'autres recommandations.