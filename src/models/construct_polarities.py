import os
import pandas as pd
import numpy as np
import tweepy
import json
import datetime

# API get
def get_tweepy_api(api_keys):
    # Get keys
    with open(api_keys) as f:
        keys = json.load(f)
    consumer_key = keys['consumer_key']
    consumer_secret = keys['consumer_secret']
    access_token = keys['access_token']
    access_token_secret = keys['access_token_secret']
    
    # Set keys
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    return tweepy.API(auth, wait_on_rate_limit=True)

# Count the number of occurences of every hashtag in the JSON
def hashtag_counts(json, marker_ht = None):
    df = pd.read_json(json, lines = True)
    ht = df['entities'].apply(lambda e: [x['text'] for x in e['hashtags']])
    ht_vc = pd.Series(ht.sum()).value_counts()
    if marker_ht is not None:
        num_tweets = len(df)
        subset_ht = ht.apply(lambda x: x if set(x) & set(marker_ht) else None).dropna()
        marker_num_tweets = len(subset_ht)
        marker_vc = pd.Series(subset_ht.sum()).value_counts()
        return ht_vc, marker_vc, num_tweets, marker_num_tweets
    return ht_vc


# Count the number of posts every user has made in the JSON
def user_counts(json):
    df = pd.read_json(json, lines=True)
    us = df['user'].apply(lambda x: x['screen_name'])
    return us.value_counts()


# Count either hashtags or users in all available JSON files
def count_features(jsons, top_k = None, mode = 'hashtag', marker_ht = None):
    # Decide whether to count hashtags or users
    if mode == 'hashtag':
        method = hashtag_counts
    elif mode == 'user':
        method = user_counts
    
    ### POLARITY: having marker_ht indicates that we are calculating polarity
    if marker_ht is not None:
        print('polarity mode')
        total_series, marker_series, num_tweets, marker_num_tweets = method(jsons[0], marker_ht = marker_ht)
        print(f'vc shape {total_series.shape}', end='\r')
    
        # Append counts to every subsequent JSON, top_k has to be defined
        for json in jsons[1:]:
            vc, marker_vc, new_num_tweets, new_marker_num_tweets = method(json, marker_ht = marker_ht)
            total_series = total_series.add(vc, fill_value = 0)
            marker_series = marker_series.add(marker_vc, fill_value = 0)
            num_tweets += new_num_tweets
            marker_num_tweets += new_marker_num_tweets
            print(f'vc shape {total_series.shape}', end='\r')   
        # make sure top-k is defined
        topk_vc = total_series.sort_values(ascending = False).iloc[:top_k]
        # note that marker_series is the entire series, rather than top-K
        return topk_vc, marker_series, num_tweets, marker_num_tweets
    
    ### Visualization: we are only interested in number of hashtags
    # Compile count of first JSON in list
    total_series = method(jsons[0])
    print(f'vc shape {total_series.shape}', end='\r')
    
    # Append counts to every subsequent JSON
    for json in jsons[1:]:
        vc_series = method(json)
        total_series = total_series.add(vc_series, fill_value = 0)
        print(f'vc shape {total_series.shape}', end='\r')
        
    # Return the top users/hashtags in all of the data
    result = total_series.sort_values(ascending = False)
    
    if top_k is not None:
        return result.iloc[:top_k]
    return result


# Get the number of certain used hashtags over time
def count_over_time(jsons, good_tags, bad_tags):
    good = []
    bad = []
    for json in jsons:
        vc = hashtag_counts(json)
        good.append(vc.reindex(good_tags).fillna(0))
        bad.append(vc.reindex(bad_tags).fillna(0))
    return good, bad

### BELOW IS FOR CALCULATING HASHTAG POLARITY

# wrapper for count_features to calculate baseline rate of occurence of top 200 hashtags
def hashtag_polarity(jsons, top_k, marker_ht):
    top200_vc, marker_vc, total_num_tweets, marker_num_tweets =  count_features(jsons, top_k, marker_ht = marker_ht)
    print(f'there are {total_num_tweets} tweets and {marker_num_tweets} subset tweets')
    baseline_ROF = top200_vc / total_num_tweets
    # marker_vc contains all hashtags in the marker 
    # marker_ROF is the ROF of 200 under the subsetted marker value_counts
    marker_ROF = marker_vc.reindex(top200_vc.index, fill_value=0) / marker_num_tweets
    return (marker_ROF - baseline_ROF) / baseline_ROF


