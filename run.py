import os
import sys
import json
from src.data import clear
from src.data import generate_dataset
from src.features import generate_features
from src.visualization import plot_graphs


# main operation
def main(targets):
    # Clear out data directories
    if 'clean' in targets:
        with open('./config/clear_params.json') as f:
            clear_params = json.load(f)
        
        # Cfg variables
        delete_paths = clear_params['delete_paths']
        
        # Clear out raw data
        clear.clean(delete_paths)
        
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
        
    if 'visualize' in targets:
        with open('./config/viz_params.json') as f:
            viz_params = json.load(f)
        
        # Cfg variables
        path = viz_params['path']
        top_k = viz_params['top_k']
        top_k_fig_path = viz_params['top_k_fig_path']
        user_hist_path = viz_params['user_hist_path']
        user_hist_zoom_path = viz_params['user_hist_zoom_path']
        good_path = viz_params['good_path']
        bad_path = viz_params['bad_path']
        good_tags = viz_params['good_tags']
        bad_tags = viz_params['bad_tags']
        maximum_posts = viz_params['maximum_posts']
        
        jsons = [os.path.join(path, name) for name in sorted(os.listdir(path)) if 'dataset' in name]
        
        # Get features
        hashtag_features = generate_features.count_features(jsons)
        user_features = generate_features.count_features(jsons, mode = 'user')
        scientific_data, misinformation_data = generate_features.count_over_time(jsons, good_tags, bad_tags)
        
        # Get plots
        plot_graphs.top_k_bar(hashtag_features, top_k, top_k_fig_path)
        
        plot_graphs.user_hist(user_features, user_hist_path)
        plot_graphs.user_hist(user_features, user_hist_zoom_path, maximum_posts)
        
        plot_graphs.plot_tags(good_tags, scientific_data, good_path)
        plot_graphs.plot_tags(bad_tags, misinformation_data, bad_path)

if __name__ == '__main__':
    args = sys.argv[1:]
    main(args)
