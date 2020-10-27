import sys
import json
from src.data import generate_dataset


# main operation
def main():
    # Load configurations
    with open('./config/data_params.json') as f:
        data_params = json.load(f)
    with open('./config/sample_params.json') as f:
        sample_params = json.load(f)
    
    # Cfg variables
    raw_data_path = data_params['raw_data_path']
    dehydrated_data_path = data_params['dehydrated_data_path']
    rehydrated_data_path = data_params['rehydrated_data_path']
    twarc_path = data_params['twarc_path']
    rehydrated_df_path = data_params['rehydrated_df_path']
    id_column = data_params['id_column']
    
    seed = sample_params['seed']
    sample_size = sample_params['sample_size']
    
    # sample raw data of tweet ids, rehydrate them (enrich them with tweet contents)
    generate_dataset.rehydrate_tweets(raw_data_path, dehydrated_data_path, rehydrated_data_path, seed, sample_size, id_column, twarc_path)
    
    # Load cleaned data
    tweets = generate_dataset.generate_dataframe(rehydrated_data_path, rehydrated_df_path)
    
    return generate_dataset.display_dataframe(rehydrated_df_path)

if __name__ == '__main__':
    args = sys.argv[1:]
    main()
