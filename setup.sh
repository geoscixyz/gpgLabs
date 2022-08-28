#!/bin/bash

# init mamba
mamba init
source ~/.bashrc

# install environment for user
mamba env create -f environment.yml --prefix ./envs

# activate enviornment
mamba activate ./envs
python -m ipykernel install --user --name=e350

# success
echo "Success!"
