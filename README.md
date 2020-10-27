# The Spread of Misinformation on Twitter
Observing how misinformation and conspiracies are spread through social media.

## Overview

Our goal currently is to construct a proper data ingestion pipeline, which will properly rehydrate a set of Tweet ID's obtained from the [Panacea Lab at Georgia State University](http://www.panacealab.org/covid19/). This dataset will then be loaded as a Pandas DataFrame for later analysis.

## Contents

A requirements.txt file is included for installing the necessary packages to run the code. However, we use the [Twarc package](https://scholarslab.github.io/learn-twarc/), which requires a Twitter API key to run properly.

Raw data is taken from a local/remote directory not included in this repository. Its paths are located in the config directory (data_params.json), and can be changed for replicative use. 

Our source code currently houses our data ingestion program, under the data directory.

## How to Run
Please configure Twarc with your proper keys before running with the following command:

```
twarc configure
```

Note that you may not be able to run Twarc on DSMLP properly without accessing its file path, in which case you can run the following:

```
~/.local/bin/twarc configure
```

After you have [properly configured Twarc](https://scholarslab.github.io/learn-twarc/01-quick-start.html), set your data paths 
to your Tweet ID set. Running run.py will return a set of properly rehydrated tweets. 