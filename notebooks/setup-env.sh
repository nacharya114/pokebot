#!/bin/bash

conda env create -f pokebot-env.yml -y

conda run -n pb_env /bin/bash -c python -m ipykernel install --name pb_env --display-name "Python (pokebot)"
