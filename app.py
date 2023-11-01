import time
import gradio as gr
import config as cfg
import openai
import speech_recognition as sr
from gtts import gTTS


openai.api_key = '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'
r = sr.Recognizer()

def transcribe_file(speech_file: str):
    """Transcribe the audio file."""
    text = ""
    with sr.AudioFile(speech_file) as audio_file:
        content = r.record(audio_file)
    
    text +=r.recognize_google(content)

    return text

def add_user_input(history, text):
    """Add user input to chat hostory."""
    history = history + [(text, None)]
    return history, gr.update(value="", interactive=False)

def speak():
    text = res[-1]
    myobj = gTTS(text=text, lang='en', slow=False) 
    myobj.save("test.wav") 
    return 'test.wav'

messages=[
        {"role": "system", "content": "You are a Question/Answer assistant. Your name is Amena."},
    ]

res = ["Hi, I'm your AI Chatbot Amena. How may I help you today?"]

def bot_response(history):
    """Returns updated chat history with the Bot response."""
    messages.append({"role": "user", "content": history[-1][0]})
    response = openai.ChatCompletion.create( model="gpt-3.5-turbo", messages = messages)
    # Intergate with ML models to load response.
    response = response['choices'][0]['message']['content']
    history[-1][1] = response
    res.append(response)
    time.sleep(2)
    return history

with gr.Blocks() as bot_interface:
    with gr.Row():
        gr.HTML(cfg.bot["banner"])
    with gr.Row():
        chatbot=gr.Chatbot([(cfg.bot["initial_message"], None)], elem_id="chatbot",Bubbles).style(height=500)
    with gr.Row():
        with gr.Column(scale=12):
            user_input = gr.Textbox(
                show_label=False, placeholder=cfg.bot["text_placeholder"],
            ).style(container=False)
        with gr.Column(min_width=70, scale=1):
            submitBtn = gr.Button("Send")
    with gr.Row():
        audio_input=gr.Audio(source="microphone", type="filepath")
    with gr.Row():
        output = gr.Audio(speak,visible=True,autoplay=True)
        speakBtn = gr.Button("Speak")


    
    input_msg = user_input.submit(add_user_input, [chatbot, user_input], [chatbot, user_input], queue=False).then(bot_response, chatbot, chatbot)
    submitBtn.click(add_user_input, [chatbot, user_input], [chatbot, user_input], queue=False).then(bot_response, chatbot, chatbot)
    input_msg.then(lambda: gr.update(interactive=True), None, [user_input], queue=False)
    inputs_event = audio_input.stop_recording(transcribe_file, audio_input, user_input).then(add_user_input, [chatbot, user_input], [chatbot, user_input], queue=False).then(bot_response, chatbot, chatbot)
    inputs_event.then(lambda: gr.update(interactive=False), None, [user_input], queue=False)
    speakBtn.click(fn = speak,outputs=output)
bot_interface.title = cfg.bot["title"]
bot_interface.launch(share=False)
 
