# Pokemon Showdown Bot Repository

The goal of this repo is to create an ongoing bot to play in Smogon OU.

We will be using the `poke-env` pip package to abstract the Pokemon Showdown API.
We wil also be using a specific fork of the Pokemon Showdown Simulator, since that has uncapped move rates for faster training.

## Installation

```
git clone https://github.com/nacharya114/pokebot.git
cd pokebot
pip install -r requirements.txt
pip install -e .
```

Make sure you're running the below fork of Pokemon Showdown with: `node pokemon-showdown`

After that, you can go into the PlayerScratchPad notebook and run the code there for a SimpleDQNAgent.

## Package Setup

This repo has 3 different modules: `bot`, `model`, and `trainer`

- `bot` Has the class BotPlayer that accepts different `StateEngine`'s which consume `poke_env.environment.Battle` objects and produces a 1D Vector.
- `model` contains the different models used either in bot or trainer
- `trainer` implements the `Trainer` class which is used to run the training loop against specific opponents, and evalutates the model against other opponents, as well as allows the agent to challenge live servers.
## Resources

- [Showdown Simulator Fork](https://github.com/hsahovic/pokemon-showdown)
- [PokeEnv](https://github.com/hsahovic/poke-env)

## Branch To Do's:
- [ ] Create a logger
- [X] Create a training script for background running
- [X] Create State Representation for a more sophisticated model