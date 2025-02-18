from datetime import datetime, timedelta

import pytest


@pytest.fixture
def valid_token():
    return create_test_token(sub="test_user", exp=datetime.utcnow() + timedelta(hours=1))