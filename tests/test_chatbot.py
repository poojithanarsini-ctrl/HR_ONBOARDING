
from unittest.mock import MagicMock, patch

from modules.chatbot import answer_policy_question


def test_chatbot_handles_empty_policy():
    answer = answer_policy_question(
        "What are the leave rules?",
        "",
    )

    assert answer
    assert (
        "policy" in answer.lower()
        or "could not find" in answer.lower()
    )


@patch.dict("os.environ", {}, clear=True)
def test_chatbot_handles_missing_api_key():
    answer = answer_policy_question(
        "What are the working hours?",
        "Working hours are 9:30 AM to 6:00 PM.",
    )

    assert "API key not found" in answer


@patch("modules.chatbot.Groq")
@patch.dict("os.environ", {"GROQ_API_KEY": "test-key"})
def test_chatbot_returns_generated_answer(mock_groq):
    mock_client = MagicMock()
    mock_groq.return_value = mock_client

    mock_client.chat.completions.create.return_value.choices = [
        MagicMock(
            message=MagicMock(
                content="Working hours are 9:30 AM to 6:00 PM."
            )
        )
    ]

    answer = answer_policy_question(
        "What are the working hours?",
        "Working hours are 9:30 AM to 6:00 PM.",
    )

    assert "9:30 AM" in answer
    mock_client.chat.completions.create.assert_called_once()


@patch("modules.chatbot.Groq")
@patch.dict("os.environ", {"GROQ_API_KEY": "test-key"})
def test_chatbot_handles_api_error(mock_groq):
    mock_client = MagicMock()
    mock_groq.return_value = mock_client
    mock_client.chat.completions.create.side_effect = Exception(
        "Simulated API error"
    )

    answer = answer_policy_question(
        "What are the working hours?",
        "Working hours are 9:30 AM to 6:00 PM.",
    )

    assert "couldn't connect" in answer.lower()