### BELOW IS FOR CALCULATING HASHTAG POLARITY
# find all user names
def collect_all_users(jsons):
    all_users = set()
    for json in jsons:
        df = pd.read_json(json, lines=True)
        us = set(df['user'].apply(lambda x: x['screen_name']))
        all_users = all_users.union(us)
        print(f'{len(all_users)} users in total', end='\r')
    return pd.Series(list(all_users))

# find the all the tweets of a user between dates
def search_tweets(api, username, t200_ht, lower, upper, date_pattern, max_posts = None, max_iter = None):
    assert type(t200_ht) == set, "make sure pass in a SET of hashtags"
    upper = pd.to_datetime(upper)
    lower = pd.to_datetime(lower)
    # all the hashtags ever used by a user
    hashtags = []
    i = 0
    tweet_stored = 0
    # number of tweets that contains t200 hashtags
    num_norm_tweets = 0
    for status in tweepy.Cursor(api.user_timeline, screen_name=username).items():
        if ((max_posts is not None) and (tweet_stored > max_posts)) \
        or ((max_iter is not None) and (i > max_iter)):
            break
        # process status here
        ajson = status._json
        created_at = ajson['created_at']
        print(i, f'{tweet_stored} tweets qualified', created_at, end = '\r')
        creation_date = datetime.datetime.strptime(created_at, date_pattern).replace(tzinfo = None)
        if lower < creation_date < upper:
            hashtags_of_tweet = [x['text'] for x in ajson['entities']['hashtags']]
            if set(hashtags_of_tweet) &  t200_ht:
                num_norm_tweets += 1
            hashtags.extend(hashtags_of_tweet)
            tweet_stored += 1
        i += 1
    # return value count of hashtags
    return pd.value_counts(pd.Series(hashtags)), num_norm_tweets

# return normalized user polarity
def user_polarity(api, username, t200_ht, lower, upper, 
                  date_pattern, 
                  ht_polarity, 
                  max_posts = None, max_iter = None,
                  normalize = True):
    print(f'investigating {username}')
    user_ht_counts, num_norm_tweets = search_tweets(api, username, t200_ht, 
                                                    lower, upper, date_pattern, 
                                                    max_posts = max_posts, max_iter = max_iter)
    toi = user_ht_counts.reindex(ht_polarity.index, fill_value=0)
    # sum of each t200 hashtag's occurence times the polarity of the hashtag 
    u_pol = (toi * ht_polarity).sum()
    if normalize:
        print(u_pol, num_norm_tweets)
        u_pol /= num_norm_tweets
    return u_pol

### Investigate retweets of a tweet
def investigate_retweets(tid, num_retrieve_con, t200_ht, lower, upper, 
                         date_pattern, 
                         ht_polarity, json_path, 
                         max_posts = None, max_iter = None,
                         api = None,
                         normalize = True):
    
    if api is None:
        return {'user1': 2, 'user2': 1}
    else:
        retweets = api.retweets(tid, num_retrieve_con)
        names = [r.user.screen_name for r in retweets]
    try:
        fh = open(json_path, "r")
        user_polarity_dict = json.load(fh)
        fh.close()
    except:
        user_polarity_dict = {}
    fh = open(json_path,'w')
    for name in names:
        fh.seek(0)
        if name not in user_polarity_dict.keys():
            score = user_polarity(api, name,
                                  set(ht_polarity.index), 
                                  lower, upper, date_pattern,
                                  ht_polarity, 
                                  max_posts = max_posts, 
                                  max_iter=max_iter,
                                 )
            user_polarity_dict[name] = score
            print(f'{name}: {score}', end = '\r')
        json.dump(user_polarity_dict, fh)
    fh.close()
    return user_polarity_dict