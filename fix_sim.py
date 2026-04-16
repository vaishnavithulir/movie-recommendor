import numpy as np
import pickle
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

print("Loading movie dict")
movies_dict = pickle.load(open('artifacts/movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

if 'tags' in movies.columns:
    print("Vectorizing")
    cv = CountVectorizer(max_features=5000, stop_words='english')
    vectors = cv.fit_transform(movies['tags'].fillna("")).toarray()
    print("Calculating similarity...")
    similarity = cosine_similarity(vectors)
else:
    print("Tags not found, using dummy similarity.")
    similarity = np.eye(len(movies))

print("Saving similarity.pkl")
pickle.dump(similarity, open('artifacts/similarity.pkl', 'wb'))
print("Done")
