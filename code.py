# Install required libraries
!pip install googletrans==4.0.0-rc1
!pip install ipywidgets
!pip install gtts
!pip install pygame

# Import libraries
from googletrans import Translator, LANGUAGES
from gtts import gTTS
import ipywidgets as widgets
from IPython.display import display, Audio, clear_output
import pygame
import io
import os

# Initialize translator
translator = Translator()

# Create a mapping between language names and codes
language_mapping = {name: code for code, name in LANGUAGES.items()}
language_names = list(LANGUAGES.values())

def translate_text(text, src_lang, dest_lang):
    """
    Translate text from source language to destination language
    """
    try:
        translation = translator.translate(text, src=src_lang, dest=dest_lang)
        return translation.text
    except Exception as e:
        return f"Error in translation: {str(e)}"

def text_to_speech(text, lang):
    """
    Convert text to speech and play it
    """
    try:
        tts = gTTS(text=text, lang=lang, slow=False)
        # Save to a bytes buffer
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        
        # Play audio
        return Audio(fp.read(), autoplay=True)
    except Exception as e:
        print(f"Error in text-to-speech: {str(e)}")
        return None

# Create widgets
text_input = widgets.Textarea(
    value='',
    placeholder='Enter text to translate',
    description='Input:',
    disabled=False,
    layout=widgets.Layout(width='90%', height='100px')
)

# Language dropdowns - using the language names directly
src_lang_dropdown = widgets.Dropdown(
    options=language_names,
    value='english',
    description='From:',
    layout=widgets.Layout(width='45%')
)

dest_lang_dropdown = widgets.Dropdown(
    options=language_names,
    value='spanish',
    description='To:',
    layout=widgets.Layout(width='45%')
)

# Buttons
translate_button = widgets.Button(
    description='Translate',
    button_style='success',
    layout=widgets.Layout(width='150px')
)

copy_button = widgets.Button(
    description='Copy Text',
    button_style='info',
    layout=widgets.Layout(width='150px')
)

speak_button = widgets.Button(
    description='Speak Translation',
    button_style='warning',
    layout=widgets.Layout(width='150px')
)

# Output area
output = widgets.Output(layout={'border': '1px solid black'})

# Event handlers
def on_translate_button_clicked(b):
    with output:
        clear_output()
        text = text_input.value
        if not text.strip():
            print("Please enter some text to translate.")
            return
            
        # Get language codes using our mapping
        src_lang_code = language_mapping[src_lang_dropdown.value.lower()]
        dest_lang_code = language_mapping[dest_lang_dropdown.value.lower()]
        
        # Translate
        translated_text = translate_text(text, src_lang_code, dest_lang_code)
        print(f"Translated text:\n{translated_text}")
        
        # Store the translated text for copy/speak functions
        global current_translation
        current_translation = translated_text

def on_copy_button_clicked(b):
    try:
        # Copy to clipboard (works in Colab)
        import google.colab
        google.colab.kernel.invokeJavaScript(f'navigator.clipboard.writeText("{current_translation}")')
        with output:
            print("Text copied to clipboard!")
    except:
        with output:
            print("Clipboard access not available in this environment.")

def on_speak_button_clicked(b):
    with output:
        clear_output()
        if 'current_translation' not in globals():
            print("Please translate some text first.")
            return
            
        # Get language code for TTS
        dest_lang_code = language_mapping[dest_lang_dropdown.value.lower()]
        
        # Play audio
        audio = text_to_speech(current_translation, dest_lang_code)
        if audio:
            display(audio)
            print("Playing audio...")
        else:
            print("Could not generate audio.")

# Attach event handlers
translate_button.on_click(on_translate_button_clicked)
copy_button.on_click(on_copy_button_clicked)
speak_button.on_click(on_speak_button_clicked)

# Display the UI
print("Language Translation Tool")
display(text_input)
display(widgets.HBox([src_lang_dropdown, dest_lang_dropdown]))
display(widgets.HBox([translate_button, copy_button, speak_button]))
display(output)
