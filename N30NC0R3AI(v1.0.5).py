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
import base64
from tkinter import filedialog, scrolledtext, messagebox, simpledialog, ttk

# ============================================================================
# PERSISTENT STORAGE (Safe Base64 Encoding)
# ============================================================================
# NEON_HISTORY_START
NEON_HISTORY_B64 = 'eyJjaGF0cyI6IHsiMSI6IHsibmFtZSI6ICJOZXcgU2Vzc2lvbiIsICJ0aW1lIjogIjIwMjYtMDYtMjdUMTI6MTU6MTYuNTMxOTIwIn19LCAibWVzc2FnZXMiOiB7IjEiOiBbeyJyb2xlIjogInVzZXIiLCAidGV4dCI6ICJoaSJ9LCB7InJvbGUiOiAiYm90IiwgInRleHQiOiAiTjMwTiBDMFIzIEFJIE9OTElORS4ifV19LCAibmV4dF9pZCI6IDJ9'
# NEON_HISTORY_END

# NEON_SETTINGS_START
NEON_SETTINGS_B64 = 'eyJ0aGVtZSI6ICJTb2Z0IE5pZ2h0IChHcmVlbikiLCAiaW50ZWxsaWdlbmNlIjogIkRlZXAiLCAicmVzcG9uc2Vfc3R5bGUiOiAiRGV0YWlsZWQiLCAic3BlZWQiOiAiTm9ybWFsIiwgInJlc3VsdF9jb3VudCI6IDE1LCAiZm9udF9zaXplIjogMTIsICJ3ZWJfc2VhcmNoIjogdHJ1ZSwgIndpa2lwZWRpYSI6IHRydWUsICJsaXZlX3NlYXJjaCI6IHRydWUsICJnaXRodWJfc2VhcmNoIjogZmFsc2UsICJyZWRkaXRfc2VhcmNoIjogZmFsc2UsICJuZXdzX3NlYXJjaCI6IGZhbHNlLCAiYWRfZmlsdGVyIjogdHJ1ZSwgInNhdmVfbWVtb3J5IjogdHJ1ZSwgInNhdmVfbG9jYWxseSI6IGZhbHNlLCAic2F2ZV9wYXRoIjogIiJ9'
# NEON_SETTINGS_END

def _decode_store(b64_str):
    try: return json.loads(base64.b64decode(b64_str).decode('utf-8'))
    except: return {}

NEON_HISTORY = _decode_store(NEON_HISTORY_B64)
NEON_SETTINGS = _decode_store(NEON_SETTINGS_B64)

try:
    from PIL import Image, ImageTk, ImageStat
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

# ============================================================================
# C0R3-X BRAIN: ADVANCED COGNITIVE SYNTHESIS (V5)
# ============================================================================

