import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity
from ast import literal_eval

class MovieRecommendationModel:
    def __init__(self, df):
        self.df = df
        self.overview_tfidf_matrix = None
        self.overview_cosine_sim = None
        self.soup_cosine_sim = None
        self.indices = None
        self._clean_data()
        self._build_model()

    def _clean_data(self):
        features = ['director', 'cast', 'keywords', 'genres']
        for feature in features:
            if feature != 'director':
                self.df[feature] = self.df[feature].apply(literal_eval)
            self.df[feature] = self.df[feature].apply(self._clean_feature)

    def _clean_feature(self, x):
        if isinstance(x, list):
            return ' '.join([str.lower(i.replace(" ", "")) for i in x])
        else:
            return str.lower(x.replace(" ", "")) if isinstance(x, str) else ''

    def _build_model(self):
        # TF-IDF Vectorizer for overview
        tfidf = TfidfVectorizer(stop_words='english')
        self.overview_tfidf_matrix = tfidf.fit_transform(self.df['overview'].fillna(''))
        self.overview_cosine_sim = linear_kernel(self.overview_tfidf_matrix, self.overview_tfidf_matrix)

        # Count Vectorizer for soup
        self._process_soup()

        # Construct a reverse map of indices and movie titles
        self.indices = pd.Series(self.df.index, index=self.df['title']).drop_duplicates()

    def _process_soup(self):
        self.df['soup'] = self.df.apply(self._create_soup, axis=1)
        count = CountVectorizer(stop_words='english')
        count_matrix = count.fit_transform(self.df['soup'])
        self.soup_cosine_sim = cosine_similarity(count_matrix, count_matrix)

    def _create_soup(self, x):
        return ' '.join(x['keywords']) + ' ' + ' '.join(x['cast']) + ' ' + x['director'] + ' ' + ' '.join(x['genres'])

    def recommend(self, title, num_recommendations=10):
        idx = self.indices[title]
        sim_scores_overview = self.overview_cosine_sim[idx]
        sim_scores_soup = self.soup_cosine_sim[idx]
        
        # Normalize sim_scores
        max_overview = np.max(sim_scores_overview)
        max_soup = np.max(sim_scores_soup)
        sim_scores_overview /= max_overview
        sim_scores_soup /= max_soup
        
        # Combine and average the normalized similarity scores
        sim_scores = (2*sim_scores_overview + sim_scores_soup) / 3
        
        # Sort and select top recommendations
        sim_scores_indices = np.argsort(-sim_scores)[1:num_recommendations+1]
        
        return self.df['title'].iloc[sim_scores_indices]
