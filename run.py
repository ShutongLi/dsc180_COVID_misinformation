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
    processed_data_path = data_params['dehydrated_data_path']
    twarc_path = data_params['twarc_path']
    rehydrated_df_path = data_params['rehydrated_df_path']
    id_column = data_params['id_column']
    day = data_params['day']

    seed = sample_params['seed']
    sample_size = sample_params['sample_size']
    
    seed = sample_params['seed']
    sample_size = sample_params['sample_size']
    
    
    
    # Update dataset from some date (set in data_params) to today
    generate_dataset.download_latest_datasets(raw_data_path, day)
    # sample raw data of tweet ids, rehydrate them (enrich them with tweet contents)
    print(generate_dataset.rehydrate_tweets(raw_data_path, processed_data_path, seed, sample_size, id_column, twarc_path, day))

if __name__ == '__main__':
    args = sys.argv[1:]
    main()
