#########################
# Author: Neil Acharya 
# 
# Generic Model Definition
#########################

from tensorflow.keras.layers import Dense, Flatten
from tensorflow.keras.models import Sequential

from ..bots.bot import BotPlayer


class DQNModel:

    def __init__(self, player: BotPlayer):
        self.player = player
        self.model = None
        self.setup_model_layers()

    def setup_model_layers(self):
        self.model = Sequential()
        self.model.add(Dense(128, activation="elu", input_shape=(1, self.player.state_engine.shape,)))

        # Our embedding have shape (1, 10), which affects our hidden layer dimension and output dimension
        # Flattening resolve potential issues that would arise otherwise
        self.model.add(Flatten())
        self.model.add(Dense(64, activation="relu"))
        self.model.add(Dense(len(self.player.action_space()), activation="linear"))



