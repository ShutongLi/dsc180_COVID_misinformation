import os
import pandas as pd
import requests
import gzip
import shutil
import json
from twarc import Twarc
from datetime import datetime, date, timedelta

# Get the last_day_added based on the latest date in your dataset
def get_last_day(raw_data_path, from_time):
    
    # Earliest possible date
    last_day_added = datetime.strptime(from_time, '%Y-%m-%d').date()
    
    # Get all filenames of our raw data
    for name in os.listdir(raw_data_path):
        try:
            # Get the date from the name
            name_date = datetime.strptime(name[:10], '%Y-%m-%d').date()
            # Get maximum date
            if last_day_added < name_date:
                last_day_added = name_date
                
        # Non-data file found
        except:
            print(f'{name} does not have a date.')
    return last_day_added

# Updates your dataset FROM from_time date (YYYY-MM-DD) TO to_time date
def download_latest_datasets(raw_data_path, from_time, to_time, cleaned = False, test = False):
    # Get days of data between range
    last_day = get_last_day(raw_data_path, from_time)
    days_between = pd.date_range(last_day, to_time, freq='d')
    
    # suffix _cleaned needed
    clean_suffix = ''
    if cleaned:
        clean_suffix = '_clean'
        
    # suffix _test for test cases
    test_suffix = ''
    if test:
        test_suffix = '_test'
    
    # Download the data from each day
    for day in days_between:
        
        # Download gzipped file
        day_str = datetime.strftime(day, '%Y-%m-%d')
        url = f'https://github.com/thepanacealab/covid19_twitter/blob/master/dailies/{day_str}/{day_str}{clean_suffix}-dataset.tsv.gz?raw=true'
        print(f'requesting from {url}')
        
        try:
            # Make directories if they don't already exist
            os.mkdir(f'{raw_data_path}/gzips')
        except:
            pass
        
        # Separate gzipped and TSV files
        try:
            filename = f'{raw_data_path}/gzips/{day_str}{clean_suffix}{test_suffix}-dataset.tsv.gz'
            filename2 = f'{raw_data_path}/{day_str}{clean_suffix}{test_suffix}-dataset.tsv'
            with open(filename, 'wb') as f:
                r = requests.get(url)
                f.write(r.content)

            # Download TSV
            with gzip.open(filename, 'rb') as f_in:
                with open(filename2, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
        except:
            print(f'There is no data for {day_str}')
            os.remove(filename)
            os.remove(filename2)


# Set up Twarc with API Keys
def configure_twarc(api_keys_json):
    with open(api_keys_json) as f:
        keys = json.load(f)
        t = Twarc(
            keys['consumer_key'],
            keys['consumer_secret'],
            keys['access_token'],
            keys['access_token_secret']
        )
    return t


# For a day's worth of tweets, sample one out of every number of tweets
def sample_file(file_path, sample_rate, id_column):
    df = pd.read_csv(file_path, sep='\t')
    return df.iloc[::sample_rate, :][id_column]


# Get the information from raw tweets we just obtained
def rehydrate_tweets(raw_data_path, json_data_path, sample_rate, id_column, api_keys_json, test=False):
    # Start and configure Twarc
    t = configure_twarc(api_keys_json)
        
    # Find out which days of Twitter data we haven't sampled from
    sample_names = set([name.split('.')[0] for name in os.listdir(raw_data_path) if 'dataset' in name])
    json_names = set([name.split('.')[0] for name in os.listdir(json_data_path) if 'dataset' in name])
    
    # Test case: just rehydrate files with _test
    if test:
        missing_names = [name in sample_names if 'test' in name]
        print(f'Hydrating test files: {missing_names}')
    else:
        missing_names = sample_names - json_names
        print(f'Here are the missing JSONs: {missing_names}')
        
    # Rehydrate data from days we haven't rehydrated from yet
    for file in sorted(missing_names):
        # Sample a subset of data from our raw ID's
        raw_path = os.path.join(raw_data_path, file + '.tsv')
        data_sample = sample_file(raw_path, sample_rate, id_column)
        
        # Generate a directory/filename to save our hydrated tweets
        name = file + '.jsonl'
        target_path = json_data_path + name
        print(f'saving to {target_path}')
        
        # Write to file
        with open(target_path, 'w') as outfile:
            for tweet in t.hydrate(data_sample):
                outfile.write(json.dumps(tweet) + '\n')
