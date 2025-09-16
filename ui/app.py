import streamlit as st
import requests
import base64
from PIL import Image
import io
import textwrap

# --- Configuration ---
API_BASE_URL = "http://localhost:8000"  # URL of your FastAPI backend
st.set_page_config(layout="wide", page_title="AI Design Agent")


# --- API Communication ---
def get_prompt_variations(user_idea: str):
    """Calls the backend to get a list of prompt variations."""
    try:
        response = requests.post(
            f"{API_BASE_URL}/agent/variations", json={"prompt": user_idea}
        )
        response.raise_for_status()
        return response.json().get("variations", [])
    except requests.RequestException as e:
        st.error(f"Error getting prompt variations: {e}")
        return None


def generate_image(prompt: str):
    """Calls the backend to generate an image from a single prompt."""
    try:
        response = requests.post(
            f"{API_BASE_URL}/agent/generate", json={"prompt": prompt}
        )
        response.raise_for_status()
        # Expecting a JSON with 'image_base64' and 'final_prompt'
        return response.json()
    except requests.RequestException as e:
        st.error(f"Error generating image: {e}")
        return None


# --- UI Layout ---
st.title("🎨 AI Design Agent")
st.markdown(
    "Your collaborative partner for visual creation. Start with a simple idea, and the agent will brainstorm and generate multiple visual concepts for you to refine."
)

# Use session state to hold the results
if "results" not in st.session_state:
    st.session_state.results = []

# --- Main Interaction ---
with st.form("idea_form"):
    user_idea = st.text_input(
        "Enter a simple idea or concept:",
        placeholder="e.g., A cat wearing a wizard hat",
        key="user_idea_input",
    )
    submitted = st.form_submit_button("✨ Generate Concepts")

if submitted and user_idea:
    st.session_state.results = []  # Clear previous results
    # 1. Get prompt variations from the "Creative Director" agent
    with st.spinner(
        "Step 1: The Creative Director is brainstorming prompt variations..."
    ):
        variations = get_prompt_variations(user_idea)

    if variations:
        st.info(
            f"Brainstorming complete! Generating {len(variations)} unique concepts..."
        )
        # 2. Generate an image for each variation
        placeholders = {}
        cols = st.columns(len(variations))

        for i, prompt_variation in enumerate(variations):
            placeholders[i] = cols[i].empty()
            with placeholders[i]:
                with st.spinner(f"Concept {i+1}: The Artist is painting..."):
                    result_data = generate_image(prompt_variation)
                    if result_data and result_data.get("image_base64"):
                        st.session_state.results.append(result_data)

# --- Display Results Gallery ---
if st.session_state.results:
    st.markdown("---")
    st.subheader("Generated Concepts")

    num_results = len(st.session_state.results)
    cols = st.columns(num_results)

    for i, result in enumerate(st.session_state.results):
        with cols[i]:
            image_b64 = result.get("image_base64")
            final_prompt = result.get("final_prompt", "Prompt not available.")

            try:
                img_data = base64.b64decode(image_b64)
                img = Image.open(io.BytesIO(img_data))
                st.image(img, use_column_width=True)

                # Use textwrap for cleaner prompt display
                wrapped_prompt = textwrap.fill(final_prompt, width=40)
                st.caption(f"**Prompt:** {wrapped_prompt}")

            except Exception as e:
                st.error(f"Could not display image {i+1}. Error: {e}")
