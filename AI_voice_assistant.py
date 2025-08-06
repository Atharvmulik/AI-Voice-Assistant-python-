import tkinter as tk
from tkinter import scrolledtext
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
from PIL import Image, ImageTk, ImageDraw
import math
import time

class VoiceAssistant:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.todo_list = []
        self.is_speaking = False

    def listen(self):
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            try:
                audio = self.recognizer.listen(source, timeout=5)
                text = self.recognizer.recognize_google(audio)
                return text.lower()
            except sr.UnknownValueError:
                return "Sorry, could not understand the input"
            except sr.RequestError:
                return "Could not request results"
            except sr.WaitTimeoutError:
                return "Listening timed out"

    def speak(self, text):
        try:
            self.is_speaking = True
            tts = gTTS(text=text, lang='en')
            tts.save("output.mp3")
            playsound("output.mp3")
            os.remove("output.mp3")
            self.is_speaking = False
        except Exception as e:
            print(f"Error in speak function: {str(e)}")
            self.is_speaking = False

    # ... (keep all your existing assistant methods) ...

class VoiceAssistantGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("✨ Nova - AI Voice Assistant")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)
        
        # Set window properties
        self.root.configure(bg='#121212')
        
        self.assistant = VoiceAssistant()
        self.is_listening = False
        self.visualization_running = False
        
        # Color scheme
        self.colors = {
            'bg': '#121212',
            'text': '#e0e0e0',
            'primary': '#bb86fc',
            'secondary': '#03dac6',
            'console_bg': '#1e1e1e',
            'wave': '#bb86fc'
        }
        
        # Setup the UI
        self.setup_gui()
        
        # Start visualization animation
        self.start_visualization()
        
    def setup_gui(self):
        # Main container
        self.main_container = tk.Canvas(self.root, bg=self.colors['bg'], highlightthickness=0)
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # Header with animated title
        self.header_frame = tk.Frame(self.main_container, bg=self.colors['bg'])
        self.header_frame.place(relx=0.5, rely=0.1, anchor=tk.CENTER)
        
        self.title_label = tk.Label(
            self.header_frame,
            text="NOVA",
            font=("Arial", 48, "bold"),
            fg=self.colors['primary'],
            bg=self.colors['bg']
        )
        self.title_label.pack()
        
        self.subtitle_label = tk.Label(
            self.header_frame,
            text="Voice Interaction System",
            font=("Arial", 14),
            fg=self.colors['text'],
            bg=self.colors['bg']
        )
        self.subtitle_label.pack()
        
        # Voice visualization canvas
        self.visualization_canvas = tk.Canvas(
            self.main_container,
            bg=self.colors['bg'],
            width=600,
            height=200,
            highlightthickness=0
        )
        self.visualization_canvas.place(relx=0.5, rely=0.4, anchor=tk.CENTER)
        
        # Console output
        self.console_frame = tk.Frame(
            self.main_container,
            bg=self.colors['console_bg'],
            bd=0,
            highlightthickness=0
        )
        self.console_frame.place(relx=0.5, rely=0.7, anchor=tk.CENTER, width=800, height=300)
        
        self.response_area = scrolledtext.ScrolledText(
            self.console_frame,
            wrap=tk.WORD,
            font=('Consolas', 11),
            bg=self.colors['console_bg'],
            fg=self.colors['text'],
            insertbackground=self.colors['primary'],
            padx=20,
            pady=20,
            bd=0,
            highlightthickness=0
        )
        self.response_area.pack(fill=tk.BOTH, expand=True)
        
        # Voice activation orb
        self.orb_canvas = tk.Canvas(
            self.main_container,
            width=120,
            height=120,
            bg=self.colors['bg'],
            highlightthickness=0
        )
        self.orb_canvas.place(relx=0.5, rely=0.85, anchor=tk.CENTER)
        self.orb_id = self.orb_canvas.create_oval(10, 10, 110, 110, fill=self.colors['primary'], outline='')
        
        # Orb click binding
        self.orb_canvas.bind("<Button-1>", self.toggle_listening)
        
        # Orb label
        self.orb_label = tk.Label(
            self.main_container,
            text="Tap to Speak",
            font=("Arial", 10),
            fg=self.colors['text'],
            bg=self.colors['bg']
        )
        self.orb_label.place(relx=0.5, rely=0.92, anchor=tk.CENTER)
        
        # Status indicator
        self.status_indicator = tk.Label(
            self.main_container,
            text="",
            font=("Arial", 10),
            fg=self.colors['secondary'],
            bg=self.colors['bg']
        )
        self.status_indicator.place(relx=0.5, rely=0.96, anchor=tk.CENTER)
        
    def start_visualization(self):
        """Start the voice visualization animation"""
        if not self.visualization_running:
            self.visualization_running = True
            self.animate_visualization()
    
    def animate_visualization(self):
        """Animate the voice visualization"""
        if not self.visualization_running:
            return
            
        width = 600
        height = 200
        self.visualization_canvas.delete("all")
        
        # Draw a smooth waveform
        if self.is_listening or self.assistant.is_speaking:
            # Active state
            freq = random.uniform(0.05, 0.2)
            amplitude = random.randint(50, 80)
        else:
            # Idle state
            freq = 0.1
            amplitude = 20
            
        offset = height // 2
        points = []
        
        for x in range(0, width + 10, 10):
            y = offset + amplitude * math.sin(freq * x + time.time() * 3)
            points.extend([x, y])
        
        self.visualization_canvas.create_line(
            points,
            fill=self.colors['wave'],
            width=3,
            smooth=True
        )
        
        # Schedule next frame
        self.root.after(50, self.animate_visualization)
    
    def update_orb(self, active):
        """Update the voice orb appearance"""
        color = self.colors['secondary'] if active else self.colors['primary']
        self.orb_canvas.itemconfig(self.orb_id, fill=color)
        
        # Add pulse animation when active
        if active:
            self.pulse_orb()
    
    def pulse_orb(self):
        """Create a pulsing animation effect on the orb"""
        for i in range(1, 4):
            radius = 110 + i * 20
            self.orb_canvas.create_oval(
                60 - radius//2, 60 - radius//2,
                60 + radius//2, 60 + radius//2,
                outline=self.colors['secondary'],
                width=2,
                tags="pulse"
            )
        
        def shrink_pulse():
            items = self.orb_canvas.find_withtag("pulse")
            for item in items:
                coords = self.orb_canvas.coords(item)
                current_size = coords[2] - coords[0]
                if current_size > 120:
                    new_size = current_size - 5
                    self.orb_canvas.coords(
                        item,
                        60 - new_size//2, 60 - new_size//2,
                        60 + new_size//2, 60 + new_size//2
                    )
                    self.root.after(20, shrink_pulse)
                else:
                    self.orb_canvas.delete(item)
        
        self.root.after(20, shrink_pulse)
    
    def update_status(self, text):
        """Update the status indicator"""
        self.status_indicator.config(text=text)
        self.status_indicator.place(relx=0.5, rely=0.96, anchor=tk.CENTER)
        
        # Schedule fade out after delay
        self.root.after(3000, lambda: self.status_indicator.config(text=""))
    
    def append_response(self, text, is_user=False):
        """Add a response to the console"""
        tag = "user" if is_user else "assistant"
        color = self.colors['secondary'] if is_user else self.colors['primary']
        
        self.response_area.tag_config(tag, foreground=color)
        self.response_area.insert(tk.END, f"{'You' if is_user else 'Nova'}: {text}\n", tag)
        self.response_area.see(tk.END)
    
    def toggle_listening(self, event=None):
        """Toggle voice listening state"""
        if not self.is_listening:
            self.is_listening = True
            self.update_orb(True)
            self.update_status("Listening...")
            threading.Thread(target=self.listen_loop, daemon=True).start()
        else:
            self.is_listening = False
            self.update_orb(False)
            self.update_status("Ready")
    
    def listen_loop(self):
        """Main listening loop"""
        while self.is_listening and not self.assistant.is_speaking:
            command = self.assistant.listen()
            if command and command != "Sorry, could not understand the input":
                self.append_response(command, is_user=True)
                self.process_command(command)
    
    def process_command(self, command):
        """Process voice commands"""
        # ... (same command processing as before) ...
        pass
    
    # ... (keep all your existing command methods) ...

def main():
    root = tk.Tk()
    app = VoiceAssistantGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
