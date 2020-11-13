import sys
import json
from src.data import generate_dataset
from src.data import clear


# main operation
def main(targets):
    # Clear out raw data directory
    if 'clean' in targets:
        with open('./config/data_params.json') as f:
            data_params = json.load(f)
        
        # Cfg variables
        raw_data_path = data_params['raw_data_path']
        
        # Clear out raw data
        clear.obliviate(raw_data_path)
        
    # Download and rehydrate Tweets pertaining to COVID-19
    if 'data' in targets:
        with open('./config/data_params.json') as f:
            data_params = json.load(f)
        with open('./config/sample_params.json') as f:
            sample_params = json.load(f)

        # Cfg variables
        raw_data_path = data_params['raw_data_path']
        rehydrated_json_path = data_params['rehydrated_json_path']
        api_keys = data_params['api_keys']
        from_day = data_params['from_day']
        to_day = data_params['to_day']
        id_column = data_params['id_column']
        want_cleaned = data_params['want_cleaned']

        sample_rate = sample_params['sample_every']

        # Update dataset from some date (set in data_params) to today
        generate_dataset.download_latest_datasets(raw_data_path, from_day, to_day, want_cleaned)
        
        # Rehydrate a subsample of tweet data
        generate_dataset.rehydrate_tweets(raw_data_path, rehydrated_json_path, sample_rate, id_column, api_keys)

if __name__ == '__main__':
    args = sys.argv[1:]
    main(args)
