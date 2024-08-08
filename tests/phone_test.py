"""Sample test module."""

from wsp import send_message, send_template_message

# TEST_NUMBER = "+51984724707"
TEST_NUMBER = "+51981052222"


TEMPLATE_SID = "HX0afd65098f0e2e1aad733fab810dbc0f"
MESSAGING_SERVICE_SID = "MG606f479a9e8797803e0f6fe0767ce119"


def test_send_hello_message() -> None:
    """Send a hello message to a phone number."""
    send_message(TEST_NUMBER, "Hello, World!")
    assert True


def test_send_template_message() -> None:
    """Send a template message to a phone number."""
    content_variables = {"1": "21"}
    send_template_message(
        TEST_NUMBER, TEMPLATE_SID, content_variables, MESSAGING_SERVICE_SID
    )
