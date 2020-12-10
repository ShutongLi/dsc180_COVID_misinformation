import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def plot_histograms(up_dict, up_dict_con, save_path):
    plt.clf()
    pd.Series(up_dict).dropna().hist(density=1, label = 'scientific tweet', alpha=0.7)
    pd.Series(up_dict_con).dropna().hist(density = 1, label = 'conspiracy tweet', alpha=0.7)
    
    plt.legend()
    plt.savefig(save_path, bbox_inches='tight')
    return plt

# Get the top k entries in the features
def top_k_bar(feature, k, save_path):
    plt.clf()
    plt.figure(figsize = (15, 14))
    sns.barplot(y = feature.iloc[:k].index, x = feature.iloc[:k].values)
    plt.savefig(save_path, bbox_inches='tight')
    return plt
    
    
# Generate a histogram of the features
def user_hist(feature, save_path, maximum_posts = None):
    plt.clf()
    feature = feature.rename('posts per user')
    plt.figure(figsize = (15, 14))
    if maximum_posts is None:
        sns.distplot(feature)
    else:
        sns.distplot(feature.loc[feature < maximum_posts])
    plt.title('density of number of posts per user')
    plt.savefig(save_path, bbox_inches='tight')
    return plt


# Observe hashtag usage over time
def plot_tags(tags, data, save_path):
    plt.clf()
    plt.figure(figsize = (15, 10))
    for tag in tags:
        plt.plot([x[tag] for x in data], label = tag)
    plt.legend()
    plt.savefig(save_path, bbox_inches='tight')
    return plt
    