import os
import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
import threading
import time
import re
import datetime
import platform
import math
import random
import json
import urllib.request
import urllib.parse
import subprocess
import webbrowser
from textblob import TextBlob as TB
import html

# Optional Image Support
try:
    from PIL import Image, ImageTk, ImageStat
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

class WebEngine:
    def __init__(self):
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'

    def _fetch(self, url):
        req = urllib.request.Request(url, headers={'User-Agent': self.user_agent})
        with urllib.request.urlopen(req, timeout=15) as response:
            return response.read().decode('utf-8', errors='ignore')

    def search(self, query):
        try:
            encoded = urllib.parse.quote(query)
            
            # Fetch Wiki for core identity of the topic
            wiki_res = ""
            try:
                w_search = json.loads(self._fetch(f"https://en.wikipedia.org/w/api.php?action=opensearch&search={encoded}&limit=1&format=json"))
                if w_search[1]:
                    title = w_search[1][0]
                    w_sum = json.loads(self._fetch(f"https://en.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(title.replace(' ', '_'))}"))
                # Blocking wikipedia disambiguation pages to fetch better results without being cut off
                    if w_sum.get("type") == "disambiguation":
                        wiki_res = ""
                    else:
                        wiki_res = w_sum.get("extract", "")
            except: pass

            return wiki_res, []
        except:
            return None, []

class SmartBrain:
    def __init__(self):
        self.web = WebEngine()
        self.context = {"last_topic": None, "user_name": "User"}
        self.conversational_patterns = {
            r"hello|hi|hey|yo|gday|g'day|greetings": ["Hey! How's it going?", "Hi! What's on your mind?", "Yo! Ready for some answers?"],
            r"how are you|how ya going|how ya goin|how ya goin'": ["I'm doing great, feeling fast and local. You?", "Living the dream in your RAM. How about you?"],
            r"who are you": ["I'm Neon, your local-core assistant. No big clouds, just me and the web."],
            r"what can you do": ["I can scour the web, solve math, analyze files, and just chat. Try me!"],
            r"thanks|thank you|tysm|ty": ["No problem!", "Anytime!", "Happy to help!"]
        }

    def get_response(self, text):
        text_lower = text.lower().strip()
        if text_lower=="help":
            return "I am neon core AI, I can search the wiki for answers (like what is a banana), do maths and some other things!"
        
        # 1. Check for Conversational Matches
        for pattern, responses in self.conversational_patterns.items():
            if re.search(pattern, text_lower):
                return random.choice(responses)

        # 2. System / Tools
        if "time" in text_lower: return f"It is {datetime.datetime.now().strftime('%I:%M %p')}."
        if "system" in text_lower: return f"System: {platform.system()} | Host: {platform.node()}"
        
        # 3. Math
        if re.search(r'[\d\+\-\*\/\(\)\^]', text) and any(c in text for c in "+-*/^%"):
            try:
                expr = text.replace("^", "**")
                res = eval(re.sub(r'[^0-9\+\-\*\/\(\)\.\%\s\*\^a-zA-Z]', '', expr), {"__builtins__": None}, {k: getattr(math, k) for k in dir(math) if not k.startswith("_")})
                return f"Calculated: {res}"
            except: pass

        # 4. Web Scouring (The Core)
        wiki, snippets = self.web.search(text)
        if wiki:
            self.context["last_topic"] = text
            return html.unescape(wiki)

        # 5. TextBlob Dynamic Fallbacks
        blob = TB(text)
        if blob.sentiment.polarity < 0:
            resp = "I can't understand this response, because I'm currently restricted to localized math, reading image properties, or Wikipedia queries, but I think that is a negative response!"
            if blob.subjectivity > 0:
                resp += " I also think it is biased."
            elif blob.subjectivity < 0:
                resp += " I also think it is non-biased."
            return resp
            
        elif blob.sentiment.polarity > 0:
            resp = "I can't understand this response, because I'm currently restricted to localized math, reading image properties, or Wikipedia queries, but I think that is a positive response!"
            if blob.subjectivity > 0:
                resp += " I also think it is biased."
            elif blob.subjectivity < 0:
                resp += " I also think it is non-biased."
            return resp
            
        else:
            resp = f"I can't understand this response, because I'm currently restricted to localized math, reading image properties, or Wikipedia queries, so I'm not sure how to respond to '{text}'."
            if blob.subjectivity > 0:
                resp += " But I think it is biased! \n\nTry asking for 'help' to see what I can do!"
            else:
                resp += " But I think it is non-biased! \n\nTry asking for 'help' to see what I can do!"
            return resp

