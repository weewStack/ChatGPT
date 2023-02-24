import openai
import speech_recognition as sr
import time
import threading
import pyttsx3
#The following are used to import the apiKey from env variable
from env import getkey
import os

getkey()
#Replace this code using you own key
openai.api_key = os.environ.get('CHAT_GPT_API_KEY')


global AIreply, final_msg
AIreply = False
final_msg = ""

#3- Initiation of the text to vocal engine and Setting up preference
engine = pyttsx3.init()
voices = engine.getProperty('voices')
# changing index, changes voices. 1 for female
engine.setProperty('voice', voices[1].id)
rate = engine.getProperty('rate')   # getting details of current speaking rate
engine.setProperty('rate',160)     # setting up new voice rate

#2-Set the apikey & Sending request to chat GPS
def generate_response(prompt):

    global AIreply, final_msg
    completions = openai.Completion.create(
        engine="text-davinci-003",#"text-davinci-003"#"text-babbage-001"
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    message = completions.choices[0].text
    final_msg = message.strip()
    AIreply = True


def chatprinter(chat):
    for word in chat:
        time.sleep(0.055)
        print(word,end= "", flush=True)
    print()


# 1- Setup the speach recogintion and prepare the main loop
r = sr.Recognizer()
with sr.Microphone() as source:
    print("-----------------------Chat is ready-----------------------")
    while True:
        print("Me:",end=" ", flush=True)
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio, show_all=True)
            TextResult = text['alternative'][0]['transcript']
            if "stop" in TextResult:
                print("ENDING CHAT COMMUNICATION")
                break

            t1 = threading.Thread(target=generate_response, args=(TextResult,))
            t1.start()

            chatprinter(TextResult)   
            
            while AIreply == False:
                pass
            AIreply = False
            
            print("ChatGPT: ", end="")
            t2 = threading.Thread(target=chatprinter, args=(final_msg,))
            t2.start()
            
            # Start reading the text received from GPT
            engine.say(final_msg)
            engine.runAndWait()
            print("--------------------------------------------")
        except:
            print("Sorry could not recognize your voice")