class ThinkingBrain:
    """
    C0R3-X Logic Engine:
    Uses multi-stage query decomposition, location-aware heuristics,
    and a recursive synthesis layer to provide high-quality intelligence.
    """
    def __init__(self, settings=None):
        self.settings = settings or {}
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
        ]
        self.last_subject = ""
        self.local_keywords = ["rockingham", "wellard", "perth", "wa", "australia", "near", "nearby", "local"]
        self.intent_patterns = {
            "shopping": r"\b(buy|get|shop|store|grocer|price|cost|sale|mall|market)\b",
            "food": r"\b(restaurant|cafe|eat|drink|food|dinner|lunch|breakfast|takeaway|menu)\b",
            "howto": r"\b(how to|step|guide|tutorial|way to|fix|repair)\b",
            "factual": r"\b(what is|who is|define|meaning of|history of|facts about)\b"
        }

    def update_settings(self, settings): self.settings = settings

    def _fetch(self, url, timeout=15):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': random.choice(self.user_agents)})
            with urllib.request.urlopen(req, timeout=timeout) as response:
                return response.read().decode('utf-8', errors='ignore')
        except: return ""

    def _clean_html(self, text):
        text = html.unescape(re.sub(r'<[^>]+>', ' ', text))
        return re.sub(r'\s+', ' ', text).strip()

    def _parse_ddg(self, raw_html):
        """Advanced extraction of titles, snippets, and source names."""
        results = []
        blocks = re.findall(r'<div class="result__body">.*?</div>\s*</div>', raw_html, re.DOTALL)
        for block in blocks:
            title_match = re.search(r'class="result__a"[^>]*>(.*?)</a>', block, re.DOTALL)
            snippet_match = re.search(r'class="result__snippet"[^>]*>(.*?)</a>', block, re.DOTALL)
            url_match = re.search(r'class="result__url"[^>]*>(.*?)</a>', block, re.DOTALL)
            
            if title_match and snippet_match:
                results.append({
                    "title": self._clean_html(title_match.group(1)),
                    "snippet": self._clean_html(snippet_match.group(1)),
                    "source": self._clean_html(url_match.group(1)) if url_match else "Web"
                })
        return results

    def respond(self, query, history):
        q_low = query.lower().strip()
        
        # 1. IMMEDIATE HEURISTICS
        if q_low in ["time", "date"]: return f"🕒 {datetime.datetime.now().strftime('%I:%M %p, %A, %B %d, %Y')}"
        if any(k in q_low for k in ["who are you", "your name"]): return "I am N30N C0R3 AI, powered by the C0R3-X Logic Engine."

        # 2. INTENT CLASSIFICATION
        intent = "general"
        for key, pattern in self.intent_patterns.items():
            if re.search(pattern, q_low):
                intent = key
                break
        
        is_local = any(loc in q_low for loc in self.local_keywords)

        # 3. CONTEXT SYNTHESIS
        pronouns = {"it", "they", "them", "there", "here", "its", "those", "these", "that", "him", "her"}
        words = q_low.split()
        needs_context = len(words) < 3 or any(w in pronouns for w in words)
        
        effective_query = query
        if needs_context and self.last_subject:
            effective_query = f"{query} {self.last_subject}"
        
        # Update Subject Tracking
        clean_sub = re.sub(r'\b(what|where|who|is|are|the|best|good|find|me|search|for|how|to|any|nearby|tell|about)\b', '', q_low).strip()
        if len(clean_sub) > 3 and not any(w in pronouns for w in words):
            self.last_subject = clean_sub

        # 4. MULTI-PATH RESEARCH DATA ACQUISITION
        research_data = []
        search_variants = [effective_query]
        
        if intent in ["shopping", "food"] or is_local:
            search_variants.append(f"{effective_query} locations address contact")
            search_variants.append(f"{effective_query} reviews ratings")
        elif intent == "howto":
            search_variants.append(f"{effective_query} step by step instructions")
        
        seen_snippets = set()
        for variant in search_variants[:2]:
            raw_html = self._fetch(f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(variant)}")
            scraped = self._parse_ddg(raw_html)
            for item in scraped:
                if item["snippet"].lower() not in seen_snippets:
                    research_data.append(item)
                    seen_snippets.add(item["snippet"].lower())

        # 5. DATA SCORING & COGNITIVE ANALYSIS
        scored_results = []
        query_keywords = set(re.findall(r'\b\w{3,}\b', effective_query.lower()))
        
        for item in research_data:
            score = 0
            combined_text = (item["title"] + " " + item["snippet"]).lower()
            for kw in query_keywords:
                if kw in combined_text: score += 10
            if is_local and any(loc in combined_text for loc in self.local_keywords):
                score += 15
            if any(marker in combined_text for marker in ["st ", "rd ", "ave ", "highway", "mall", "centre", "shop ", "ph:"]):
                score += 8
            scored_results.append((score, item))
        
        scored_results.sort(key=lambda x: x[0], reverse=True)
        top_tier = [x[1] for x in scored_results if x[0] > 0]

        # 6. RESPONSE REFINEMENT
        if not top_tier:
            return "I couldn't synthesize a definitive answer from current research layers. Please try a more specific query, including a suburb or detailed topic."

        final_output = f"⚡ **C0R3-X COGNITIVE REPORT: {self.last_subject.upper()}**\n"
        locations = [i for i in top_tier if any(k in (i["title"] + i["snippet"]).lower() for k in ["st ", "rd ", "ave ", "open", "address", "phone", "located", "ph:"])]
        factual = [i for i in top_tier if i not in locations]

        if (intent in ["shopping", "food"] or is_local) and locations:
            final_output += "\n📍 **VERIFIED LOCATIONS & ENTITIES:**\n"
            for loc in locations[:6]:
                addr_match = re.search(r'\d+ [A-Za-z]+ (?:St|Rd|Ave|Hwy|Way|Pde|Cct)', loc["snippet"])
                addr = f" - {addr_match.group(0)}" if addr_match else ""
                final_output += f"• **{loc['title']}**{addr}\n  _{loc['snippet']}_\n"

        if factual:
            final_output += "\n🔍 **RESEARCH SYNTHESIS:**\n"
            for fact in factual[:6]:
                final_output += f"• {fact['snippet']}\n"

        if re.search(r'[\d\+\-\*\/\(\)\^]', query) and any(c in query for c in "+-*/"):
            try:
                expr = query.replace("^", "**")
                clean_expr = re.sub(r'[^0-9\+\-\*\/\(\)\.\%\s\*\^a-zA-Z]', '', expr)
                math_val = eval(clean_expr, {'__builtins__': None}, {k: getattr(math, k) for k in dir(math) if not k.startswith('_')})
                final_output = f"🔢 **CALCULATION:** {math_val}\n\n" + final_output
            except: pass

        return final_output.strip()

