
# The Spread of Misinformation on Twitter
Observing how misinformation and conspiracies are spread through social media.

## Overview

Our goal explore the ways and extent to which misinformation is spread throughout social media platforms, specifically Twitter. Our scope will be limited to the current COVID-19 pandemic, and data will be obtained from the [Panacea Lab at Georgia State University](http://www.panacealab.org/covid19/). 

## Contents

- `src` contains the source code of our project, including algorithms for data extraction, analysis, and modelling.
- `notebooks` contain some examples of the models this code will generate, detailing our findings under the circumstances in which we conducted our testing.
- `config` contains easily changable parameters to test the data under various circumstances or change directories as needed.
- `run.py` will build and run different the different parts of the source code, as needed by the user.
- `requirements.txt` lists the Python package dependencies of which the code relies on. 
- `references` cite the sources we used to construct this project.


## How to Run

- To properly obtain the data from Twitter, you must first apply for a [Developer Account](https://developer.twitter.com/en/apply-for-access) to obtain API keys.
- Save your tokens in the following JSON format in your home directory (or wherever you set your API_key directory to in `config/data_params.json`):
```
{
    "consumer_key": [Your Consumer Key],
    "consumer_secret": [Your Secret Consumer Key],
    "access_token": [Your Access Token],
    "access_token_secret": [Your Secret Access Token]
}
```
- Install the dependencies by running `pip install -r requirements.txt` from the root directory of the project.
- 
### Building the project stages using `run.py`
- To download and rehydrate the data, run `python run.py data`
	- This downloads, samples, and transforms data from the Panacea Lab repository to the directory specified in `config/data_params.json`
- To clean up and delete excess data, run `python run.py clean`
	- This deletes all files and directories within the directory specified in `config/clear_params.json`

## Project Work Splits
Hasan
- Overhauled data download/hydration
- Established project targets
- Implemented minor version control fixes
- Updated README

Shutong
- Overhauled data download/hydration
- Implemented feature extraction
- Developed figure generating code for EDA
- Wrote EDA
