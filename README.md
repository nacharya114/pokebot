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

## Resources

- [Showdown Simulator Fork](https://github.com/hsahovic/pokemon-showdown)
- [PokeEnv](https://github.com/hsahovic/poke-env)

## Branch To Do's:
- Create a logger