import pytest
from uuid import uuid4


@pytest.fixture
def user_evaluate_payload():
    """
    Returns a valid payload dictionary for authenticated track evaluation calls.
    TrackNum matches the exact database integer type requirements.
    """
    return {
        "id_source": str(uuid4()),
        "TrackNum": 12
    }


@pytest.fixture
def noname_evaluate_payload():
    """
    Returns a valid payload dictionary for anonymous track evaluation calls.
    TrackNum matches the exact database integer type requirements.
    """
    return {
        "id_source": str(uuid4()),
        "TrackNum": 1
    }
