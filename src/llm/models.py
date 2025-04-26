import os
from langchain_anthropic import ChatAnthropic
from langchain_deepseek import ChatDeepSeek
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from enum import Enum
from pydantic import BaseModel, SecretStr
from typing import Tuple, Union


class ModelProvider(str, Enum):
    """Enum for supported LLM providers"""

    ANTHROPIC = "Anthropic"
    DEEPSEEK = "DeepSeek"
    GEMINI = "Gemini"
    GROQ = "Groq"
    OPENAI = "OpenAI"


class LLMModel(BaseModel):
    """Represents an LLM model configuration"""

    display_name: str
    model_name: str
    provider: ModelProvider

    def to_choice_tuple(self) -> Tuple[str, str, str]:
        """Convert to format needed for questionary choices"""
        return (self.display_name, self.model_name, self.provider.value)

    def has_json_mode(self) -> bool:
        """Check if the model supports JSON mode"""
        return not self.is_deepseek() and not self.is_gemini()

    def is_deepseek(self) -> bool:
        """Check if the model is a DeepSeek model"""
        return self.model_name.startswith("deepseek")

    def is_gemini(self) -> bool:
        """Check if the model is a Gemini model"""
        return self.model_name.startswith("gemini")


# Define available models
AVAILABLE_MODELS = [
    LLMModel(
        display_name="[anthropic] claude-3.5-haiku",
        model_name="claude-3-5-haiku-latest",
        provider=ModelProvider.ANTHROPIC,
    ),
    LLMModel(
        display_name="[anthropic] claude-3.5-sonnet",
        model_name="claude-3-5-sonnet-latest",
        provider=ModelProvider.ANTHROPIC,
    ),
    LLMModel(
        display_name="[anthropic] claude-3.7-sonnet",
        model_name="claude-3-7-sonnet-latest",
        provider=ModelProvider.ANTHROPIC,
    ),
    LLMModel(
        display_name="[deepseek] deepseek-r1",
        model_name="deepseek-reasoner",
        provider=ModelProvider.DEEPSEEK,
    ),
    LLMModel(
        display_name="[deepseek] deepseek-v3",
        model_name="deepseek-chat",
        provider=ModelProvider.DEEPSEEK,
    ),
    LLMModel(
        display_name="[gemini] gemini-2.0-flash",
        model_name="gemini-2.0-flash",
        provider=ModelProvider.GEMINI,
    ),
    LLMModel(
        display_name="[gemini] gemini-2.5-pro",
        model_name="gemini-2.5-pro-exp-03-25",
        provider=ModelProvider.GEMINI,
    ),
    LLMModel(
        display_name="[groq] llama-4-scout-17b",
        model_name="meta-llama/llama-4-scout-17b-16e-instruct",
        provider=ModelProvider.GROQ
    ),
    LLMModel(
        display_name="[groq] llama-4-maverick-17b",
        model_name="meta-llama/llama-4-maverick-17b-128e-instruct",
        provider=ModelProvider.GROQ
    ),
    LLMModel(
        display_name="[openai] gpt-4.5",
        model_name="gpt-4.5-preview",
        provider=ModelProvider.OPENAI,
    ),
    LLMModel(
        display_name="[openai] gpt-4o",
        model_name="gpt-4o",
        provider=ModelProvider.OPENAI,
    ),
    LLMModel(
        display_name="[openai] o1", model_name="o1", provider=ModelProvider.OPENAI
    ),
    LLMModel(
        display_name="[openai] o3-mini",
        model_name="o3-mini",
        provider=ModelProvider.OPENAI,
    ),
]

# Create LLM_ORDER in the format expected by the UI
LLM_ORDER = [model.to_choice_tuple() for model in AVAILABLE_MODELS]


def get_model_info(model_name: str) -> Union[LLMModel, None]:
    """Get model information by model_name"""
    return next(
        (model for model in AVAILABLE_MODELS if model.model_name == model_name), None
    )


# Define the union of all possible chat model types
ChatModelType = Union[
    ChatOpenAI, ChatGroq, ChatAnthropic, ChatDeepSeek, ChatGoogleGenerativeAI, None
]


def get_model(model_name: str, model_provider: ModelProvider) -> ChatModelType:
    if model_provider == ModelProvider.GROQ:
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            # Print error to console
            print(
                "API Key Error: Please make sure GROQ_API_KEY is set in your .env file."
            )
            raise ValueError(
                "Groq API key not found.  Please make sure GROQ_API_KEY is set in your .env file."
            )
        # Wrap API key in SecretStr
        return ChatGroq(model=model_name, api_key=SecretStr(api_key))
    elif model_provider == ModelProvider.OPENAI:
        # Get and validate API key
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            # Print error to console
            print(
                "API Key Error: Please make sure OPENAI_API_KEY is set in your .env file."
            )
            raise ValueError(
                "OpenAI API key not found.  Please make sure OPENAI_API_KEY is set in your .env file."
            )
        # Wrap API key in SecretStr
        return ChatOpenAI(model=model_name, api_key=SecretStr(api_key))
    elif model_provider == ModelProvider.ANTHROPIC:
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            print(
                "API Key Error: Please make sure ANTHROPIC_API_KEY is set in your .env file."
            )
            raise ValueError(
                "Anthropic API key not found.  Please make sure ANTHROPIC_API_KEY is set in your .env file."
            )
        # Correct keyword argument to model_name, wrap API key, and pass None for optional args
        return ChatAnthropic(
            model_name=model_name, api_key=SecretStr(api_key), timeout=None, stop=None
        )
    elif model_provider == ModelProvider.DEEPSEEK:
        api_key = os.getenv("DEEPSEEK_API_KEY")
        if not api_key:
            print(
                "API Key Error: Please make sure DEEPSEEK_API_KEY is set in your .env file."
            )
            raise ValueError(
                "DeepSeek API key not found.  Please make sure DEEPSEEK_API_KEY is set in your .env file."
            )
        # Wrap API key in SecretStr
        return ChatDeepSeek(model=model_name, api_key=SecretStr(api_key))
    elif model_provider == ModelProvider.GEMINI:
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            print(
                "API Key Error: Please make sure GOOGLE_API_KEY is set in your .env file."
            )
            raise ValueError(
                "Google API key not found.  Please make sure GOOGLE_API_KEY is set in your .env file."
            )
        # Wrap API key in SecretStr
        return ChatGoogleGenerativeAI(model=model_name, api_key=SecretStr(api_key))
    # Add a return statement for the case where the provider is not matched
    return None
