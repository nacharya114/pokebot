#!/bin/bash

conda init bash 

source ~/.bashrc

conda env create -f work/pokebot-env.yml 

conda run -n pb_env python -m ipykernel install --name pb_env --display-name "Python (pokebot)"
