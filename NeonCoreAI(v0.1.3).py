import json
import math
import os
import random
import re
import threading
import tkinter as tk
import urllib.parse
import urllib.request
import datetime
import html
from tkinter import filedialog, scrolledtext, messagebox, simpledialog

# ============================================================================
# PERSISTENT HISTORY STORAGE (Embedded)
# ============================================================================
# NEON_HISTORY_START
NEON_HISTORY = json.loads('{"chats": {"1": {"name": "New Session", "time": "2026-06-24T18:12:18.876328"}}, "messages": {"1": [{"role": "user", "text": "what is a banana"}, {"role": "bot", "text": "I searched everything but couldn\'t find a clear answer. Try being more specific?"}, {"role": "user", "text": "what is a banana"}, {"role": "bot", "text": "A banana is an edible fruit from banana plants. It is usually yellow when ripe, soft inside, sweet, and high in carbohydrates and potassium."}]}, "next_id": 2}')
# NEON_HISTORY_END

# Image support via Pillow
try:
    from PIL import Image, ImageTk, ImageStat
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

class MemoryDatabase:
    """Chat storage embedded in this file so history survives restarts."""
    _storage = None
    def __init__(self):
        if MemoryDatabase._storage is None:
            MemoryDatabase._storage = {
                "chats": {int(k): v for k, v in NEON_HISTORY.get("chats", {}).items()},
                "messages": {int(k): v for k, v in NEON_HISTORY.get("messages", {}).items()},
                "next_id": NEON_HISTORY.get("next_id", 1)
            }
    def create_chat(self, name):
        cid = self._storage["next_id"]
        self._storage["next_id"] += 1
        self._storage["chats"][cid] = {"name": name, "time": datetime.datetime.now().isoformat()}
        self._storage["messages"][cid] = []
        self._save()
        return cid
    def get_or_create_chat(self, name):
        if self._storage["chats"]: return sorted(self._storage["chats"].keys())[0]
        return self.create_chat(name)
    def add_msg(self, cid, role, text):
        if cid in self._storage["messages"]:
            self._storage["messages"][cid].append({"role": role, "text": text})
            self._save()
    def get_history(self, cid): return self._storage["messages"].get(cid, [])
    def get_chats(self): return sorted(self._storage["chats"].items())
    def clear_all(self):
        self._storage = {"chats": {}, "messages": {}, "next_id": 1}
        MemoryDatabase._storage = self._storage
        return self.create_chat("New Session")
    def _save(self):
        try:
            path = os.path.abspath(__file__)
            with open(path, "r", encoding="utf-8") as f: source = f.read()
            history = json.dumps(self._storage, ensure_ascii=False)
            replacement = f"# NEON_HISTORY_START\nNEON_HISTORY = json.loads({history!r})\n# NEON_HISTORY_END"
            source = re.sub(r"# NEON_HISTORY_START\nNEON_HISTORY = .*?\n# NEON_HISTORY_END", replacement, source, flags=re.DOTALL)
            with open(path, "w", encoding="utf-8") as f: f.write(source)
        except: pass

# ============================================================================
# OMNI-BRAIN: THE COMPLETE INTELLIGENCE ENGINE
# ============================================================================

