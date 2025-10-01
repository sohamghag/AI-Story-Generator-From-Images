import streamlit as st
from PIL import Image
from story_generator import generate_story_from_images, generate_audio_from_story
from io import BytesIO

st.set_page_config(page_title="AI Story Generator", layout="wide")  # Full width page

# ----- HEADER -----
st.markdown("<h1 style='text-align:center; color:fff;'>AI Story Generator From Images</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Upload 1-10 images, choose a style, and let the AI create and narrate your tale!</p>", unsafe_allow_html=True)
st.markdown("---")


# ----- SIDEBAR STYLE -----
with st.sidebar:
    st.markdown("## Controls")
    story_images = st.file_uploader("Upload Images...", type=["jpg", "png", "jpeg"], accept_multiple_files=True)
    story_style = st.selectbox("Choose Story Style",
                               ["Comedy", "Thriller", "Fairy Tale", "Sci-Fi", "Mystery", "Adventure", "Moral"])
    generate_button = st.button("Generate Story & Narration", type="primary")


if generate_button:
        if not story_images:
            st.warning("Please Upload Atleast 1 Image.")
        elif len(story_images) > 10:
            st.warning("Please Upload a Maximum 10 Images.")
        else:
            with st.spinner("Generating Story & Narration..."):
                try:
                    images_list = [Image.open(image) for image in story_images]
                    st.subheader("Your visual Inspiration")
                    image_columns = st.columns(len(images_list))

                    for i, image in enumerate(images_list):
                        with image_columns[i]:
                            st.image(image, use_container_width=True)

                    story = generate_story_from_images(images_list, story_style)
                    if story:
                        st.subheader("Your Story")
                        st.markdown(f"<h5 style='color:gray'>{story}</h5 >", unsafe_allow_html=True)

                    with st.spinner("Generating Audio..."):
                        audio = generate_audio_from_story(story)
                        if audio:
                            st.subheader("Listen Your Story")
                            st.audio(audio, format='audio/mp3')



                except Exception as e:
                    st.error(f"Something went wrong. {e}")