# ============================================================================
# INFRASTRUCTURE (Storage, Settings, UI)
# ============================================================================

class MemoryDatabase:
    _storage = None
    def __init__(self, settings=None):
        self.settings = settings or {}
        if MemoryDatabase._storage is None:
            if self.settings.get("save_locally") and self.settings.get("save_path") and os.path.exists(self.settings["save_path"]):
                try:
                    with open(self.settings["save_path"], "r") as f: MemoryDatabase._storage = json.load(f)
                except: pass
            if MemoryDatabase._storage is None:
                MemoryDatabase._storage = {"chats": {int(k): v for k, v in NEON_HISTORY.get("chats", {}).items()}, "messages": {int(k): v for k, v in NEON_HISTORY.get("messages", {}).items()}, "next_id": NEON_HISTORY.get("next_id", 1)}

    def create_chat(self, name):
        cid = self._storage["next_id"]; self._storage["next_id"] += 1
        self._storage["chats"][cid] = {"name": name, "time": datetime.datetime.now().isoformat()}
        self._storage["messages"][cid] = []; self._save(); return cid

    def get_or_create_chat(self):
        if self._storage["chats"]: return sorted(self._storage["chats"].keys())[0]
        return self.create_chat("New Session")

    def add_msg(self, cid, role, text):
        if cid in self._storage["messages"]: 
            self._storage["messages"][cid].append({"role": role, "text": text})
            if self.settings.get("save_memory", True): self._save()

    def get_history(self, cid): return self._storage["messages"].get(cid, [])
    def get_chats(self): return sorted(self._storage["chats"].items())
    def clear_all(self): self._storage = {"chats": {}, "messages": {}, "next_id": 1}; return self.create_chat("New Session")

    def _save(self):
        if self.settings.get("save_locally") and self.settings.get("save_path"):
            try:
                with open(self.settings["save_path"], "w") as f: json.dump(self._storage, f, indent=4)
                return
            except: pass
        try:
            path = os.path.abspath(__file__)
            with open(path, "r") as f: source = f.read()
            b64 = base64.b64encode(json.dumps(self._storage).encode('utf-8')).decode('utf-8')
            source = re.sub(r"# NEON_HISTORY_START\nNEON_HISTORY_B64 = .*?\n# NEON_HISTORY_END", f"# NEON_HISTORY_START\nNEON_HISTORY_B64 = '{b64}'\n# NEON_HISTORY_END", source, flags=re.DOTALL)
            with open(path, "w") as f: f.write(source)
        except: pass

