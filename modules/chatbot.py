
import os
from dotenv import load_dotenv
from groq import Groq

from modules.policy_guardrails import (
    build_guardrail_prompt,
    get_fallback_response,
)

load_dotenv()


def answer_policy_question(question: str, policy_text: str) -> str:
    """Answer questions using the supplied HR policy document."""

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        return "Groq API key not found. Please check your .env file."

    if not policy_text or not policy_text.strip():
        return get_fallback_response()

    prompt = build_guardrail_prompt(question, policy_text)

    if not prompt:
        return get_fallback_response()

    try:
        client = Groq(api_key=api_key)

        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an HR policy assistant. "
                        "Use only the supplied policy evidence. "
                        "Never invent policies or disclose private data."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
        )

        answer = response.choices[0].message.content

        return answer or get_fallback_response()

    except Exception as exc:
        print(f"Groq error: {exc}")
        return (
            "Sorry, I couldn't connect to the HR answer service. "
            "Please try again later."
        )
