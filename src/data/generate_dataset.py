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

# helper method for sample_files
def sample(df, sample_rate, id_column):
    return df.iloc[::sample_rate, :][id_column]

def sample_files(raw_data_path, sample_rate, dehydrated_sample_path, id_column):
    if not os.path.exists(dehydrated_sample_path):
        os.makedirs(dehydrated_sample_path)
    # find the filenames 
    file_names = sorted([name for name in os.listdir(raw_data_path) if 'dataset' in name])
    # for every .tsv under the directory
    for file in file_names:
        # read the file into df
        df = pd.read_table(f'{os.path.join(raw_data_path, file)}')
        # sample it
        a_sample = sample(df, sample_rate, id_column)
        # get the saving file name {original_file_name}.txt 
        fname = file.split('.')[0] + '.txt'
        print(f'sampling for dataset on {fname}')
        # save the sample to the path
        a_sample.to_csv(os.path.join(dehydrated_sample_path, fname), index = False, header = None)

# Get the information from raw tweets we just obtained
# processed_data_path is the path for the sampled dehydrated ids
def rehydrate_tweets(raw_data_path, processed_data_path, project_path, json_data_path, sample_rate, id_column, twarc_location):
    # Sample data and write to processed_data_path
    sample_files(raw_data_path, sample_rate, processed_data_path, id_column)
    
    # Rehydrate text file
    if not os.path.exists(json_data_path):
        os.makedirs(json_data_path)
    for file in os.listdir(processed_data_path):
        # absolute path for txt id file
        abs_path = project_path + os.path.join(processed_data_path, file)
        # absolute path for target directory
        name = file.split('.')[0] + '.jsonl'
        abs_target_path = project_path + json_data_path + name
        print(f'saving to {abs_target_path}')
        
        os.system(f'{twarc_location} hydrate {abs_path} > {abs_target_path}')
