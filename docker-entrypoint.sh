#!/bin/bash
set -e

if [[ "$1" = "serve" ]]; then
    shift 1
    torchserve --start --ts-config /home/imdb_infer/config.properties --models imdb=imdb.mar --model-store /home/model_store
else
    eval "$@"
fi

# prevent docker exit
tail -f /dev/null