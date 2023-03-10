# PokemonDataBaseProject

Project to store all the pokemon, their regions, and type matchups and allow for the user to search it up
In order to setup you need to a .env file to have your local mysql information(This is so I don't leak my personal info online), also you need to setup a database for mysql and specify the name in the .env

# Steps

## Installation

For this project you will need to install mySql
Install these packages using the `python -m pip install X` format replace python for python3 on mac
`PyYaml`
`streamlit`
`python-dotenv`
`pandas`
`mysql`
`mysql-connector-python`
For the information, create a file `.env` and put PASSWORD = YOURPASS on one line and DATABASE = "PokemonDB"

## Running

Type `streamlit run mainRunner.py` on mac and `python -m streamlit run mainRunner.py`
Everything else should work after that
