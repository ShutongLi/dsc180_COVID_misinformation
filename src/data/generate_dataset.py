import os
import pandas as pd
import json

def rehydrate_tweets(raw_data_path, dehydrated_data_path, rehydrated_data_path, seed, sample_size, id_column, twarc_location):
    # Sample data to rehydrate
    df = pd.read_table(raw_data_path)
    id_sample = df[id_column].sample(n=sample_size, replace = False, random_state = seed)

    # Create text file for rehydration
    id_sample.to_csv(dehydrated_data_path, index=False, header=False)

    # Input API keys
#     os.system('twarc configure')
    # Rehydrate text file
    os.system(f'{twarc_location} hydrate {dehydrated_data_path} > {rehydrated_data_path}')


# !!! file path for the jsonl is changed to relative here due to unknown error
def generate_dataframe(rehydrated_data_path, rehydrated_df_path):
    rehydrated_fp = rehydrated_data_path.replace('~/dsc180_project_structure/', '')
    rehydrated_df_fp = rehydrated_df_path
    
    with open(rehydrated_fp) as rh_fh:
        json_content = rh_fh.read()
    rows = []
    for line in json_content.splitlines():
        rows.append(json.loads(line))
    tweets = pd.DataFrame(rows)
    tweets['hashtags'] = tweets['entities'].apply(lambda x: [tag['text'] for tag in x['hashtags']])
    tweets.to_csv(rehydrated_df_fp, index = False)
    
def display_dataframe(rehydrated_df_path):
    return pd.read_csv(rehydrated_df_path)