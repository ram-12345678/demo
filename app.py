import streamlit as st
from transformers import AutoProcessor, SeamlessM4Tv2Model
import torchaudio
from IPython.display import Audio

st.title("SeamlessM4T Translation Demo")

# Load the processor and model
processor = AutoProcessor.from_pretrained("facebook/seamless-m4t-v2-large")
model = SeamlessM4Tv2Model.from_pretrained("facebook/seamless-m4t-v2-large")

# Speech-to-Speech (S2ST) Translation
st.header("Speech-to-Speech (S2ST) Translation")

text_input_s2st = st.text_input("Enter text for S2ST translation:", "Hello, my dog is cute")

if st.button("Translate S2ST"):
    text_inputs_s2st = processor(text=text_input_s2st, src_lang="eng", return_tensors="pt")
    audio_array_s2st = model.generate(**text_inputs_s2st, tgt_lang="rus")[0].cpu().numpy().squeeze()
    st.audio(audio_array_s2st, format="wav", label="Translated Audio (S2ST)")

# Speech-to-Text (S2TT) Translation
st.header("Speech-to-Text (S2TT) Translation")

file_input_s2tt = st.file_uploader("Upload an audio file for S2TT translation:", type=["wav"])

if file_input_s2tt is not None:
    audio_s2tt, orig_freq_s2tt = torchaudio.load(file_input_s2tt)
    audio_s2tt = torchaudio.functional.resample(audio_s2tt, orig_freq=orig_freq_s2tt, new_freq=16_000)

    if st.button("Translate S2TT"):
        audio_inputs_s2tt = processor(audios=audio_s2tt, return_tensors="pt")
        text_output_s2tt = model.generate(**audio_inputs_s2tt, tgt_lang="rus")[0]
        st.write("Translated Text (S2TT):", text_output_s2tt)

# Text-to-Speech (T2ST) Translation
st.header("Text-to-Speech (T2ST) Translation")

text_input_t2st = st.text_input("Enter text for T2ST translation:", "मेरा कुत्ता बहुत प्यारा है")

if st.button("Translate T2ST"):
    audio_array_t2st = model.generate(text_input_t2st, src_lang="hin", tgt_lang="eng")[0].cpu().numpy().squeeze()
    st.audio(audio_array_t2st, format="wav", label="Translated Audio (T2ST)")
