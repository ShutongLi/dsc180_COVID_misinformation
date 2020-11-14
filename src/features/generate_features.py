import os
import pandas as pd
import numpy as np

# Count the number of occurences of every hashtag in the JSON
def hashtag_counts(json):
    df = pd.read_json(json, lines = True)
    ht = df['entities'].apply(lambda e: [x['text'] for x in e['hashtags']])
    return pd.Series(ht.sum()).value_counts()


# Count the number of posts every user has made in the JSON
def user_counts(json):
    df = pd.read_json(json, lines=True)
    us = df['user'].apply(lambda x: x['screen_name'])
    return us.value_counts()


# Count either hashtags or users in all available JSON files
def count_features(jsons, top_k, mode = 'hashtag'):
    # Decide whether to count hashtags or users
    if mode == 'hashtag':
        method = hashtag_counts
    elif mode == 'user':
        method = user_counts
        
    # Compile count of first JSON in list
    total_series = method(jsons[0])
    print(f'vc shape {total_series.shape}', end='\r')
    
    # Append counts to every subsequent JSON
    for json in jsons[1:]:
        vc_series = method(json)
        total_series = total_series.add(vc_series, fill_value = 0)
        print(f'vc shape {total_series.shape}', end='\r')
        
    # Return the top K users/hashtags in all of the data
    if top_k is None:
        return total_series.sort_values().sort_values(ascending=False)
    return total_series.sort_values(ascending=False).iloc[:top_k]


# Get the number of certain used hashtags over time
def count_over_time(jsons, good_tags, bad_tags):
    good = []
    bad = []
    for json in jsons:
        vc = hashtag_counts(json)
        good.append(vc.reindex(good_tags).fillna(0))
        bad.append(vc.reindex(bad_tags).fillna(0))
    return good, bad
