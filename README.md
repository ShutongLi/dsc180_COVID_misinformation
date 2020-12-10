
# The Spread of Misinformation on Twitter
Observing how misinformation and conspiracies are spread through social media.

## Overview

Our goal explore the ways and extent to which misinformation is spread throughout social media platforms, specifically Twitter. Our scope will be limited to the current COVID-19 pandemic, and data will be obtained from the [Panacea Lab at Georgia State University](http://www.panacealab.org/covid19/). 

## Contents

- `src` contains the source code of our project, including algorithms for data extraction, analysis, and modelling.
- `notebooks` contain some examples of the models this code will generate, detailing our findings under the circumstances in which we conducted our testing.
- `config` contains easily changable parameters to test the data under various circumstances or change directories as needed.
- `run.py` will build and run different the different parts of the source code, as needed by the user.
- `references` cite the sources we used to construct this project.
- `requirements.txt` lists the Python package dependencies of which the code relies on. 
- Alternatively, `Dockerfile` and `run_jupyter.sh` are both included in case a user may want to recreate our project environment.


## How to Run

- To properly obtain the data from Twitter, you must first apply for a [Developer Account](https://developer.twitter.com/en/apply-for-access) to obtain API keys.
- Save your tokens in the following JSON format in project root directory (or wherever you set your API_key directory to in `config/data_params.json`):
```
{
    "consumer_key": [Your Consumer Key],
    "consumer_secret": [Your Secret Consumer Key],
    "access_token": [Your Access Token],
    "access_token_secret": [Your Secret Access Token]
}
```
- Install the dependencies by running `pip install -r requirements.txt` from the root directory of the project.
- Alternately, you may reference our Dockerfile to recreate our environment (or use the existing dockerhub repository, [yunghas/spread_of_misinformation](https://hub.docker.com/repository/docker/yunghas/spread_of_misinformation)).

### Building the project stages using `run.py`
- To download and rehydrate the data, run `python run.py data`
	- This downloads, samples, and transforms data from the Panacea Lab repository to the directory specified in `config/data_params.json`
- To clean up and delete excess data, run `python run.py clean`
	- This deletes all files and directories within the directory specified in `config/clear_params.json`
- To process some general statistics and run some visualizations on them, run `python run.py statistics`
	- This aggregates some statistics on the data, and prints visualizations to the directories specified in `config/viz_params.json`
- To build a histogram visualizing the polarities associated with a retweeted post, run `python run.py build`
	- This takes two heavily retweeted tweets from `config/build_params.json`, presumably one scientific and the other misinformative, and prints visualizations to the directories specified in `config/build_params.json`
- To run all of these steps at once, run `python run.py all`

## Project Work Splits
Hasan
- Implemented hashtag polarity algorithm
- Implemented user polarity algorithm
- Cleaned up project targets
- Updated README

Shutong
- Implemented retweet polarity calculation
- Optimized user polarity algorithm
- Developed retweet polarity visualization
- Reworked src files for run.py
