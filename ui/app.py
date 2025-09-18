import streamlit as st
import requests
import base64
from PIL import Image
import io
import textwrap
import os

# --- Configuration ---
API_BASE_URL = os.getenv("API_BASE_URL", "http://api:8000")
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
        return []


def generate_image(prompt: str):
    """Calls the backend to generate an image from a single prompt."""
    try:
        response = requests.post(
            f"{API_BASE_URL}/agent/generate", json={"prompt": prompt}
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"Error generating image: {e}")
        return None


# --- UI Layout ---
st.title("🎨 AI Design Agent")
st.markdown(
    "Your collaborative partner for visual creation. Start with a simple idea, "
    "and the agent will brainstorm and generate multiple visual concepts for you to refine."
)

# Session state for storing results
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

    # Step 1: Get prompt variations
    with st.spinner("Step 1: Brainstorming prompt variations..."):
        variations = get_prompt_variations(user_idea)

    if not variations:
        st.warning("No variations received from the backend.")
    else:
        st.info(f"Generating {len(variations)} unique concepts...")

        # Step 2: Generate images with live display
        max_cols = 3
        total_variations = len(variations)
        progress_bar = st.progress(0)
        generated_count = 0

        # Placeholder container for results
        results_container = st.container()

        for i in range(0, total_variations, max_cols):
            chunk = variations[i : i + max_cols]
            cols = results_container.columns(len(chunk))

            for j, prompt_variation in enumerate(chunk):
                with cols[j]:
                    placeholder = st.empty()  # Individual placeholder for live update
                    with st.spinner(f"Concept {i+j+1}: Generating..."):
                        result_data = generate_image(prompt_variation)
                        if result_data and result_data.get("image_base64"):
                            st.session_state.results.append(result_data)

                            # Decode and display image immediately
                            try:
                                img_data = base64.b64decode(result_data["image_base64"])
                                img = Image.open(io.BytesIO(img_data))
                                placeholder.image(img, use_container_width=True)
                                wrapped_prompt = textwrap.fill(
                                    result_data.get(
                                        "final_prompt", "Prompt not available."
                                    ),
                                    width=40,
                                )
                                placeholder.caption(f"**Prompt:** {wrapped_prompt}")
                            except Exception as e:
                                placeholder.error(
                                    f"Could not display image. Error: {e}"
                                )
                        else:
                            placeholder.warning(
                                f"Concept {i+j+1} could not be generated."
                            )

                        # Update progress bar
                        generated_count += 1
                        progress_bar.progress(generated_count / total_variations)
