#from AppOpener import close, open as appopen(for windows)
from selenium import webdriver
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
from webbrowser import open as webopen
from pywhatkit import search, playonyt
from dotenv import dotenv_values
from bs4 import BeautifulSoup
from rich import print
from groq import Groq
import webbrowser
import subprocess
import requests
import asyncio
import os

env_vars = dotenv_values(".env")
GroqAPIkey = env_vars.get("GroqAPIKey")

classes = ['zCubwf', 'hgKElc', 'LTKZOO sY7ric', 'gsrt vk_b FzvWSb YwPhnf', 'pclqee', 'tw-Data-text tw-text-small tw-ta',
           'IZ6rdc', 'O5uR6d LTKOO', 'vlzY6d', 'webanswers-webanswers_table__webanswers-table', 'dDoNo ikb48b gsrt', 'sXLaOe',
           'LWkfKe', 'VQF4g', 'qv3Wpe', 'kno-rdesc', 'SPZz6b']

useragent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.142.86 Safari/537.36'
client = Groq(api_key=GroqAPIkey)

professional_responses = [
    "Your satisfaction is my top priority sir; feel free to summon me if there is anything I could help you with.",
    "I'm at your service for any additional assistance or support you may need-don't hesitate to ask."
]

messages = []

SystemChatBot = [{"role": "system", "content": f"Hello, I am {env_vars.get('Username')} your owner, You're a content writer. You have to write content like letter, articles, essays, research papers etc."}]

def GoogleSearch(Topic):
    search(Topic)
    return True

def Content(Topic):

    def OpenNotepad(File):
        subprocess.run(["open", "-a", "TextEdit", File])

    def ContentWriterAI(prompt):
        messages.append({"role": "system", "content": f"{prompt}"})

        completion = client.chat.completions.create(
            model="moonshotai/kimi-k2-instruct",
            messages=SystemChatBot + messages,
            max_tokens=2048,
            temperature=0.7,
            top_p=1,
            stream=True,
            stop=None
        )

        Answer = ""

        for chunk in completion:
            if chunk.choices[0].delta.content:
                Answer += chunk.choices[0].delta.content

        Answer = Answer.replace("</s>", "")
        messages.append({"role": "assistant", "content": Answer})
        return Answer

    Topic = Topic.replace("Content", "").strip()
    ContentByAI = ContentWriterAI(Topic)

    os.makedirs("Data", exist_ok=True)
    with open(f"Data/{Topic.lower().replace(' ', '')}.txt", "w", encoding="utf-8") as file:
        file.write(ContentByAI)

    OpenNotepad(f"Data/{Topic.lower().replace(' ', '')}.txt")
    return True

def YoutubeSearch(Topic):
    Url4Search = f"https://www.youtube.com/results?search_query={Topic}"
    webbrowser.open(Url4Search)
    return True

def PlayYoutube(query):
    playonyt(query)
    return True

''' windows
def OpenApp(app, sess=requests.session()):
    try:
        appopen(app, match_closest=True, output=True, throw_error=True)
        return True
    except:
        def extract_links(html):
            if html is None:
                return []
            soup = BeautifulSoup(html, 'html.parser')
            links = soup.find_all('a', {'jsname': 'UWckNb'})
            return [link.get('href') for link in links]
        
        def search_google(query):
            url = f"https://www.google.com/search?q={query}"
            headers = {"User-Agent": useragent}
            response = sess.get(url, headers=headers)

            if response.status_code == 200:
                return response.text
            else:
                print("Failed to retrieve search results")
            return None

        html = search_google(app)

        if html:
            link = extract_links(html)[0]
            webopen(link)

        return True
'''

def OpenApp(app, sess=requests.session()):
    try:
        # Attempt to open the app directly using macOS's open command
        subprocess.run(["open", f"-a", app], check=True)
        return True
    except subprocess.CalledProcessError:
        # If the app is not found, perform a web search
        print(f"App '{app}' not found locally. Online search feature will be introduced later...")

def CloseApp(app):
    if "chrome" in app:
        pass
    else:
        try:
            subprocess.run(["osascript", "-e", f'tell application "{app}" to quit'], check=True)
            return True
        except subprocess.CalledProcessError:
            print(f"Failed to close {app}. It may not be running.")
            return False

def System(command):
    def mute():
        subprocess.run(["osascript", "-e", "set volume output muted true"])

    def unmute():
        subprocess.run(["osascript", "-e", "set volume output muted false"])

    def volume_up():
        subprocess.run(["osascript", "-e", "set volume output volume (output volume of (get volume settings) + 10)"])

    def volume_down():
        subprocess.run(["osascript", "-e", "set volume output volume (output volume of (get volume settings) - 10)"])


    if command == "mute":
        mute()
    elif command == "unmute":
        unmute()
    elif command == "volume up":
        volume_up()
    elif command == "volume down":
        volume_down()

    return True

def command_splitter(raw: str) -> list[str]:
    words = raw.split()
    cmds = []
    current = []

    keywords = ["open", "close", "play", "content", "google", "youtube", "system"]

    for word in words:
        if word in keywords:
            if current:
                cmds.append(" ".join(current))
                current = []
        current.append(word)

    if current:
        cmds.append(" ".join(current))

    return cmds


async def TranslateAndExecute(commands: list[str]):

    funcs = []
    for command in commands:
        if command.startswith("open "):
            fun = asyncio.to_thread(OpenApp, command.removeprefix("open "))
            funcs.append(fun)
        elif command.startswith("close "):
            fun = asyncio.to_thread(CloseApp, command.removeprefix("close "))
            funcs.append(fun)
        elif command.startswith("play "):
            fun = asyncio.to_thread(PlayYoutube, command.removeprefix("play "))
            funcs.append(fun)
        elif command.startswith("content "):
            fun = asyncio.to_thread(Content, command.removeprefix("content "))
            funcs.append(fun)
        elif command.startswith("google search "):
            fun = asyncio.to_thread(GoogleSearch, command.removeprefix("google search "))
            funcs.append(fun)
        elif command.startswith("youtube search "):
            fun = asyncio.to_thread(YoutubeSearch, command.removeprefix("youtube search "))
            funcs.append(fun)
        elif command.startswith("system "):
            fun = asyncio.to_thread(System, command.removeprefix("system "))
            funcs.append(fun)
        else:
            print(f"No Function found. For {command}")

    results = await asyncio.gather(*funcs)
    for result in results:
        yield result

async def Automation(commands: list[str]):
    async for result in TranslateAndExecute(commands):
        pass

    return True


if __name__ == "__main__":
    commands = [
        "open finder"
    ]

    asyncio.run(Automation(commands))


