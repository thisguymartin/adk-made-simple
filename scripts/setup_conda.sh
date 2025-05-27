#!/usr/bin/env zsh
# Setup Anaconda environment and install dependencies

ENV_NAME="adk-made-simple"
PYTHON_VERSION=3.11

conda create -y -n $ENV_NAME python=$PYTHON_VERSION
conda activate $ENV_NAME
pip install --upgrade pip
pip install -r requirements.txt

echo "[INFO] Conda environment '$ENV_NAME' created and dependencies installed. To activate: conda activate $ENV_NAME"
