#!/usr/bin/env bash

set -e

python -m nltk.downloader wordnet wordnet_ic stopwords words punkt averaged_perceptron_tagger
