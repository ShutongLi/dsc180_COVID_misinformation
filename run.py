import sys
import json
from src.data import generate_dataset


# main operation
def main():
    # Load configurations
    data_params = json.loads('/dsc180_project_structure/config/data_params.json')
    sample_params = json.loads('/dsc180_project_structure/config/sample_params.json')
    
    # Cfg variables
    raw_data_path = data_params['raw_data_path']
    dehydrated_data_path = data_params['dehydrated_data_path']
    rehydrated_data_path = data_params['rehydrated_data_path']
    id_column = data_params['id_column']
    
    seed = sample_params['seed']
    sample_size = sample_params['sample_size']
    
    # Clean raw data
    generate_dataset.rehydrate_tweets(raw_data_path, dehydrated_data_path, hydrated_data_path, seed, sample_size, id_column)
    
    # Load cleaned data
    tweets = read_dataframe(hydrated_data_path)

if __name__ == '__main__':
    args = sys.argv[1:]
    main()
