import os
import sys
import json
from src.data import clear
from src.data import generate_dataset
from src.features import calculate_stats
from src.models import construct_polarities
from src.visualization import plot_graphs


# main operation
def main(targets):
    # Run all
    if 'all' in targets:
        targets = ['data', 'statistics', 'build', 'clean']
        
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

    if 'statistics' in targets:
        with open('./config/stat_params.json') as f:
            stat_params = json.load(f)
        
        # Cfg variables
        path = stat_params['path']
        top_k = stat_params['top_k']
        top_k_fig_path = stat_params['top_k_fig_path']
        user_hist_path = stat_params['user_hist_path']
        user_hist_zoom_path = stat_params['user_hist_zoom_path']
        good_path = stat_params['good_path']
        bad_path = stat_params['bad_path']
        good_tags = stat_params['good_tags']
        bad_tags = stat_params['bad_tags']
        maximum_posts = stat_params['maximum_posts']
        
        jsons = [os.path.join(path, name) for name in sorted(os.listdir(path)) if 'dataset' in name]
        
        # Get features
        hashtag_features = calculate_stats.count_features(jsons)
        user_features = calculate_stats.count_features(jsons, mode = 'user')
        scientific_data, misinformation_data = calculate_stats.count_over_time(jsons, good_tags, bad_tags)
        
        # Get plots
        plot_graphs.top_k_bar(hashtag_features, top_k, top_k_fig_path)
        
        plot_graphs.user_hist(user_features, user_hist_path)
        plot_graphs.user_hist(user_features, user_hist_zoom_path, maximum_posts)
        
        plot_graphs.plot_tags(good_tags, scientific_data, good_path)
        plot_graphs.plot_tags(bad_tags, misinformation_data, bad_path)
        
    if 'build' in targets:
        with open('./config/polarity_params.json') as f:
            polarity_params = json.load(f)  
            
        # Cfg variables
        top_k = polarity_params['top_k']
        api_keys = polarity_params['api_keys']
        marker_tags = polarity_params['marker_tags']
        max_posts = polarity_params['max_posts']
        start_date = polarity_params['start_date']
        end_date = polarity_params['end_date']
        date_pattern = polarity_params['twitter_date_pattern']
        max_iter = polarity_params['max_iter']
        toi_con = polarity_params['toi_con']
        num_retrieve_con = polarity_params['num_retrieve_con']
        toi_sci = polarity_params['toi_sci']
        con_path = polarity_params['con_path']
        sci_path = polarity_params['sci_path']
        viz_path = polarity_params['viz_path']
        data_path = polarity_params['data_path']
        
        jsons = [os.path.join(data_path, name) for name in sorted(os.listdir(data_path)) if 'dataset' in name]
        
        # Get Tweepy API functions
        api = construct_polarities.get_tweepy_api(api_keys)
        
        # Get Hashtag Polarities
        ht_polarity = construct_polarities.hashtag_polarity(jsons, top_k, marker_ht = marker_tags)
        
        # Show retweet polarity histograms and user polarities from relevant users
        up_dict = construct_polarities.investigate_retweets(toi_sci, num_retrieve_con,
                                           set(ht_polarity.index), 
                                           start_date, end_date, date_pattern,
                                           ht_polarity, sci_path,
                                           max_posts = max_posts,
                                           api = api,
                                           max_iter=max_iter)
        
        up_dict_con = construct_polarities.investigate_retweets(toi_con, num_retrieve_con,
                                           set(ht_polarity.index), 
                                           start_date, end_date, date_pattern,
                                           ht_polarity, con_path,
                                           max_posts = max_posts,
                                           api = api,
                                           max_iter=max_iter)
        
        plot_graphs.plot_histograms(up_dict, up_dict_con, viz_path)

    # Clear out data directories
    if 'clean' in targets:
        with open('./config/clear_params.json') as f:
            clear_params = json.load(f)
        
        # Cfg variables
        delete_paths = clear_params['delete_paths']
        
        # Clear out raw data
        clear.clean(delete_paths)
        
    if 'test' in targets:
        with open('./config/test_params.json') as f:
            test_params = json.load(f)
        
        # Cfg variables
        path = test_params['path']
        top_k = test_params['top_k']
        top_k_fig_path = test_params['top_k_fig_path']
        user_hist_path = test_params['user_hist_path']
        user_hist_zoom_path = test_params['user_hist_zoom_path']
        good_path = test_params['good_path']
        bad_path = test_params['bad_path']
        good_tags = test_params['good_tags']
        bad_tags = test_params['bad_tags']
        maximum_posts = test_params['maximum_posts']
        marker_tags = test_params['marker_tags']
        max_posts = test_params['max_posts']
        start_date = test_params['start_date']
        end_date = test_params['end_date']
        date_pattern = test_params['twitter_date_pattern']
        max_iter = test_params['max_iter']
        toi_con = test_params['toi_con']
        num_retrieve_con = test_params['num_retrieve_con']
        toi_sci = test_params['toi_sci']
        con_path = test_params['con_path']
        sci_path = test_params['sci_path']
        viz_path = test_params['viz_path']
        
        jsons = [os.path.join(path, name) for name in sorted(os.listdir(path)) if 'test' in name]
        
        # Get features
        hashtag_features = calculate_stats.count_features(jsons)
        user_features = calculate_stats.count_features(jsons, mode = 'user')
        scientific_data, misinformation_data = calculate_stats.count_over_time(jsons, good_tags, bad_tags)
        
        # Get plots
        plot_graphs.top_k_bar(hashtag_features, top_k, top_k_fig_path)
        
        plot_graphs.user_hist(user_features, user_hist_path)
        plot_graphs.user_hist(user_features, user_hist_zoom_path, maximum_posts)
        
        plot_graphs.plot_tags(good_tags, scientific_data, good_path)
        plot_graphs.plot_tags(bad_tags, misinformation_data, bad_path)
        
        # Get Hashtag Polarities
        ht_polarity = construct_polarities.hashtag_polarity(jsons, top_k, marker_ht = marker_tags)
        
        # Show retweet polarity histograms and user polarities from relevant users
        up_dict = construct_polarities.investigate_retweets(toi_sci, num_retrieve_con,
                                           set(ht_polarity.index), 
                                           start_date, end_date, date_pattern,
                                           ht_polarity, sci_path,
                                           max_posts = max_posts,
                                           api = None,
                                           max_iter=max_iter)
        
        up_dict_con = construct_polarities.investigate_retweets(toi_con, num_retrieve_con,
                                           set(ht_polarity.index), 
                                           start_date, end_date, date_pattern,
                                           ht_polarity, con_path,
                                           max_posts = max_posts,
                                           api = None,
                                           max_iter=max_iter)
        
        plot_graphs.plot_histograms(up_dict, up_dict_con, viz_path)
        
if __name__ == '__main__':
    args = sys.argv[1:]
    main(args)
