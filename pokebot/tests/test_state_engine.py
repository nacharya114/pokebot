import pytest

from .conftest import *
from pokebot.bots import SimpleStateEngine

@pytest.mark.skip
def test_simple_state_engine(test_battle):

    se = SimpleStateEngine(shape=10)

    battle_state = se.convert(test_battle)

    assert battle_state.shape == se.shape

