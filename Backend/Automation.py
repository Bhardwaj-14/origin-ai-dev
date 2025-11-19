import os
import time
import webbrowser
import subprocess
import requests
import asyncio
from concurrent.futures import ThreadPoolExecutor

from AppOpener import open as appopen, close as appclose
from pywhatkit import search, playonyt
from dotenv import dotenv_values
from bs4 import BeautifulSoup
from groq import Groq

# ------------------ ENV + CLIENT ------------------ #

env_vars = dotenv_values(".env")
GroqAPIkey = env_vars.get("GroqAPIKey")

client = Groq(api_key=GroqAPIkey)

messages = []
SystemChatBot = [
    {
        "role": "system",
        "content": f"Hello, I am {env_vars.get('Username')}. You write content like letters, essays, research papers, etc."
    }
]

useragent = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    " AppleWebKit/537.36 (KHTML, like Gecko)"
    " Chrome/124.0.0.0 Safari/537.36"
)

executor = ThreadPoolExecutor(max_workers=10)

# ------------------ CORE FUNCTIONS ------------------ #

def GoogleSearch(topic):
    search(topic)
    return True

def YoutubeSearch(topic):
    url = f"https://www.youtube.com/results?search_query={topic}"
    webbrowser.open(url)
    return True

def PlayYoutube(query):
    playonyt(query)
    return True

# ---------- Content Writer (Groq AI) ---------- #

def ContentWriter(prompt):
    messages.append({"role": "system", "content": prompt})

    completion = client.chat.completions.create(
        model="moonshotai/kimi-k2-instruct",
        messages=SystemChatBot + messages,
        max_tokens=2048,
        temperature=0.7,
        stream=True
    )

    answer = ""
    for chunk in completion:
        if chunk.choices[0].delta.content:
            answer += chunk.choices[0].delta.content

    answer = answer.replace("</s>", "")
    messages.append({"role": "assistant", "content": answer})
    return answer

def Content(topic):
    topic = topic.replace("content", "").strip()
    text = ContentWriter(topic)

    os.makedirs("Data", exist_ok=True)
    file_path = f"Data/{topic.lower().replace(' ', '')}.txt"

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(text)

    os.startfile(file_path)  # Windows open file
    return True

# ------------ App Opening / Closing (Windows) ------------ #

def OpenApp(app):
    try:
        appopen(app, match_closest=True)
    except:
        # fallback web search
        url = f"https://www.google.com/search?q={app}"
        webbrowser.open(url)

def CloseApp(app):
    try:
        appclose(app, match_closest=True)
    except:
        print(f"[!] Couldn't close {app}")

# ------------------ COMMAND HANDLER ------------------ #

def handle_command(cmd):
    cmd = cmd.lower().strip()

    if cmd.startswith("open "):
        return executor.submit(OpenApp, cmd.replace("open ", ""))

    elif cmd.startswith("close "):
        return executor.submit(CloseApp, cmd.replace("close ", ""))

    elif cmd.startswith("play "):
        return executor.submit(PlayYoutube, cmd.replace("play ", ""))

    elif cmd.startswith("youtube search "):
        return executor.submit(YoutubeSearch, cmd.replace("youtube search ", ""))

    elif cmd.startswith("google search "):
        return executor.submit(GoogleSearch, cmd.replace("google search ", ""))

    elif cmd.startswith("content "):
        return executor.submit(Content, cmd)

    else:
        print(f"[!] No function found for: {cmd}")
        return None

# ------------------ MAIN PROGRAM LOOP ------------------ #

def main():
    print("=== Windows Automation Assistant ===")
    print("Type commands like:")
    print("- open chrome")
    print("- close notepad")
    print("- play despacito")
    print("- google search python tutorial")
    print("- youtube search ai robots")
    print("- content Climate Change")
    print("- exit")

    futures = []

    while True:
        cmd = input(">>> ").strip()

        if cmd.lower() in ["exit", "quit"]:
            print("Exiting...")
            break

        future = handle_command(cmd)
        if future:
            futures.append(future)

    # Wait for all running threads to complete
    executor.shutdown(wait=True)


if __name__ == "__main__":
    main()
