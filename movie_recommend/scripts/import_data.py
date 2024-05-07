import pandas as pd 
from main.models import Movie, Cast
import os


def run() : 

    movie_df = pd.read_csv('../Data/Main_data/American1970.csv')


    for i in range(1971, 1990) :
        tmp =  pd.read_csv('../Data/Main_data/American' + str(i) + '.csv')
        
        movie_df = pd.concat([movie_df, pd.read_csv('../Data/Main_data/American' + str(i) + '.csv')])

    

    # for i in range(2010, 2024):
    #     # if not os.path.exists('../Data/Main_data/Japanese_actor_id' + str(i)  + 'done.csv') : continue
    #     # actor_df = pd.concat([actor_df, pd.read_csv('../Data/Main_data/Japanese_actor_id' + str(i)  + 'done.csv')])
    #     if not os.path.exists('../Data/Main_data/South_Korean_actor_id' + str(i)  + 'done.csv') : continue
    #     actor_df = pd.concat([actor_df, pd.read_csv('../Data/Main_data/South_Korean_actor_id' + str(i) + 'done.csv')])
        


    movie_df=  movie_df.drop(['Unnamed: 0'], axis = 1)
    movie_df = movie_df.drop_duplicates('TMDB_id')
    movie_df = movie_df.dropna()
    
    
    print(Cast.objects.get(id = 227611).name)
    # objs = []
    for index, row in movie_df.iterrows():
        # Kiểm tra xem đối tượng Cast với ID tương tự đã tồn tại chưa
        if not Movie.objects.filter(id=row['TMDB_id']).exists():
            # Nếu không tồn tại, tạo và thêm vào danh sách
            tmp = Movie(title = row['Title'], genre = row['genre'], released = row['released'], 
                        overview = row['overview'], popularity = row['popularity'], image = row['image'], id = row['TMDB_id'])
            
            list_casts = eval(row['casts'])
            tmp.save()
            for i in list_casts : 
                if not Cast.objects.filter(id = i).exists() : continue
                tmp.casts.add(Cast.objects.get(id = i))

            # objs.append(tmp)

    # Lưu tất cả các đối tượng vào trong database

    # Movie.objects.bulk_create(objs)
    
    
    print("CSV data has been loaded into the Django database.")


    