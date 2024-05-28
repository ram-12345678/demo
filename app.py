import streamlit as st
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import os


def speech_to_text(language):
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        st.write(f"Listening...")

        try:
            audio = recognizer.listen(source)
            text = recognizer.recognize_google(audio, language=language)
            return text
        except sr.UnknownValueError:
            return "Sorry, I couldn't understand what you said."
        except sr.RequestError:
            return "Sorry, unable to access Google Speech Recognition service."


def translate_text(text, dest_lang):
    translator = Translator()
    translation = translator.translate(text, dest=dest_lang)
    return translation.text


def text_to_speech(text, lang):
    tts = gTTS(text=text, lang=lang)
    filename = "output.mp3"
    tts.save(filename)
    return filename


lang_codes = {
    'af': 'afrikaans', 'sq': 'albanian', 'am': 'amharic', 'ar': 'arabic',
    'hy': 'armenian', 'az': 'azerbaijani', 'eu': 'basque', 'be': 'belarusian',
    'bn': 'bengali', 'bs': 'bosnian', 'bg': 'bulgarian', 'ca': 'catalan',
    'ceb': 'cebuano', 'ny': 'chichewa', 'zh-cn': 'chinese (simplified)',
    'zh-tw': 'chinese (traditional)', 'co': 'corsican', 'hr': 'croatian',
    'cs': 'czech', 'da': 'danish', 'nl': 'dutch', 'en': 'english',
    'eo': 'esperanto', 'et': 'estonian', 'tl': 'filipino', 'fi': 'finnish',
    'fr': 'french', 'fy': 'frisian', 'gl': 'galician', 'ka': 'georgian',
    'de': 'german', 'el': 'greek', 'gu': 'gujarati', 'ht': 'haitian creole',
    'ha': 'hausa', 'haw': 'hawaiian', 'he': 'hebrew', 'hi': 'hindi',
    'hmn': 'hmong', 'hu': 'hungarian', 'is': 'icelandic', 'ig': 'igbo',
    'id': 'indonesian', 'ga': 'irish', 'it': 'italian', 'ja': 'japanese',
    'jw': 'javanese', 'kn': 'kannada', 'kk': 'kazakh', 'km': 'khmer',
    'ko': 'korean', 'ku': 'kurdish (kurmanji)', 'ky': 'kyrgyz', 'lo': 'lao',
    'la': 'latin', 'lv': 'latvian', 'lt': 'lithuanian', 'lb': 'luxembourgish',
    'mk': 'macedonian', 'mg': 'malagasy', 'ms': 'malay', 'ml': 'malayalam',
    'mt': 'maltese', 'mi': 'maori', 'mr': 'marathi', 'mn': 'mongolian',
    'my': 'myanmar (burmese)', 'ne': 'nepali', 'no': 'norwegian', 'or': 'odia',
    'ps': 'pashto', 'fa': 'persian', 'pl': 'polish', 'pt': 'portuguese',
    'pa': 'punjabi', 'ro': 'romanian', 'ru': 'russian', 'sm': 'samoan',
    'gd': 'scots gaelic', 'sr': 'serbian', 'st': 'sesotho', 'sn': 'shona',
    'sd': 'sindhi', 'si': 'sinhala', 'sk': 'slovak', 'sl': 'slovenian',
    'so': 'somali', 'es': 'spanish', 'su': 'sundanese', 'sw': 'swahili',
    'sv': 'swedish', 'tg': 'tajik', 'ta': 'tamil', 'te': 'telugu', 'th': 'thai',
    'tr': 'turkish', 'uk': 'ukrainian', 'ur': 'urdu', 'ug': 'uyghur', 'uz': 'uzbek',
    'vi': 'vietnamese', 'cy': 'welsh', 'xh': 'xhosa', 'yi': 'yiddish',
    'yo': 'yoruba', 'zu': 'zulu'
}

st.title('Speech to Speech Translation')

input_language = st.selectbox('Select Input Language', list(lang_codes.values()))
output_language = st.selectbox('Select Target Language', list(lang_codes.values()))

if st.button('Translate'):
    input_text = speech_to_text(input_language)

    if input_text:
        translated_text = translate_text(input_text, output_language)
        output_filename = text_to_speech(translated_text, output_language)
        st.audio(output_filename, format='audio/mp3')