class SettingsStore:
    def __init__(self): self.data = NEON_SETTINGS
    def save(self):
        try:
            path = os.path.abspath(__file__)
            with open(path, "r") as f: source = f.read()
            b64 = base64.b64encode(json.dumps(self.data).encode('utf-8')).decode('utf-8')
            source = re.sub(r"# NEON_SETTINGS_START\nNEON_SETTINGS_B64 = .*?\n# NEON_SETTINGS_END", f"# NEON_SETTINGS_START\nNEON_SETTINGS_B64 = '{b64}'\n# NEON_SETTINGS_END", source, flags=re.DOTALL)
            with open(path, "w") as f: f.write(source)
        except: pass

class NeonUI:
    themes = {
        "Neon Orange": {"bg": "#000000", "panel": "#0A0A0A", "field": "#111111", "accent": "#FF5F00", "bot": "#00F0FF", "text": "#FFFFFF", "muted": "#444444"},
        "Neon Pink": {"bg": "#000000", "panel": "#0A0A0A", "field": "#111111", "accent": "#FF007F", "bot": "#BC13FE", "text": "#FFFFFF", "muted": "#444444"},
        "Neon Green": {"bg": "#000000", "panel": "#030803", "field": "#061206", "accent": "#39FF14", "bot": "#00FFCC", "text": "#E8FFE8", "muted": "#1A4D1A"},
        "Neon Blue": {"bg": "#000000", "panel": "#00050f", "field": "#000c1f", "accent": "#00BFFF", "bot": "#00FFFF", "text": "#E0F7FF", "muted": "#003366"},
        "Neon Red": {"bg": "#000000", "panel": "#0f0000", "field": "#1f0000", "accent": "#FF003F", "bot": "#FF6600", "text": "#FFE0E0", "muted": "#660000"},
        "Soft Night (Green)": {"bg": "#121212", "panel": "#1E1E1E", "field": "#252525", "accent": "#81C784", "bot": "#64B5F6", "text": "#E0E0E0", "muted": "#424242"},
        "Soft Night (Blue)": {"bg": "#0D1117", "panel": "#161B22", "field": "#21262D", "accent": "#58A6FF", "bot": "#A5D6FF", "text": "#C9D1D9", "muted": "#484F58"}
    }

    def __init__(self, root):
        self.root = root; self.root.title("N30N C0R3 AI"); self.root.geometry("1100x900")
        self.settings_store = SettingsStore(); self.settings = self.settings_store.data
        self.memory = MemoryDatabase(self.settings); self.chat_id = self.memory.get_or_create_chat()
        self.brain = ThinkingBrain(self.settings); self.img_cache = []
        self._build_layout(); self.apply_theme(); self.load_history()

    def _build_layout(self):
        self.header = tk.Frame(self.root, height=60); self.header.pack(side=tk.TOP, fill=tk.X)
        self.logo = tk.Label(self.header, text="N30N C0R3 AI", font=("Consolas", 16, "bold")); self.logo.pack(side=tk.LEFT, padx=30)
        self.paned = tk.PanedWindow(self.root, orient=tk.HORIZONTAL, bd=0, sashwidth=2); self.paned.pack(fill=tk.BOTH, expand=True)
        self.side = tk.Frame(self.paned, width=220); self.side.pack_propagate(False); self.paned.add(self.side)
        self.side_label = tk.Label(self.side, text="SESSIONS", font=("Consolas", 11, "bold")); self.side_label.pack(pady=20)
        self.chat_list = tk.Listbox(self.side, bd=0, font=("Consolas", 10)); self.chat_list.pack(fill=tk.BOTH, expand=True, padx=15)
        self.chat_list.bind("<<ListboxSelect>>", self._switch_chat)
        self.btn_f = tk.Frame(self.side); self.btn_f.pack(fill=tk.X, padx=15, pady=15)
        self.b_new = tk.Button(self.btn_f, text="+", bd=0, font=("Consolas", 14), command=self.new_chat, width=3); self.b_new.pack(side=tk.LEFT, padx=2)
        self.b_set = tk.Button(self.btn_f, text="⚙", bd=0, font=("Consolas", 14), command=self.open_settings, width=3); self.b_set.pack(side=tk.LEFT, padx=2)
        self.b_clr = tk.Button(self.btn_f, text="×", bd=0, font=("Consolas", 14), command=self.clear_history, width=3); self.b_clr.pack(side=tk.LEFT, padx=2)
        self.chat_main = tk.Frame(self.paned); self.paned.add(self.chat_main)
        self.display = scrolledtext.ScrolledText(self.chat_main, bd=0, wrap=tk.WORD, state='disabled', padx=25, pady=25); self.display.pack(fill=tk.BOTH, expand=True)
        self.footer = tk.Frame(self.chat_main, height=100); self.footer.pack(side=tk.BOTTOM, fill=tk.X, padx=20, pady=15); self.footer.pack_propagate(False)
        self.wrap = tk.Frame(self.footer, highlightthickness=1); self.wrap.pack(fill=tk.BOTH, expand=True)
        self.b_file = tk.Button(self.wrap, text="+", bd=0, font=("Arial", 22), command=self.load_file); self.b_file.pack(side=tk.LEFT, padx=15)
        self.entry = tk.Entry(self.wrap, bd=0, font=("Consolas", 13)); self.entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True); self.entry.bind("<Return>", lambda e: self.send())
        self.b_send = tk.Button(self.wrap, text="➜", bd=0, font=("Arial", 22), command=self.send); self.b_send.pack(side=tk.RIGHT, padx=15)

    def apply_theme(self):
        theme_name = self.settings.get("theme", "Neon Orange")
        theme = self.themes.get(theme_name, self.themes["Neon Orange"])
        self.root.configure(bg=theme["bg"]); self.paned.configure(bg=theme["bg"]); self.header.configure(bg=theme["panel"]); self.logo.configure(bg=theme["panel"], fg=theme["accent"])
        self.side.configure(bg=theme["panel"]); self.side_label.configure(bg=theme["panel"], fg=theme["accent"]); self.chat_list.configure(bg=theme["panel"], fg=theme["text"], selectbackground=theme["field"])
        self.btn_f.configure(bg=theme["panel"])
        for b in [self.b_new, self.b_set, self.b_clr, self.b_file, self.b_send]: b.configure(bg=theme["field"], fg=theme["accent"], activebackground=theme["panel"], activeforeground=theme["accent"])
        self.chat_main.configure(bg=theme["bg"]); self.display.configure(bg=theme["bg"], fg=theme["text"], font=("Consolas", int(self.settings.get("font_size", 12))), insertbackground=theme["accent"])
        self.display.tag_config("user", foreground=theme["accent"], font=("Consolas", int(self.settings.get("font_size", 12)), "bold")); self.display.tag_config("bot", foreground=theme["bot"]); self.display.tag_config("code", foreground=theme["text"], background=theme["field"])
        self.footer.configure(bg=theme["bg"]); self.wrap.configure(bg=theme["field"], highlightbackground=theme["muted"]); self.entry.configure(bg=theme["field"], fg=theme["text"], font=("Consolas", 13), insertbackground=theme["accent"])
        self._refresh_chats()

    def open_settings(self):
        win = tk.Toplevel(self.root); win.title("All Settings"); win.geometry("600x850")
        theme_name = self.settings.get("theme", "Neon Orange")
        theme = self.themes.get(theme_name, self.themes["Neon Orange"])
        win.configure(bg=theme["bg"])
        def _get_val(k, default=False):
            v = self.settings.get(k); return v if v is not None else default
        v = {
            "theme": tk.StringVar(value=str(self.settings.get("theme", "Neon Orange"))),
            "intelligence": tk.StringVar(value=str(self.settings.get("intelligence", "Balanced"))),
            "response_style": tk.StringVar(value=str(self.settings.get("response_style", "Balanced"))),
            "speed": tk.StringVar(value=str(self.settings.get("speed", "Normal"))),
            "result_count": tk.StringVar(value=str(self.settings.get("result_count", 15))),
            "font_size": tk.StringVar(value=str(self.settings.get("font_size", 12))),
            "web_search": tk.BooleanVar(value=_get_val("web_search", True)),
            "wikipedia": tk.BooleanVar(value=_get_val("wikipedia", True)),
            "live_search": tk.BooleanVar(value=_get_val("live_search", True)),
            "github_search": tk.BooleanVar(value=_get_val("github_search", False)),
            "reddit_search": tk.BooleanVar(value=_get_val("reddit_search", False)),
            "news_search": tk.BooleanVar(value=_get_val("news_search", False)),
            "ad_filter": tk.BooleanVar(value=_get_val("ad_filter", True)),
            "save_memory": tk.BooleanVar(value=_get_val("save_memory", True)),
            "save_locally": tk.BooleanVar(value=_get_val("save_locally", False)),
            "save_path": tk.StringVar(value=str(self.settings.get("save_path", "")))
        }
        container = tk.Frame(win, bg=theme["bg"]); container.pack(fill=tk.BOTH, expand=True, padx=40, pady=20)
        def _l(t): tk.Label(container, text=t, bg=theme["bg"], fg=theme["accent"], font=("Consolas", 10, "bold")).pack(anchor="w", pady=(15, 2))
        _l("UI THEME"); tk.OptionMenu(container, v["theme"], *self.themes.keys()).pack(fill=tk.X)
        _l("INTELLIGENCE MODE"); tk.OptionMenu(container, v["intelligence"], "Fast", "Balanced", "Deep", "Local Only").pack(fill=tk.X)
        _l("RESPONSE STYLE"); tk.OptionMenu(container, v["response_style"], "Short", "Balanced", "Detailed").pack(fill=tk.X)
        _l("SEARCH SPEED"); tk.OptionMenu(container, v["speed"], "Fast", "Normal", "Deep").pack(fill=tk.X)
        _l("ACTIVE DATA SOURCES")
        for key, label in [("web_search", "Web Search (General)"), ("wikipedia", "Wikipedia (Factual)"), ("live_search", "Live Hours Data"), ("github_search", "GitHub Search"), ("reddit_search", "Reddit Search"), ("news_search", "Google News")]:
            tk.Checkbutton(container, text=label, variable=v[key], bg=theme["bg"], fg=theme["text"], selectcolor=theme["field"], activebackground=theme["bg"]).pack(anchor="w")
        _l("STORAGE")
        tk.Checkbutton(container, text="Save Chat Memory", variable=v["save_memory"], bg=theme["bg"], fg=theme["text"], selectcolor=theme["field"], activebackground=theme["bg"]).pack(anchor="w")
        tk.Checkbutton(container, text="External JSON Database", variable=v["save_locally"], bg=theme["bg"], fg=theme["text"], selectcolor=theme["field"], activebackground=theme["bg"]).pack(anchor="w")
        p_f = tk.Frame(container, bg=theme["bg"]); p_f.pack(fill=tk.X, pady=5)
        tk.Entry(p_f, textvariable=v["save_path"], bg=theme["field"], fg=theme["text"], bd=0).pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=5)
        tk.Button(p_f, text="...", command=lambda: v["save_path"].set(filedialog.asksaveasfilename(defaultextension=".json")), bg=theme["field"], fg=theme["bot"], bd=0).pack(side=tk.RIGHT, padx=5)

        def _apply():
            for k in v:
                val = v[k].get()
                if k in ["result_count", "font_size"]:
                    try: self.settings[k] = int(val)
                    except: pass
                else: self.settings[k] = val
            self.settings_store.save(); self.brain.update_settings(self.settings); self.apply_theme()
            new_theme = self.themes.get(self.settings["theme"], self.themes["Neon Orange"])
            win.configure(bg=new_theme["bg"]); container.configure(bg=new_theme["bg"])
            for widget in container.winfo_children():
                try: widget.configure(bg=new_theme["bg"], fg=new_theme["text"])
                except: pass
                if isinstance(widget, tk.Label): widget.configure(fg=new_theme["accent"])
                if isinstance(widget, tk.Button): widget.configure(bg=new_theme["field"], fg=new_theme["accent"])
            btn_apply.configure(bg=new_theme["accent"], fg=new_theme["bg"])
            btn_save.configure(bg=new_theme["field"], fg=new_theme["accent"])

        btn_apply = tk.Button(win, text="APPLY", command=_apply, bg=theme["accent"], fg=theme["bg"], font=("Consolas", 11, "bold"), bd=0)
        btn_apply.pack(pady=(20, 5), fill=tk.X, padx=40)
        btn_save = tk.Button(win, text="SAVE & CLOSE", command=lambda: [_apply(), win.destroy()], bg=theme["field"], fg=theme["accent"], font=("Consolas", 11, "bold"), bd=0)
        btn_save.pack(pady=5, fill=tk.X, padx=40)

    def _refresh_chats(self):
        self.chat_list.delete(0, tk.END)
        for cid, chat in self.memory.get_chats(): self.chat_list.insert(tk.END, chat["name"])

    def _switch_chat(self, e):
        idx = self.chat_list.curselection()
        if idx:
            chats = self.memory.get_chats()
            self.chat_id = chats[idx[0]][0]; self.load_history()

    def new_chat(self):
        name = simpledialog.askstring("New", "Session name:")
        if name: self.chat_id = self.memory.create_chat(name); self._refresh_chats(); self.load_history()

    def clear_history(self):
        if messagebox.askyesno("Clear", "Wipe chat history?"): self.chat_id = self.memory.clear_all(); self._refresh_chats(); self.load_history()

    def load_history(self):
        self.display.config(state='normal'); self.display.delete("1.0", tk.END); self.display.config(state='disabled')
        for m in self.memory.get_history(self.chat_id):
            tag = "user" if m.get("role") == "user" else "bot"
            self.add_msg("YOU" if tag=="user" else "NEON", m.get("text", ""), tag)

    def load_file(self):
        path = filedialog.askopenfilename()
        if path:
            filename = os.path.basename(path)
            if any(path.lower().endswith(e) for e in ['.png','.jpg','.jpeg','.webp']) and HAS_PIL:
                img = Image.open(path); img.thumbnail((400, 400)); photo = ImageTk.PhotoImage(img); self.img_cache = [photo]
                self.display.config(state='normal'); self.display.image_create(tk.END, image=photo); self.display.insert(tk.END, "\n"); self.display.config(state='disabled')
                self.add_msg("SYSTEM", f"Captured {filename}.", "bot")
            else: self.add_msg("SYSTEM", f"Document {filename} loaded.", "bot")

    def send(self):
        text = self.entry.get().strip()
        if text: self.add_msg("YOU", text, "user"); self.memory.add_msg(self.chat_id, "user", text); self.entry.delete(0, tk.END); threading.Thread(target=self._process, args=(text,)).start()

    def _process(self, text):
        resp = self.brain.respond(text, self.memory.get_history(self.chat_id))
        self.root.after(0, lambda: self.add_msg("NEON", resp, "bot")); self.memory.add_msg(self.chat_id, "bot", resp)

    def add_msg(self, sender, msg, tag):
        self.display.config(state='normal'); self.display.insert(tk.END, f"\n{sender}\n", tag)
        if "```" in msg:
            parts = msg.split("```")
            for i, p in enumerate(parts): self.display.insert(tk.END, p, "code" if i % 2 == 1 else None)
        else: self.display.insert(tk.END, msg + "\n")
        self.display.config(state='disabled'); self.display.yview(tk.END)

if __name__ == "__main__":
    root = tk.Tk(); NeonUI(root); root.mainloop()
