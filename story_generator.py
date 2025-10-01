import os
from io import BytesIO

from google import genai
from dotenv import load_dotenv
from gtts import gTTS
from google.genai import types
load_dotenv()
api_key = os.getenv('GOOGLE_API_KEY')

if not api_key:
    raise ValueError('API_KEY environment variable is not set')

client = genai.Client(api_key=api_key)


# get images --> display images --> feed image to gemini with prompt --> get story --> narration

def prompt(style: str) -> str:
    story = """
Write a short story in exactly 5 paragraphs. 
The story must follow a clear beginning, middle, and end with engaging characters, 
a central conflict, and a resolution.

The style, tone, and narrative voice must strictly match the one I provide. 
Maintain this style consistently in all five paragraphs. 

At the end of the story, provide a moral/lesson, but it must also be expressed 
in the same style and tone. The moral should feel naturally connected to the story 
rather than separate.
    """

    style_instruction = f"\nStyle to use: {style}.\n"

    return story + style_instruction

def generate_story_from_images(images,style):
    if not 1<=len(images)<=100:
        raise ValueError('Number of images should be between 1 and 100')
    else:
        response = client.models.generate_content(model="gemini-2.5-pro", contents=[images,prompt(style)])
        return response.text

def generate_audio_from_story(story):
    try:
        if not story:
            raise ValueError('No story provided')
        else:
            tts = gTTS(text=story, lang='en',slow=False)
            audio_fp = BytesIO()
            tts.write_to_fp(audio_fp)
            audio_fp.seek(0)
            return audio_fp
    except Exception as e:
        print(e)





