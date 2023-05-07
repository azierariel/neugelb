#!/bin/bash

echo $@

if [[ $@ == 'articles-download' ]]
then
    python pipelines/articles_download.py
elif [[ $@ == 'articles-import' ]]
then
    python pipelines/articles_import.py
elif [[ $@ == 'sources-download' ]]
then
    python pipelines/sources_download.py
elif [[ $@ == 'sources-import' ]]
then
    python pipelines/sources_import.py
else
    echo "Invalid argument"
fi
