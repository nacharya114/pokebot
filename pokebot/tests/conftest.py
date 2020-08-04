import pytest
from unittest.mock import MagicMock

from poke_env.environment.battle import Battle


@pytest.fixture()
def test_battle():

    logger = MagicMock()

    battle = Battle("tag", "username", logger)

    yield battle