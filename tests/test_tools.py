from app.agent.tools import generate_image
from langchain_core.tools import BaseTool

def test_generate_image_is_tool():
    """Tests that the generate_image function is a LangChain tool."""
    assert isinstance(generate_image, BaseTool)
