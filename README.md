# The Spread of Misinformation on Twitter
Observing how misinformation and conspiracies are spread through social media.

## Overview

Our goal explore the ways and extent to which misinformation is spread throughout social media platforms, specifically Twitter. Our scope will be limited to the current COVID-19 pandemic, and data will be obtained from the [Panacea Lab at Georgia State University](http://www.panacealab.org/covid19/). 

## Contents

A requirements.txt file is included for installing the necessary packages to run the code. However, we use the [Twarc package](https://scholarslab.github.io/learn-twarc/), which requires a Twitter API key to run properly.

Raw data is taken from a local/remote directory not included in this repository. Its paths are located in the config directory (data_params.json), and can be changed for replicative use. 

Our source code currently houses our data ingestion program, under the data directory.

## How to Run
Please configure Twarc with your proper keys before running with the following command:

```
twarc configure
```

Note that you may not be able to run Twarc without specifying the correct file location. A Docker setup will be provided in the near future.

After you have [properly configured Twarc](https://scholarslab.github.io/learn-twarc/01-quick-start.html), set your data paths 
to your Tweet ID set. Running run.py will return a set of properly rehydrated tweets. 