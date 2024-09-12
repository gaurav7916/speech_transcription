import os
import assemblyai as aai
from dotenv import load_dotenv, find_dotenv
import streamlit as st

st.title("AI Assistant")
st.markdown("This AI Assistant will transcribe your speech in real-time.")

class AI_Assistant:
    def __init__(self):
        load_dotenv(find_dotenv())
        aai.settings.api_key = os.getenv("9c8e0dd36b64455384fe19951cf0dc71")
        
        self.transcriber = None

    def start_transcription(self):
        self.transcriber = aai.RealtimeTranscriber(
            sample_rate=16000,
            on_data=self.on_data,
            on_error=self.on_error,
            on_open=self.on_open,
            on_close=self.on_close,
            end_utterance_silence_threshold=1000
        )
        self.transcriber.connect()
        microphone_stream = aai.extras.MicrophoneStream(sample_rate=16000)
        self.transcriber.stream(microphone_stream)
    
    def stop_transcription(self):
        if self.transcriber:
            self.transcriber.close()
            self.transcriber = None
    
    def on_open(self, session_opened: aai.RealtimeSessionOpened):
        # Optional: print("Session ID:", session_opened.session_id)
        pass

    def on_data(self, transcript: aai.RealtimeTranscript):
        if not transcript.text:
            return
        if isinstance(transcript, aai.RealtimeFinalTranscript):
            # Ensure only final transcripts are processed and displayed
            print(transcript.text)  # Output to console
            st.write(transcript.text)  # Display in Streamlit

    def on_error(self, error: aai.RealtimeError):
        print("An error occurred:", error)

    def on_close(self):
        print("Transcription session closed.")

# Initialize and start transcription
ai_assistant = AI_Assistant()
ai_assistant.start_transcription()
