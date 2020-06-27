# Running the Training Script

It expects 2 params, a path to a training pipeline definition (i.e. 'example.json'), and a save file path for the model. 

`./train.sh example.json <model-name>.h5`

It expects a PS server to be running locally.

## Training pipeline

The example is in `example.json`

Its a JSON object with specific paramters:

```
{
    "policy": {
        "attr": "eps",
        "value_max": 1.0,
        "value_min": 0.2,
        "value_test": 0,
        "nb_steps": 10000
    }, 
    "agent": {
        "nb_actions": 14,
        "nb_steps_warmup": 1000,
        "gamma": 0.5,
        "target_model_update": 1,
        "delta_clip": 0.01
    },
    "state_engine": "HeuristicStateEngine",
    "model": "DQNModel",
    "trainer":"SimpleDQNTrainer",
    "trainer_params": {
        "opponent"  : {
            "type": "SimpleHeuristicsPlayer",
            "format": "gen8randombattle"
        },
        "nbsteps": 10000
    }
}
```

You can have model paramters and state engine parameters as well.