import speech_recognition as sr
import os
import win32com.client
import webbrowser
import openai
import datetime
from config import apikey
import random

chatStr=""
def chat(query):
    global chatStr
    print(chatStr)
    openai.api_key = apikey
    chatStr += f"Shishir: {query}\n Jarvis: "
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=chatStr,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    #speaker = win32com.client.Dispatch("SAPI.SpVoice")
    speaker.Speak(response["choices"][0]["text"])
    chatStr += f"{response['choices'][0]['text']}\n"
    return response["choices"][0]["text"]







def ai(prompt):
    openai.api_key = apikey
    text = f"OpenAI response for Prompt: {prompt} \n *************************\n\n"
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    print(response["choices"][0]["text"])
    text += response["choices"][0]["text"]

    if not os.path.exists("Openai"):
        os.mkdir("Openai")
        #with open(f"Openai/prompt- {random.randint(1,23456789)}", "w") as f:
        with open(f"Openai/{prompt[0:30]}.txt","w") as f:
            f.write(text)

def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        # r.pause_threshold =1
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"user said: {query}")
            return query
        except Exception as e:
            return "Some error occured. Sorry from Jarvis"


speaker = win32com.client.Dispatch("SAPI.SpVoice")
speaker.Speak("Hello I am Jarvis AI")
while True:
    print("Listening...")
    query = takecommand()
    #speaker.Speak(query)
    sites = [["youtube", "https://www.youtube.com"], ["google", "https://www.google.com"],
             ["wikipedia", "https://www.wikipedia.com"]]
    for site in sites:
        if f"Open {site[0]}".lower() in query.lower():
            speaker.Speak(f"Opening {site[0]} sir...")
            webbrowser.open(site[1])

        elif "the time".lower() in query.lower():
            strfTime = datetime.datetime.now().strftime("%H:%M:%S")
            speaker.Speak(f"Sir the time is {strfTime}")

        elif"using artificial intelligence".lower() in query.lower():
            ai(prompt=query)
        elif "Jarvis Quit".lower() in query.lower():
            exit()
        elif "reset chat".lower() in query.lower():
            chatStr=""

        else:
            print("chatting...")
            chat(query)