class NeonUI:
    def __init__(self, root):
        self.root = root
        self.root.title("NEON CORE")
        self.root.geometry("800x900")
        self.root.configure(bg="#000000")
        
        self.orange = "#FF5F00"
        self.cyan = "#00FFCC"
        self.brain = SmartBrain()
        self.attached_path = None
        
        self._build_layout()

    def _build_layout(self):
        # 1. Header Bar
        header = tk.Frame(self.root, bg="#080808", height=60)
        header.pack(side=tk.TOP, fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(header, text="NEON CORE AI", bg="#080808", fg=self.orange, font=("Consolas", 16, "bold")).pack(side=tk.LEFT, padx=20)
        self.status_dot = tk.Label(header, text="●", bg="#080808", fg="#00FF00", font=("Arial", 14))
        self.status_dot.pack(side=tk.RIGHT, padx=(0, 5))
        self.status_text = tk.Label(header, text="SYSTEM ONLINE", bg="#080808", fg="#555555", font=("Consolas", 9))
        self.status_text.pack(side=tk.RIGHT, padx=(0, 20))

        # 2. Chat Display Area
        chat_frame = tk.Frame(self.root, bg="#000000")
        chat_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.display = scrolledtext.ScrolledText(
            chat_frame, bg="#000000", fg="#FFFFFF", font=("Consolas", 12),
            bd=0, wrap=tk.WORD, state='disabled', padx=15, pady=15,
            highlightthickness=1, highlightbackground="#111111"
        )
        self.display.pack(fill=tk.BOTH, expand=True)
        self.display.tag_config("user_tag", foreground=self.orange, font=("Consolas", 12, "bold"))
        self.display.tag_config("bot_tag", foreground=self.cyan, font=("Consolas", 12, "bold"))

        # 3. Interaction Area (Footer)
        footer = tk.Frame(self.root, bg="#000000", height=80) # Dark base
        footer.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)
        footer.pack_propagate(False)
        
        input_container = tk.Frame(footer, bg="#111111", highlightthickness=1, highlightbackground="#333333")
        input_container.pack(fill=tk.BOTH, expand=True)

        self.btn_file = tk.Button(input_container, text="+", bg="#111111", fg=self.orange, bd=0, font=("Arial", 18), activebackground="#1a1a1a", command=self.pick_file)
        self.btn_file.pack(side=tk.LEFT, padx=10)

        # Fix for the entry bar - removed pady and added ipady to fill container vertically
        self.entry = tk.Entry(input_container, bg="#111111", fg="#FFFFFF", font=("Consolas", 13), bd=0, insertbackground=self.orange)
        self.entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.entry.bind("<Return>", lambda e: self.send())

        self.btn_send = tk.Button(input_container, text="➜", bg="#111111", fg=self.orange, bd=0, font=("Arial", 18), activebackground="#1a1a1a", command=self.send)
        self.btn_send.pack(side=tk.RIGHT, padx=10)

    def pick_file(self):
        path = filedialog.askopenfilename()
        if path:
            self.attached_path = path
            self.set_status(f"LOADED: {os.path.basename(path)}", self.orange)

    def set_status(self, text, color="#555555"):
        self.status_text.config(text=text.upper(), fg=color)
        self.status_dot.config(fg="#FF8C00" if "THINKING" in text.upper() else "#00FF00")

    def send(self):
        text = self.entry.get().strip()
        if not text and not self.attached_path: return
        
        self.add_msg("YOU", text, "user_tag")
        self.entry.delete(0, tk.END)
        self.set_status("THINKING...", self.orange)
        
        threading.Thread(target=self._process, args=(text,)).start()

    def _process(self, text):
        # Handle file if attached
        if self.attached_path:
            filename = os.path.basename(self.attached_path)
            ext = os.path.splitext(self.attached_path)[1].lower()
            resp = ""
            if ext in ['.png', '.jpg', '.jpeg', '.webp'] and HAS_PIL:
                with Image.open(self.attached_path) as img:
                    resp = f"Image '{filename}' detected. It's {img.width}x{img.height} pixels. Ready for instructions."
            else:
                try:
                    with open(self.attached_path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read(1000)
                        resp = f"File '{filename}' loaded. Preview:\n\n{content}..."
                except: resp = "Error reading the file."
            self.attached_path = None
            self.root.after(0, lambda: self.add_msg("NEON", resp, "bot_tag"))
        else:
            resp = self.brain.get_response(text)
            self.root.after(0, lambda: self.add_msg("NEON", resp, "bot_tag"))
        
        self.root.after(0, lambda: self.set_status("SYSTEM ONLINE"))

    def add_msg(self, sender, msg, tag):
        self.display.config(state='normal')
        self.display.insert(tk.END, f"\n{sender}\n", tag)
        self.display.insert(tk.END, f"{msg}\n")
        self.display.config(state='disabled')
        self.display.yview(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    NeonUI(root)
    root.mainloop()
