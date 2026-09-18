import os
import re
import json

from openai import OpenAI
import openai
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()


def get_openai_client() -> OpenAI:
    """
    Create OpenAI client.

    Returns:
        OpenAI client.
    """
    return OpenAI(
        api_key=os.getenv("OPENAI_API_KEY")
    )


def get_structured_completion(
    prompt: str,
    response_model: type[BaseModel],
    model: str | None = None
) -> BaseModel:
    """
    Generate structured output.

    Args:
        prompt: Input prompt.
        response_model: Pydantic response model.
        model: OpenAI model name.

    Returns:
        Parsed response model.
    """
    model = model or os.getenv("OPENAI_CHAT_MODEL", "gpt-4o")

    client = get_openai_client()

    messages = [
        {
            "role": "system",
            "content": "You are an expert financial analyst."
        },
        {
            "role": "user",
            "content": prompt
        }
    ]

    try:
        response = client.beta.chat.completions.parse(
            model=model,
            messages=messages,
            response_format=response_model
        )

        try:
            parsed = response.choices[0].message.parsed
            print("[debug] Structured parsed output:", parsed)
        except Exception:
            print("[debug] Structured response received but could not access parsed field")

        return response.choices[0].message.parsed

    except openai.BadRequestError as exc:
        msg = str(exc)
        if "response_format" in msg or "json_schema" in msg or "Structured Outputs" in msg:
            fallback = client.chat.completions.create(
                model=model,
                messages=messages
            )

            text = fallback.choices[0].message.content
            print("[debug] Fallback raw text response:\n", text)

            match = re.search(r"\{.*\}", text, re.S)
            json_text = match.group(0) if match else text

            try:
                if isinstance(json_text, str) and json_text.strip() in ("null", "None", ""):
                    if hasattr(response_model, "model_construct"):
                        return response_model.model_construct()
                    try:
                        return response_model.model_validate({}) if hasattr(response_model, "model_validate") else response_model.parse_obj({})
                    except Exception:
                        raise RuntimeError("Model returned null and cannot construct an empty instance.")

                if hasattr(response_model, "model_validate_json"):
                    parsed = response_model.model_validate_json(json_text)
                else:
                    parsed = response_model.parse_raw(json_text)

                return parsed
            except Exception as e:
                raise RuntimeError(f"Failed to parse JSON fallback response: {e}\nRaw output:\n{text}") from e

        raise
