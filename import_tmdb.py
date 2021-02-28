#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 28 13:58:23 2021

@author: lisatostrams
"""


import tmdbsimple as tmdb
tmdb.API_KEY = 'df4ecf274dc5b5517bf279fa8489a30b'

#%%


import json
import http.client
import requests
import csv

import requests

import pandas as pd
import time

tmdb_api = requests.Session()
tmdb_api.params={'api_key':tmdb.API_KEY}



def get_popular_movies_info(max_movies=10000):
    url = 'https://api.themoviedb.org/3/movie/top_rated'
    
    pages = max_movies // 20
    df = pd.DataFrame(columns=['adult', 'backdrop_path', 'genre_ids', 'id', 'original_language', 'original_title', 'overview', 'popularity', 'poster_path', 'release_date', 'title', 'video', 'vote_average', 'vote_count'])
    df.to_csv('data/pop_movies.csv',index=False)    
    st = time.time()
    total_time=0
    for page in range(1,pages+1):
        http_resp = tmdb_api.get(url,params={'page':page})
        json_resp = json.loads(http_resp.text)
        movies = json_resp['results']
        movies_df = pd.DataFrame(movies)
        movies_df.to_csv('data/pop_movies.csv', mode='a', header=False,index=False)
        total_time = (time.time()-st)
        remaining = (pages+1-page)*(total_time/page)
        print('page {} of {}, est time remaining: {:.0f}m{:.2f}s'.format(page,pages,remaining//60,remaining%60))
        


def get_known_for_info(known_for_row):
    return_val = []
    for record in known_for_row:
        if 'title' not in record.keys() and 'name' in record.keys():
            title = record['name']
        elif 'title' in record.keys():
            title = record['title']
        else:
            title = ''
        if 'id' in record.keys():
            _id = record['id']
        else:
            _id = ''
        return_val.append((_id,title))
    return return_val
        
    
    

def get_popular_credits_info(max_people=10000):
    
    url = 'https://api.themoviedb.org/3/person/popular'
    
    pages = max_people // 20
    df = pd.DataFrame(columns=['adult', 'backdrop_path', 'genre_ids', 'id', 'original_language', 'original_title', 'overview', 'popularity', 'poster_path', 'release_date', 'title', 'video', 'vote_average', 'vote_count'])
    df.to_csv('data/pop_credits.csv',index=False)    
    st = time.time()
    total_time=0
    for page in range(1,pages+1):
        http_resp = tmdb_api.get(url,params={'page':page})
        json_resp = json.loads(http_resp.text)
        people = json_resp['results']
        people_df = pd.DataFrame(people)
        people_df.known_for = people_df.known_for.apply(get_known_for_info)
        people_df.to_csv('data/pop_credits.csv', mode='a', header=False,index=False)
        total_time = (time.time()-st)
        remaining = (pages+1-page)*(total_time/page)
        print('page {} of {}, est time remaining: {:.0f}m{:.2f}s'.format(page,pages,remaining//60,remaining%60))
        
  