class OmniBrain:
    """Local-first brain for chat, math, code, memory, explanations, and research."""
    def __init__(self):
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
        self.blacklist = ["ebay", "amazon", "aliexpress", "walmart", "target", "etsy", "wish", "temu", "alibaba"]
        self.ad_triggers = ["price", "shipping", "buy now", "discount", "sale", "stock", "cart", "$", "€", "£"]
        self.last_subject = ""
        self.small_facts = {
            "banana": "A banana is an edible fruit from banana plants. It is usually yellow when ripe, soft inside, sweet, and high in carbohydrates and potassium.",
            "python": "Python is a high-level programming language known for readable syntax, fast development, and broad use in automation, web apps, data work, AI, and scripting.",
            "ai": "AI means artificial intelligence: software designed to perform tasks that normally require human-like reasoning, language understanding, perception, or decision-making.",
            "computer": "A computer is an electronic machine that processes data using instructions called programs."
        }

    def _fetch(self, url):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': self.user_agent})
            with urllib.request.urlopen(req, timeout=12) as response:
                return response.read().decode('utf-8', errors='ignore')
        except Exception:
            return ""

    def _clean(self, text):
        text = html.unescape(re.sub(r'<.*?>', '', text))
        text = re.sub(r'(?<!\w)#\d+\b', '', text)
        return re.sub(r'\s+', ' ', text).strip(" -\n\t")

    def _history_text(self, history, limit=8):
        recent = history[-limit:] if history else []
        return "\n".join(f"{m.get('role', 'unknown')}: {m.get('text', '')}" for m in recent)

    def _safe_math(self, query):
        expr = query.lower()
        replacements = {
            "plus": "+", "minus": "-", "times": "*", "x": "*",
            "multiplied by": "*", "divided by": "/", "over": "/",
            "to the power of": "**", "^": "**"
        }
        for old, new in replacements.items():
            expr = expr.replace(old, new)
        expr = re.sub(r'[^0-9+\-*/().% ]', '', expr)
        if not expr.strip() or not re.search(r'\d\s*[+\-*/%]|\*\*', expr):
            return None
        try:
            result = eval(expr, {"__builtins__": {}}, {})
            if isinstance(result, float) and result.is_integer():
                result = int(result)
            return f"🧮 {query.strip()} = {result}"
        except Exception:
            return None

    def _code_answer(self, query):
        q = query.lower()
        if not any(k in q for k in ["code", "program", "script", "function", "make", "create", "write"]):
            return None
        if "python" in q:
            if "calculator" in q:
                code = """def calculate(a, op, b):
    if op == '+': return a + b
    if op == '-': return a - b
    if op == '*': return a * b
    if op == '/': return a / b
    raise ValueError('Unknown operator')

print(calculate(10, '+', 5))"""
            elif "hello" in q:
                code = "name = input('Name: ')\nprint(f'Hello, {name}!')"
            else:
                code = """def main():
    print('Your Python program starts here')

if __name__ == '__main__':
    main()"""
            return f"Here is a clean Python starting point:\n```python\n{code}\n```"
        if "javascript" in q or "js" in q:
            return "Here is a simple JavaScript starting point:\n```javascript\nfunction main() {\n  console.log('Hello from JavaScript');\n}\n\nmain();\n```"
        if "html" in q or "website" in q:
            return "Here is a simple HTML page:\n```html\n<!doctype html>\n<html>\n  <head><title>My Page</title></head>\n  <body>\n    <h1>Hello</h1>\n  </body>\n</html>\n```"
        return None

    def _memory_answer(self, query, history):
        q = query.lower()
        if not any(k in q for k in ["remember", "history", "what did i say", "last message", "recap", "summary"]):
            return None
        if not history:
            return "I do not have any saved messages in this chat yet."
        recent = history[-6:]
        lines = []
        for item in recent:
            role = "You" if item.get("role") == "user" else "NEON"
            text = item.get("text", "").replace("\n", " ")
            if len(text) > 140:
                text = text[:137] + "..."
            lines.append(f"• {role}: {text}")
        return "Recent chat history:\n" + "\n".join(lines)

    def _explain_answer(self, query):
        q = query.lower()
        if not q.startswith(("explain ", "why ", "how ")):
            return None
        topic = re.sub(r'^(explain|why|how)\s+', '', query, flags=re.I).strip()
        if not topic:
            return None
        return (
            f"Here is the simple version of {topic}:\n"
            f"• Core idea: it is a concept or process with parts that interact.\n"
            f"• How to understand it: identify the inputs, the steps, and the output.\n"
            f"• Best next step: ask me for an example, a diagram-style breakdown, or code."
        )

    def _research(self, query):
        encoded = urllib.parse.quote(query)
        results = []
        try:
            wiki_search = json.loads(self._fetch(f"https://en.wikipedia.org/w/api.php?action=opensearch&search={encoded}&limit=1&format=json"))
            if len(wiki_search) > 1 and wiki_search[1]:
                title = wiki_search[1][0]
                wiki_sum = json.loads(self._fetch(f"https://en.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(title.replace(' ', '_'))}"))
                extract = self._clean(wiki_sum.get("extract", ""))
                if extract:
                    results.append(("Core Fact", extract))
        except Exception:
            pass
        try:
            instant = json.loads(self._fetch(f"https://api.duckduckgo.com/?q={encoded}&format=json&no_html=1"))
            answer = self._clean(instant.get("AbstractText") or instant.get("Answer") or "")
            if answer:
                results.append(("Direct Answer", answer))
        except Exception:
            pass
        try:
            html_data = self._fetch(f"https://html.duckduckgo.com/html/?q={encoded}")
            snippets = re.findall(r'<a class="result__snippet".*?>(.*?)</a>', html_data, re.DOTALL)
            cleaned = []
            for snippet in snippets:
                text = self._clean(snippet)
                low = text.lower()
                if any(t in low for t in self.ad_triggers) and not any(k in query.lower() for k in ["buy", "shop", "price"]):
                    continue
                if len(text) > 30 and text not in cleaned:
                    cleaned.append(text)
            if cleaned:
                results.append(("Web Findings", cleaned[:5]))
        except Exception:
            pass
        if not results:
            return None
        response = []
        for label, content in results:
            if isinstance(content, list):
                response.append(f"🌐 **{label}:**")
                response.extend(f"• {item}" for item in content)
            else:
                response.append(f"💡 **{label}:**\n{content}")
        return "\n\n".join(response)

    def respond(self, query, history):
        q_low = query.lower().strip()
        if not q_low:
            return "Type something and I will work with it."

        if q_low in ["hi", "hello", "hey", "yo", "sup"]:
            return "NEON is online. Ask me for code, math, explanations, memory, or live info."
        if "thank" in q_low:
            return "Anytime."
        if q_low in ["time", "date", "today"]:
            return f"It's {datetime.datetime.now().strftime('%I:%M %p, %A, %B %d, %Y')}."
        if "what can you do" in q_low or q_low == "help":
            return "I can answer locally, calculate math, write starter code, explain topics, recap chat history, preview images, and research the web when needed."

        for answerer in (self._memory_answer,):
            ans = answerer(query, history)
            if ans:
                return ans

        math_ans = self._safe_math(query)
        if math_ans:
            return math_ans

        code_ans = self._code_answer(query)
        if code_ans:
            return code_ans

        for key, fact in self.small_facts.items():
            if re.search(rf'\b{re.escape(key)}s?\b', q_low) and any(k in q_low for k in ["what is", "what are", "tell me", "define"]):
                self.last_subject = key
                return fact

        explain_ans = self._explain_answer(query)
        if explain_ans and not any(k in q_low for k in ["latest", "current", "news", "today"]):
            return explain_ans

        search_query = query
        if len(query.split()) < 4 and self.last_subject and any(w in q_low for w in ["it", "this", "that", "more", "why", "how"]):
            search_query = f"{self.last_subject} {query}"
        if len(query.split()) > 2:
            self.last_subject = query

        research = self._research(search_query)
        if research:
            return research

        return (
            "I could not get a solid answer from my local rules or web research.\n"
            "Try asking with a specific topic, for example: `what is photosynthesis`, `write python code for a calculator`, or `12 * 8 + 4`."
        )

