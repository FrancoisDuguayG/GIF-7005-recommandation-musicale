from pathlib import Path
import pandas as pd
import os
import fnmatch

# Programme pour extraire les données de Millon Song Dataset qui n'a pas été utilisé, car trop de données étaient
# manquante pour faire une analyse du contenu.
header = True

f = open("data/MillonSongDataset.csv","w+", encoding="utf-8")

for root,dirnames,filenames in os.walk(Path('data/MillionSongSubset')):
    for filename in fnmatch.filter(filenames, '*.h5'):
        #print(os.path.join(root, filename))
        hdf = pd.HDFStore(Path(root, filename),mode ='r')
        df1 = hdf.get('/analysis/songs/')
        df2 = hdf.get('/metadata/songs/')
        df3 = hdf.get('/musicbrainz/songs/')
        df = pd.concat([df1,df2,df3], axis = 1).reindex(df1.index)
        if header:
            df.to_csv(f, mode='a', header=True, lineterminator='\n')
            header = False
        else:
            df.to_csv(f,mode='a', header=False, lineterminator='\n')
        hdf.close()
f.close()
