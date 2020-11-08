import os
import pandas as pd
import requests
import gzip
import shutil
from datetime import datetime, date, timedelta

# pre-condition: from_time does not change to an earlier time (kinda bad but doesn't hurt here)
# Get the last_day_added based on the latest date in your dataset
def get_last_day(raw_data_path, from_time):
    # Failsafe in case you have no raw data
    last_day_added = datetime.strptime(from_time, '%Y-%m-%d').date()
    # Get all filenames of our raw data
    for name in os.listdir(raw_data_path):
        # Just in case a file name doesn't have the date
        try:
            # Get the date from the name
            name_date = datetime.strptime(name[:10], '%Y-%m-%d').date()
            # Get maximum date
            if last_day_added < name_date:
                last_day_added = name_date
        except:
            print(f'{name} does not have a date.')
    return last_day_added

# Updates your dataset FROM from_time date (YYYY-MM-DD) TO today
def download_latest_datasets(raw_data_path, from_time, to_time, cleaned = False):
    # Get days of data between range
    last_day = get_last_day(raw_data_path, from_time)
    days_between = pd.date_range(last_day, to_time, freq='d')
    
    # suffix _cleaned needed
    clean_suffix = ''
    if cleaned:
        clean_suffix = '_clean'
    
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
            filename = f'{raw_data_path}/gzips/{day_str}{clean_suffix}-dataset.tsv.gz'
            filename2 = f'{raw_data_path}/{day_str}{clean_suffix}-dataset.tsv'
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
    return 

# Get the information from raw tweets we just obtained
def rehydrate_tweets(raw_data_path, processed_data_path, seed, sample_size, id_column, twarc_location, day):
    # Sample data to rehydrate
    df = pd.read_table(f'{raw_data_path}/{day}_clean-dataset.tsv')
    id_sample = df[id_column].sample(n=sample_size, replace = False, random_state = seed)

    # Create text file for rehydration
    id_sample.to_csv(f'{processed_data_path}/{day}_tweet_ids', index=False, header=False)

    # Rehydrate text file
    os.system(f'{twarc_location} hydrate {processed_data_path}/{day}_tweet_ids > {processed_data_path}/{day}_tweets_hydrated.jsonl')
    
    # Display example
    return pd.read_json(f'{processed_data_path}/{day}_tweets_hydrated.jsonl', lines=True).head()
