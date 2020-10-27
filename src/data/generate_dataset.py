import os
import pandas as pd
import json

def rehydrate_tweets(raw_data_path, dehydrated_data_path, rehydrated_data_path, seed, sample_size, id_column):
    # Sample data to rehydrate
    df = pd.read_table(raw_data_path)
    id_sample = df[id_column].sample(n=sample_size, replace = False, random_state = seed)

    # Create text file for rehydration
    id_sample.to_csv(dehydrated_data_path, index=False, header=False)

    # Input API keys
    os.system('twarc configure')
    # Rehydrate text file
    os.system('twarc hydrate ' + dehydrated_data_path + ' > ' + rehydrated_data_path)
    
def read_dataframe(rehydrated_data_path):
    return pd.read_csv(rehydrated_data_path)