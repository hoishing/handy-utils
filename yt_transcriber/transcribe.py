import streamlit as st
from google.genai import Client, types
from io import BytesIO
from pytubefix import Buffer, YouTube


def download_yt_audio(yt: YouTube) -> tuple[Buffer, str]:
    """download the lowest quality audio stream to a pytubefix Buffer object"""
    audio_stream = (
        yt.streams.filter(only_audio=True, audio_codec="opus").order_by("abr").first()
    )
    buffer = Buffer()
    buffer.download_in_buffer(audio_stream)
    mime_type = audio_stream.mime_type
    return buffer, mime_type


def get_audio_part(mime_type: str, buffer: Buffer) -> types.Part:
    """convert the pytubefix Buffer object to a Gemini types.Part object"""
    return types.Part.from_bytes(data=buffer.read(), mime_type=mime_type)


def remove_duplicate_gemini_audio(name: str, client: Client):
    """adding audio with the same name to Gemini cloud storage will raise an error, so remove the existing one"""
    audio_files = [f.name for f in client.files.list()]
    for file_name in audio_files:
        if name in file_name:
            client.files.delete(name=file_name)


def upload_gemini_audio(
    name: str, buffer: Buffer, mime_type: str, client: Client
) -> types.File:
    """upload the audio to Gemini cloud storage"""
    io_obj: BytesIO = buffer.buffer
    io_obj.seek(0)
    upload_config = types.UploadFileConfig(mime_type=mime_type, name=name)
    remove_duplicate_gemini_audio(name, client)
    return client.files.upload(file=io_obj, config=upload_config)


def transcribe(
    audio: types.File | types.Part,
    client: Client,
    model: str = "gemini-2.0-flash",
    system_prompt: str = "You are a professional transcriber. You output only transcript, no other text.",
    user_prompt: str = "Generate a transcript of the speech",
) -> str:
    """transcribe the audio using Gemini"""
    response = client.models.generate_content(
        model=model,
        config=types.GenerateContentConfig(system_instruction=system_prompt),
        contents=[user_prompt, audio],
    )
    return response.text


def transcribe_ui(yt: YouTube, api_key: str) -> str:
    """Streamlit UI for transcribing audio"""
    st.markdown("#### 🗣️ &nbsp; Transcribe Audio")
    with st.spinner("No captions found, transcribing audio with Gemini..."):
        client = Client(api_key=api_key)
        filename = yt.video_id.lower()
        buffer, mime_type = download_yt_audio(yt)
        audio_file = upload_gemini_audio(filename, buffer, mime_type, client)

        transcript = transcribe(audio_file, client)
        st.text_area(label="Transcript", value=transcript, height=400)
