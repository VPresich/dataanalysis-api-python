import pytest
from uuid import uuid4


# @pytest.fixture
# def user_evaluate_payload():
#     """
#     Returns a valid payload dictionary for authenticated track evaluation calls.
#     TrackNum matches the exact database integer type requirements.
#     """
#     return {
#         "id_source": "62f5e11f-0a40-4a66-8429-8da6e088c999",
#         "TrackNum": 121
#     }


@pytest.fixture
def user_evaluate_payload():
    """
    Returns a valid payload dictionary for authenticated track evaluation calls.
    TrackNum matches the exact database integer type requirements.
    """
    return {
        "id_source": "62f5e11f-0a40-4a66-8429-8da6e088c999",
        "TrackNum": 45
    }


# @pytest.fixture
# def noname_evaluate_payload():
#     """
#     Returns a valid payload dictionary for anonymous track evaluation calls.
#     TrackNum matches the exact database integer type requirements.
#     """
#     return {
#         "id_source": "6649a534-3921-4cfb-94d7-335cd5725ff2",
#         "TrackNum": 18
#     }


# @pytest.fixture
# def noname_evaluate_payload():
#     """
#     Returns a valid payload dictionary for anonymous track evaluation calls.
#     TrackNum matches the exact database integer type requirements.
#     """
#     return {
#         "id_source": "877e00c3-a903-4da7-a2b4-2c5dabbd0c7d",
#         "TrackNum": 1188
#     }


@pytest.fixture
def noname_evaluate_payload():
    """
    Returns a valid payload dictionary for anonymous track evaluation calls.
    TrackNum matches the exact database integer type requirements.
    """
    return {
        "id_source": "877e00c3-a903-4da7-a2b4-2c5dabbd0c7d",
        "TrackNum": 20
    }