# ============================================================================
# GUI ARCHITECTURE
# ============================================================================

class NeonUI:
    def __init__(self, root):
        self.root = root
        self.root.title("NEON CORE AI")
        self.root.geometry("1100x850")
        self.root.configure(bg="#000000")
        
        self.memory = MemoryDatabase()
        self.chat_id = self.memory.get_or_create_chat("Main Session")
        self.brain = OmniBrain()
        self.img_cache = []
        
        self.orange, self.cyan = "#FF5F00", "#00FFCC"
        self._build_ui()
        self.load_history()

    def _build_ui(self):
        side = tk.Frame(self.root, bg="#080808", width=200)
        side.pack(side=tk.LEFT, fill=tk.Y)
        side.pack_propagate(False)
        
        tk.Label(side, text="SESSIONS", bg="#080808", fg=self.orange, font=("Consolas", 12, "bold")).pack(pady=20)
        self.chat_list = tk.Listbox(side, bg="#080808", fg="#666666", bd=0, highlightthickness=0, font=("Consolas", 10))
        self.chat_list.pack(fill=tk.BOTH, expand=True, padx=10)
        self.refresh_chats()
        
        tk.Button(side, text="+ New Chat", bg="#080808", fg=self.cyan, bd=0, command=self.new_chat).pack(pady=5)
        tk.Button(side, text="× Clear History", bg="#080808", fg=self.orange, bd=0, command=self.clear_history).pack(pady=10)
        
        main = tk.Frame(self.root, bg="#000000")
        main.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        header = tk.Frame(main, bg="#0A0A0A", height=60)
        header.pack(fill=tk.X)
        tk.Label(header, text="NEON CORE AI", bg="#0A0A0A", fg=self.orange, font=("Consolas", 14, "bold")).pack(side=tk.LEFT, padx=30)
        
        self.display = scrolledtext.ScrolledText(main, bg="#000000", fg="#FFFFFF", font=("Consolas", 12), bd=0, wrap=tk.WORD, state='disabled', padx=20, pady=20)
        self.display.pack(fill=tk.BOTH, expand=True)
        self.display.tag_config("user", foreground=self.orange, font=("Consolas", 12, "bold"))
        self.display.tag_config("bot", foreground=self.cyan)
        self.display.tag_config("code", foreground="#FFFFFF", background="#111111")

        footer = tk.Frame(main, bg="#000000", height=90)
        footer.pack(fill=tk.X, padx=20, pady=10)
        footer.pack_propagate(False)
        
        wrap = tk.Frame(footer, bg="#0F0F0F", highlightthickness=1, highlightbackground="#222222")
        wrap.pack(fill=tk.BOTH, expand=True)
        
        tk.Button(wrap, text="+", bg="#0F0F0F", fg=self.orange, bd=0, font=("Arial", 20), command=self.load_file).pack(side=tk.LEFT, padx=15)
        self.entry = tk.Entry(wrap, bg="#0F0F0F", fg="#FFFFFF", font=("Consolas", 13), bd=0, insertbackground=self.orange)
        self.entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.entry.bind("<Return>", lambda e: self.send())
        tk.Button(wrap, text="➜", bg="#0F0F0F", fg=self.orange, bd=0, font=("Arial", 20), command=self.send).pack(side=tk.RIGHT, padx=15)

    def refresh_chats(self):
        self.chat_list.delete(0, tk.END)
        for cid, chat in self.memory.get_chats(): self.chat_list.insert(tk.END, chat["name"])

    def new_chat(self):
        name = simpledialog.askstring("New Chat", "Chat name:")
        if name:
            self.chat_id = self.memory.create_chat(name)
            self.brain.chat_id = self.chat_id
            self.refresh_chats()
            self.clear_display()

    def clear_history(self):
        if messagebox.askyesno("Clear History", "Wipe all chat history?"):
            self.chat_id = self.memory.clear_all()
            self.refresh_chats()
            self.clear_display()

    def clear_display(self):
        self.display.config(state='normal')
        self.display.delete("1.0", tk.END)
        self.display.config(state='disabled')

    def load_history(self):
        for item in self.memory.get_history(self.chat_id):
            sender = "YOU" if item.get("role") == "user" else "NEON"
            tag = "user" if item.get("role") == "user" else "bot"
            self.add_msg(sender, item.get("text", ""), tag)

    def load_file(self):
        path = filedialog.askopenfilename()
        if path:
            filename = os.path.basename(path)
            if any(path.lower().endswith(e) for e in ['.png', '.jpg', '.jpeg', '.webp']) and HAS_PIL:
                img = Image.open(path); img.thumbnail((400, 400))
                photo = ImageTk.PhotoImage(img); self.img_cache.append(photo)
                self.display.config(state='normal'); self.display.image_create(tk.END, image=photo); self.display.insert(tk.END, "\n"); self.display.config(state='disabled')
                self.add_msg("SYSTEM", f"Visual scan of {filename} completed.", "bot")
            else: self.add_msg("SYSTEM", f"Document {filename} loaded.", "bot")

    def send(self):
        text = self.entry.get().strip()
        if text:
            self.add_msg("YOU", text, "user")
            self.memory.add_msg(self.chat_id, "user", text)
            self.entry.delete(0, tk.END)
            threading.Thread(target=self._process, args=(text,)).start()

    def _process(self, text):
        history = self.memory.get_history(self.chat_id)
        resp = self.brain.respond(text, history)
        self.root.after(0, lambda: self.add_msg("NEON", resp, "bot"))
        self.memory.add_msg(self.chat_id, "bot", resp)

    def add_msg(self, sender, msg, tag):
        self.display.config(state='normal')
        self.display.insert(tk.END, f"\n{sender}\n", tag)
        if "```" in msg:
            parts = msg.split("```")
            for i, p in enumerate(parts): self.display.insert(tk.END, p, "code" if i % 2 == 1 else None)
        else: self.display.insert(tk.END, msg + "\n")
        self.display.config(state='disabled'); self.display.yview(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    NeonUI(root)
    root.mainloop()
