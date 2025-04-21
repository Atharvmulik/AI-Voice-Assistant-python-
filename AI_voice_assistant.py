


import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
import speech_recognition as sr
from gtts import gTTS
import os
import webbrowser
import time
import pyautogui
from playsound import playsound
import wikipedia
import random
import re

class VoiceAssistant:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.todo_list = []

    def listen(self):
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            try:
                audio = self.recognizer.listen(source)
                text = self.recognizer.recognize_google(audio)
                return text.lower()
            except sr.UnknownValueError:
                return "Sorry, could not understand the input"
            except sr.RequestError:
                return "Could not request results"

    def speak(self, text):
        try:
            tts = gTTS(text=text, lang='en')
            tts.save("output.mp3")
            playsound("output.mp3")
            os.remove("output.mp3")
        except Exception as e:
            print(f"Error in speak function: {str(e)}")

    def search_youtube(self, query):
        try:
            webbrowser.open(f"https://www.youtube.com/results?search_query={query}")
            time.sleep(5)
            pyautogui.click(x=631, y=553)
            return f"Searching YouTube for: {query}"
        except Exception as e:
            return f"Error searching YouTube: {str(e)}"

    def search_wikipedia(self, query):
        try:
            wiki_result = wikipedia.summary(query, sentences=2)
            return f"Wikipedia says: {wiki_result}"
        except Exception as e:
            return f"An error occurred: {str(e)}"

    def play_spotify(self, song_name):
        try:
            webbrowser.open(f"https://open.spotify.com/search/{song_name}")
            time.sleep(10)
            pyautogui.click(x=635, y=574)
            return f"Playing {song_name}"
        except Exception as e:
            return f"Error playing music: {str(e)}"

    def play_snake_water_gun(self):
        choices = ['snake', 'water', 'revolver']
        computer_choice = random.choice(choices)
        self.speak("Choose snake, water, or revolver")
        user_choice = self.listen()

        if user_choice not in choices:
            return "Invalid choice"

        self.speak(f"Computer chose {computer_choice}")
        if user_choice == computer_choice:
            return "It's a tie!"
        elif ((user_choice == 'snake' and computer_choice == 'water') or
              (user_choice == 'water' and computer_choice == 'revolver') or
              (user_choice == 'revolver' and computer_choice == 'snake')):
            return "You win!"
        else:
            return "Computer wins!"

    def get_club_info(self, club_name):
        clubs_info = {
            "sports club": "Sports club is one of most enthusiastic clubs in VIT Pune...",
            "sarathi club": "Sarthi is the largest club in VIT college...",
            "robotics club": "The Robotics Club focuses on building robots, and making new innovations..."
        }
        return clubs_info.get(club_name.lower(), "Sorry, I don't have information about that club.")

    def get_member_info(self, query):
        members_info = {
            "atharv": {"name": "Atharv Mulik", "age": 19, "roll_no": "27", "village": "Walchandnagar, Indapur"},
            "siddhi": {"name": "Siddhi Naik", "age": 19, "roll_no": "33", "village": "Kivale Gaon, Pune"},
            "sandesh": {"name": "Sandesh Nakade", "age": 19, "roll_no": "34", "village": "Nagpur, Indapur"},
            "rudra": {"name": "Rudra", "age": 19, "roll_no": "48", "village": "Beed, Maharashtra"},
            "mohit": {"name": "Mohit", "age": 19, "roll_no": "36", "village": "Maharashtra"},
            "arpita": {"name": "Arpita", "age": 19, "roll_no": "35", "village": "Parbhani"}
        }
        query = query.lower()
        roll_number_match = re.search(r"roll no (\d+)", query)

        if roll_number_match:
            roll_no = roll_number_match.group(1)
            for member in members_info.values():
                if member["roll_no"] == roll_no:
                    return f"{member['name']} is {member['age']} years old, with roll number {member['roll_no']}, from {member['village']}."

        for member in members_info.values():
            if member["name"].lower() in query:
                return f"{member['name']} is {member['age']} years old, with roll number {member['roll_no']}, from {member['village']}."

        return "Sorry, I don't have information about that member."

    def add_to_todo_list(self, task):
        self.todo_list.append(task)
        return f"Added '{task}' to your to-do list."

    def remove_from_todo_list(self, task):
        if task in self.todo_list:
            self.todo_list.remove(task)
            return f"Removed '{task}' from your to-do list."
        else:
            return f"'{task}' not found in your to-do list."

    def show_todo_list(self):
        if not self.todo_list:
            return "Your to-do list is empty."
        return "Your to-do list:\n" + "\n".join(f"{i+1}. {task}" for i, task in enumerate(self.todo_list))


class VoiceAssistantGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("✨ AI Voice Assistant")
        self.root.geometry("1100x700")
        self.root.configure(bg="#1e1e2f")

        self.assistant = VoiceAssistant()
        self.is_listening = False

        self.setup_gui()

    def setup_gui(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton", font=("Segoe UI", 10, "bold"), foreground="#ffffff", background="#444")
        style.configure("TLabel", background="#1e1e2f", foreground="#ffffff", font=("Segoe UI", 12))
        
        title = ttk.Label(self.root, text="🎙️ AI Voice Assistant", font=("Segoe UI", 22, "bold"))
        title.pack(pady=15)

        self.response_area = scrolledtext.ScrolledText(
            self.root, wrap=tk.WORD, width=90, height=25,
            font=('Consolas', 11), bg="#111", fg="#00FFAA", insertbackground="white"
        )
        self.response_area.pack(pady=10)

        button_frame = tk.Frame(self.root, bg="#1e1e2f")
        button_frame.pack(pady=10)

        self.toggle_button = tk.Button(button_frame, text="🎤 Start Listening", font=('Segoe UI', 10, 'bold'),
                                       command=self.toggle_listening, bg="#00AAFF", fg="white", padx=10, pady=5)
        self.toggle_button.grid(row=0, column=0, padx=5)

        buttons = [
            ("YouTube", self.youtube_search),
            ("Wikipedia", self.wikipedia_search),
            ("Music", self.play_music),
            ("Game", self.play_game),
            ("Todo List", self.todo_list),
            ("Club Info", self.club_info),
            ("Member Info", self.member_info),
            ("Clear", self.clear_response_area)
        ]

        for i, (label, command) in enumerate(buttons):
            tk.Button(button_frame, text=label, command=command,
                      bg="#333", fg="white", font=('Segoe UI', 10),
                      padx=10, pady=5, relief=tk.RAISED, bd=2).grid(row=0, column=i + 1, padx=5)

        self.status_label = ttk.Label(self.root, text="Status: Ready")
        self.status_label.pack(pady=5)

    def update_status(self, text):
        self.status_label.config(text=f"Status: {text}")
        self.root.update()

    def append_response(self, text):
        self.response_area.insert(tk.END, f"{text}\n")
        self.response_area.see(tk.END)

    def clear_response_area(self):
        self.response_area.delete(1.0, tk.END)

    def toggle_listening(self):
        if not self.is_listening:
            self.is_listening = True
            self.toggle_button.config(text="⏹️ Stop Listening")
            self.update_status("Listening...")
            threading.Thread(target=self.listen_loop, daemon=True).start()
        else:
            self.is_listening = False
            self.toggle_button.config(text="🎤 Start Listening")
            self.update_status("Ready")

    def listen_loop(self):
        while self.is_listening:
            command = self.assistant.listen()
            if command != "Sorry, could not understand the input":
                self.append_response(f"You said: {command}")
                self.process_command(command)

    def process_command(self, command):
        if any(phrase in command for phrase in ['search youtube', 'find on youtube']):
            self.youtube_search()
        elif any(phrase in command for phrase in ['what is', 'who is', 'tell me about']):
            result = self.assistant.search_wikipedia(command)
            self.append_response(f"Assistant: {result}")
            self.assistant.speak(result)
        elif any(phrase in command for phrase in ['to do list', 'todo list']):
            self.todo_list()

    def youtube_search(self):
        self.update_status("Listening for YouTube search...")
        self.assistant.speak("What should I search on YouTube?")
        query = self.assistant.listen()
        if query != "Sorry, could not understand the input":
            result = self.assistant.search_youtube(query)
            self.append_response(result)

    def wikipedia_search(self):
        self.update_status("Listening for Wikipedia search...")
        self.assistant.speak("What would you like to know about?")
        query = self.assistant.listen()
        if query != "Sorry, could not understand the input":
            result = self.assistant.search_wikipedia(query)
            self.append_response(result)
            self.assistant.speak(result)

    def play_music(self):
        self.update_status("Listening for song name...")
        self.assistant.speak("What song would you like to play?")
        song = self.assistant.listen()
        if song != "Sorry, could not understand the input":
            result = self.assistant.play_spotify(song)
            self.append_response(result)
            self.assistant.speak(result)

    def play_game(self):
        self.update_status("Starting game...")
        result = self.assistant.play_snake_water_gun()
        self.append_response(result)
        self.assistant.speak(result)

    def todo_list(self):
        self.update_status("Listening for action...")
        self.assistant.speak("What should you want to do: add task, remove task, or view task?")
        action = self.assistant.listen()

        if "add" in action:
            self.assistant.speak("What task would you like to add?")
            task = self.assistant.listen()
            if task != "Sorry, could not understand the input":
                result = self.assistant.add_to_todo_list(task)
                self.append_response(result)
                self.assistant.speak(result)
        elif "remove" in action:
            self.assistant.speak("What task would you like to remove?")
            task = self.assistant.listen()
            if task != "Sorry, could not understand the input":
                result = self.assistant.remove_from_todo_list(task)
                self.append_response(result)
                self.assistant.speak(result)
        elif "view" in action:
            result = self.assistant.show_todo_list()
            self.append_response(result)
            self.assistant.speak(result)
        else:
            self.append_response("Invalid action. Please say 'add task', 'remove task', or 'view task'.")

    def club_info(self):
        self.update_status("Listening for club name...")
        self.assistant.speak("Which club would you like to know about?")
        club = self.assistant.listen()
        if club != "Sorry, could not understand the input":
            info = self.assistant.get_club_info(club)
            self.append_response(info)
            self.assistant.speak(info)

    def member_info(self):
        self.update_status("Listening for member query...")
        self.assistant.speak("Please provide member name")
        query = self.assistant.listen()
        if query != "Sorry, could not understand the input":
            info = self.assistant.get_member_info(query)
            self.append_response(info)
            self.assistant.speak(info)


def main():
    root = tk.Tk()
    app = VoiceAssistantGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
