from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
from typing import List
from app.core.settings import settings


# --- Pydantic model for the desired JSON output ---
class PromptVariations(BaseModel):
    """A list of creative and diverse prompts for image generation."""

    variations: List[str] = Field(description="A list of unique prompt strings.")


# --- Initialize the LLM ---
llm = ChatOllama(model=settings.OLLAMA_MODEL, temperature=0.9, format="json")

# --- Create the Output Parser ---
parser = JsonOutputParser(pydantic_object=PromptVariations)


# --- Create the Prompt Template ---
# NOTE: We have removed the conditional logic based on FAST_MODE.
# This agent will now *always* generate 3 prompt variations.
# The "fast" aspect will be handled by the image generation tool, which
# will still create low-quality images quickly if FAST_MODE is enabled.
prompt_template = """
You are a creative assistant and expert prompt engineer for a text-to-image AI.
Your task is to take a user's simple idea and generate a list of 3 diverse, detailed, and imaginative prompts.

- Generate variations based on different styles, moods, and compositions.
- Do NOT just add a few words; create fundamentally different takes on the core concept.
- Ensure the output is a valid JSON object containing a single key "variations" with a list of strings.

USER'S IDEA: {user_idea}

{format_instructions}
"""

prompt = ChatPromptTemplate.from_template(
    template=prompt_template,
    partial_variables={"format_instructions": parser.get_format_instructions()},
)

# --- Create the Ideation Chain ---
ideation_chain = prompt | llm | parser
