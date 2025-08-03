from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
import os


def get_default_model():
    """Get the default model. Uses OpenAI if OPENAI_API_KEY is set, otherwise Anthropic."""
    if os.getenv("OPENAI_API_KEY"):
        return ChatOpenAI(
            model="gpt-4o",
            temperature=0,
            max_tokens=4000
        )
    else:
        return ChatAnthropic(model_name="claude-sonnet-4-20250514", max_tokens=64000)


def get_openai_model(model_name="gpt-4o", temperature=0, max_tokens=4000):
    """Get an OpenAI model specifically."""
    return ChatOpenAI(
        model=model_name,
        temperature=temperature,
        max_tokens=max_tokens
    )


def get_anthropic_model(model_name="claude-sonnet-4-20250514", max_tokens=64000):
    """Get an Anthropic model specifically.""" 
    return ChatAnthropic(model_name=model_name, max_tokens=max_tokens)
