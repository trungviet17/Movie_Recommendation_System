from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import numpy as np
import pandas as pd
from flask import Flask, render_template, request
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json
import bs4 as bs
import urllib.request
import pickle
import requests
import lxml

# load the nlp model and tfidf vectorizer from disk
filename = '/workspaces/Movie_Recommendation_System/movie_recommend/main/model/nlp_model.pkl'
clf = pickle.load(open(filename, 'rb'))
vectorizer = pickle.load(open('/workspaces/Movie_Recommendation_System/movie_recommend/main/model/tranform.pkl','rb'))


def create_similarity():
    data = pd.read_csv('/workspaces/Movie_Recommendation_System/main_data.csv')
    # creating a count matrix
    cv = CountVectorizer()
    count_matrix = cv.fit_transform(data['comb'])
    # creating a similarity score matrix
    similarity = cosine_similarity(count_matrix)
    return data,similarity

def rcmd(m):
    m = m.lower()
    try:
        data.head()
        similarity.shape
    except:
        data, similarity = create_similarity()
    if m not in data['movie_title'].unique():
        return('Sorry! The movie you requested is not in our database. Please check the spelling or try with some other movies')
    else:
        i = data.loc[data['movie_title']==m].index[0]
        lst = list(enumerate(similarity[i]))
        lst = sorted(lst, key = lambda x:x[1] ,reverse=True)
        lst = lst[1:11] # excluding first item since it is the requested movie itself
        l = []
        for i in range(len(lst)):
            a = lst[i][0]
            l.append(data['movie_title'][a])
        return l
    
# converting list of string to list (eg. "["abc","def"]" to ["abc","def"])
def convert_to_list(my_list):
    my_list = my_list.split('","')
    my_list[0] = my_list[0].replace('["','')
    my_list[-1] = my_list[-1].replace('"]','')
    return my_list

def get_suggestions():
    data = pd.read_csv('/workspaces/Movie_Recommendation_System/main_data.csv')
    return list(data['movie_title'].str.capitalize())

def home(request):
    suggestions = get_suggestions()
    return render(request, 'main/home.html',{'suggestions': suggestions})

@csrf_exempt
def similarity(request):
    if request.method == 'POST':
        movie = request.POST['name']
        if movie:
            rc = rcmd(movie)
            if isinstance(rc, str):  # Sửa đổi kiểm tra kiểu dữ liệu
                return JsonResponse({'result': rc})  # Sửa đổi trả về JSON response
            else:
                m_str = "---".join(rc)
                return JsonResponse({'result': m_str})  # Sửa đổi trả về JSON response
        else:
            return JsonResponse({'error': 'No movie name provided'}, status=400)  # Trả về lỗi nếu không có tên phim
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)  # Trả về lỗi nếu phương thức yêu cầu không hợp lệ


@csrf_exempt
def recommend(request):
    if request.method == 'POST':
        # getting data from AJAX request
        title = request.POST.get('title', '')
        cast_ids = request.POST.get('cast_ids', '')
        cast_names = request.POST.get('cast_names', '')
        cast_chars = request.POST.get('cast_chars', '')
        cast_bdays = request.POST.get('cast_bdays', '')
        cast_bios = request.POST.get('cast_bios', '')
        cast_places = request.POST.get('cast_places', '')
        cast_profiles = request.POST.get('cast_profiles', '')
        imdb_id = request.POST.get('imdb_id', '')
        poster = request.POST.get('poster', '')
        genres = request.POST.get('genres', '')
        overview = request.POST.get('overview', '')
        vote_average = request.POST.get('rating', '')
        vote_count = request.POST.get('vote_count', '')
        release_date = request.POST.get('release_date', '')
        runtime = request.POST.get('runtime', '')
        status = request.POST.get('status', '')
        rec_movies = request.POST.get('rec_movies', '')
        rec_posters = request.POST.get('rec_posters', '')

        # get movie suggestions for auto complete
        suggestions = get_suggestions()

        # call the convert_to_list function for every string that needs to be converted to list
        rec_movies = convert_to_list(rec_movies)
        rec_posters = convert_to_list(rec_posters)
        cast_names = convert_to_list(cast_names)
        cast_chars = convert_to_list(cast_chars)
        cast_profiles = convert_to_list(cast_profiles)
        cast_bdays = convert_to_list(cast_bdays)
        cast_bios = convert_to_list(cast_bios)
        cast_places = convert_to_list(cast_places)
        
        # convert string to list (eg. "[1,2,3]" to [1,2,3])
        cast_ids = cast_ids.split(',')
        cast_ids[0] = cast_ids[0].replace("[","")
        cast_ids[-1] = cast_ids[-1].replace("]","")
        
        # rendering the string to python string
        for i in range(len(cast_bios)):
            cast_bios[i] = cast_bios[i].replace(r'\n', '\n').replace(r'\"','\"')
        
        # combining multiple lists as a dictionary which can be passed to the html file so that it can be processed easily and the order of information will be preserved
        movie_cards = {rec_posters[i]: rec_movies[i] for i in range(len(rec_posters))}
        
        casts = {cast_names[i]:[cast_ids[i], cast_chars[i], cast_profiles[i]] for i in range(len(cast_profiles))}

        cast_details = {cast_names[i]:[cast_ids[i], cast_profiles[i], cast_bdays[i], cast_places[i], cast_bios[i]] for i in range(len(cast_places))}

        # # web scraping to get user reviews from IMDB site
        # sauce = urllib.request.urlopen('https://www.imdb.com/title/{}/reviews?ref_=tt_ov_rt'.format(imdb_id)).read()
        # soup = bs(sauce, 'lxml')
        # soup_result = soup.find_all("div",{"class":"text show-more__control"})

        # reviews_list = [] # list of reviews
        # reviews_status = [] # list of comments (good or bad)
        # for reviews in soup_result:
        #     if reviews.string:
        #         reviews_list.append(reviews.string)
        #         # passing the review to our model
        #         movie_review_list = np.array([reviews.string])
        #         movie_vector = vectorizer.transform(movie_review_list)
        #         pred = clf.predict(movie_vector)
        #         reviews_status.append('Good' if pred else 'Bad')

        # # combining reviews and comments into a dictionary
        # movie_reviews = {reviews_list[i]: reviews_status[i] for i in range(len(reviews_list))}     
        movie_reviews ={}
        # passing all the data to the html file
        return render(request, 'main/recommend.html',{'title': title, 'poster': poster, 'overview': overview, 'vote_average': vote_average,
            'vote_count': vote_count, 'release_date': release_date, 'runtime': runtime, 'status': status, 'genres': genres,
            'movie_cards': movie_cards, 'reviews': movie_reviews, 'casts': casts, 'cast_details': cast_details})