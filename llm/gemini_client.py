import os
from pydantic import BaseModel
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()


def get_structured_completion(
    prompt: str,
    response_model: type[BaseModel],
    model: str | None = None
) -> BaseModel:
    """
    Generate structured output using Gemini API.

    Args:
        prompt: Input prompt.
        response_model: Pydantic response model.
        model: Gemini model name.

    Returns:
        Parsed response model.
    """
    model = model or os.getenv("GEMINI_CHAT_MODEL", "gemini-3.6-flash")

    llm = ChatGoogleGenerativeAI(
        model=model,
        google_api_key=os.getenv("GEMINI_API_KEY"),
        temperature=0
    )

    structured_llm = llm.with_structured_output(response_model)

    full_prompt = f"You are an expert financial analyst.\n\n{prompt}"
    
    response = structured_llm.invoke(full_prompt)
    
    # In some cases, LangChain might return a dict instead of a BaseModel if parsing fails partially,
    # but with_structured_output usually guarantees the BaseModel type for gemini-1.5-pro/flash.
    if isinstance(response, dict):
        return response_model(**response)
        
    return response
