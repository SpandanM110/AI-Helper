import assemblyai as aai

import openai
import elevenlabs
from queue import Queue


aai.settings.api_key = "e68bafe98cf44d6aa5a3a49f2834e158"
openai.api_key = "YOUR_API_KEY"
elevenlabs.set_api_key("3cea1ecd88fa5d66b516d241069fed27")




transcript_queue = Queue()
def on_data(transcript: aai.RealtimeTranscript):
    if not transcript.text:
        return
    if isinstance(transcript, aai.RealtimeFinalTranscript):
        transcript_queue.put(transcript.text + '')
        print("User said: ", transcript.text, end="\r\n")
    else:
        print(transcript.text, end="\r")

def on_error(error: aai.RealtimeError):
    print("An Error occured:", error )


def handle_conversation():
    while True:
        transcriber  =aai.RealtimeTranscriber(
            on_data=on_data,
            on_error=on_error,
            sample_rate=44_100,
        )

        transcriber.connect()

        microphone_stream = aai.extras.MicrophoneStream()

        transcriber.stream(microphone_stream)

        transcriber.close()

        transcript_result = transcript_queue.get()

        response = openai.ChatCompletion.create(
            model = 'gpt-4',
            messages = [
                {"role": "system", "content": 'You are a highly skilled AI, answer the questions given within a maximum of 1000 characters.'},
                {"role": "user", "content": transcript_result}
            ]
        )

        text = response['choices'][0]['message']['content']
       
        # Convert the response to audio and play it
        audio = elevenlabs.generate(
            text=text,
            voice="Daniel" # or any voice of your choice
        )

        print("\nAI:", text, end="\r\n")

        elevenlabs.play(audio)

handle_conversation()




