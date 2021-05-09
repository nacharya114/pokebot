# Pokemon Showdown Bot Repository

The goal of this repo is to create an ongoing bot to play in Smogon OU.

We will be using the `poke-env` pip package to abstract the Pokemon Showdown API.
We wil also be using a specific fork of the Pokemon Showdown Simulator, since that has uncapped move rates for faster training.

## Installation

For environment creation, we used conda

```
git clone https://github.com/nacharya114/pokebot.git
cd pokebot
conda env create -f pokebot-env.yml
pip install -e .
```

Make sure you're running Pokemon Showdown with this flag: `./pokemon-showdown --no-security` OR download and run my docker image that automatically starts up the server for you: `docker.io/nacharya114/pokemonshowdown:latest`

After that, you can go into the Training Notebook and run the code there for a SimpleDQNAgent and also challenge it to a live battle.

### Run Time Alternative (Docker)

Alternatively, once you've downloaded and cloned this repo, you can use docker to get the training pipeline up and running. There are two `docker-compose.yml`'s in this repo, one at the base level and one inside of `notebooks`. 

#### Jupyter Notebook

The docker compose file inside of the notebook subdirectory automatically starts up a pokemon showdown server for you, as well as initializes a jupyter lab environment with the appropriate kernel already to use. This is handy for quick experiments and for allowing a visual interface for your training if you can afford to have it open for long durations. All you need to do is create a `.env` file in the `notebooks` sudirectory with a variable pointing to your local pokebot repo:
```
# pokebot/notebooks/.env
HOME_DIR=/home/nacharya/pokebot
```

After that, just running `docker compose up` should get you up and running. 

#### Detached Container

On the other hand, if you want to run this whole process in a detached executor and just want the model weights, the `docker-compose.yml` at the base directory of this repo will let you run just that. This compose will simply wait for the pokemon showdown server to come up, start up a conda environment, and run your training loop. The results will be mounted to docker volume which you can access later.

In order pass in different `hparams.json`'s in, you can mount a new volume and change the location in the command dictionary:

```
...
  trainer:
    build: .
    command: [ "scripts/train.py", 
            "/home/pokebot/new-hparams/hparams.json",  <-- Change this 
            "/home/pokebot/models",
            # "--no-wandb" # uncomment this line if you wand to integrate with Weights & Biases. 
            "--server", "ps:8000"
            ]
    volumes: 
      - models:/home/pokebot/models
      - '<path-to-local-hparams.json>:/home/pokebot/new-hparams' <--- based on this
...
```

To run this is a detached process, simply run `docker compose up -d`

## Package Setup

This repo has 3 different modules: `bot`, `model`, and `trainer`

- `bot` Has the class BotPlayer that accepts different `StateEngine`'s which consume `poke_env.environment.Battle` objects and produces a 1D Vector.
- `model` contains the different models used either in bot or trainer
- `trainer` implements the `Trainer` class which is used to run the training loop against specific opponents, and evalutates the model against other opponents, as well as allows the agent to challenge live servers.
## Resources

- [Showdown Simulator](https://github.com/hsahovic/pokemon-showdown)
- [PokeEnv](https://github.com/hsahovic/poke-env)

## Branch To Do's:
- [ ] Create a logger
- [X] Create a training script for background running
- [X] Create State Representation for a more sophisticated model