# 🌈 N30N C0R3 AI - 7-Color ASCII v2.0

> One-file local AI with 7-color ASCII art generation, saved chats, knowledge base, reminders, todo lists, and a full settings panel.

```
███╗   ██╗██████╗  ██████╗ ███╗   ██╗     ██████╗ ██████╗ ██████╗ ██████╗
████╗  ██║╚════██╗██╔═══██╗████╗  ██║    ██╔════╝██╔═══██╗██╔══██╗██╔════╝
██╔██╗ ██║ █████╔╝██║   ██║██╔██╗ ██║    ██║     ██║   ██║██████╔╝█████╗  
██║╚██╗██║ ╚═══██╗██║   ██║██║╚██╗██║    ██║     ██║   ██║██╔══██╗██╔══╝  
██║ ╚████║██████╔╝╚██████╔╝██║ ╚████║    ╚██████╗╚██████╔╝██║  ██║███████╗
╚═╝  ╚═══╝╚═════╝  ╚═════╝ ╚═╝  ╚═══╝     ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝
                                                                          
                                  █████╗ ██╗                              
                                 ██╔══██╗██║                              
                                 ███████║██║                              
                                 ██╔══██║██║                              
                                 ██║  ██║██║                              
                                 ╚═╝  ╚═╝╚═╝                              
```

## Run

```bash
python3 ai.py
```

## Main Features

| Feature | What It Does |
|---|---|
| 7-Color ASCII Art | Generate rainbow-colored ASCII art with markers §0‑§6 (Red, Orange, Yellow, Green, Blue, Indigo, Violet) |
| Pattern Generation | Create diamond, spiral, checker, waves, grid, circle, triangle, star, rainbow, and gradient patterns |
| Knowledge Base | Built-in encyclopedia with 60+ topics (science, technology, space, biology, etc.) |
| Persistent Memory | Chat history and settings are safe-saved using Base64 encoding |
| Reminders | Set timed reminders with threading support |
| Todo Lists | Add, remove, and list tasks |
| Notes | Save and retrieve quick notes |
| Fun Features | Jokes, quotes, lyrics, poems, stories, and battle comparisons |
| Math & Conversion | Safe math evaluation and unit conversions (length, weight, temperature, distance) |
| Themes | 12 color themes including Neon variants, Soft Night, Retro Terminal, and Matrix |
| Settings Panel | Full control over theme, font size, ASCII style, personality, and more |
| External Storage | Option to save chat database to an external JSON file |
| Image to ASCII | Convert images to 7-color ASCII art (requires Pillow) |
| Import/Export | Export chats to JSON/TXT and import from JSON |
| Smart Context | Tracks conversation topics and user preferences |

## Brain Powers

| Skill | Example |
|---|---|
| Identity | `who are you` |
| ASCII Art | `ascii NEON` or press 🌈 button |
| Patterns | `show me a diamond pattern` |
| Deep Facts | `what is quantum entanglement` |
| Math | `sqrt(144) * (25 / 5)` |
| Conversion | `10 cm to inch`, `30 c to f` |
| Reminders | `remind me to call mom in 5 minutes` |
| Todo | `add task buy groceries`, `remove 1`, `list` |
| Notes | `save note my password is...`, `show notes` |
| Fun | `tell me a joke`, `give me a quote` |
| Lyrics | `sing imagine` |
| Poems | `poem roses` |
| Stories | `tell me a story about ai` |
| Battles | `Goku vs Superman` |
| Dice | `roll d20` |
| Coin | `flip coin` |
| Password | `generate password 16` |

## Settings

Open **⚙ Settings** from the top toolbar.

| Setting | Options |
|---|---|
| UI Theme | Neon Orange, Pink, Green, Blue, Red, Purple, Yellow, Soft Night (Green/Blue/Purple), Retro Terminal, Matrix |
| Font Size | 8-24 |
| ASCII Style | block, shade, diagonal, dots, numbers |
| ASCII Width | 20-200 |
| Personality | friendly, witty, sarcastic, professional, philosophical |
| Response Style | concise, detailed, comprehensive |
| Creative Mode | Toggle |
| Auto-save chat | Toggle |
| Show timestamps | Toggle |
| Enable reminders | Toggle |
| Auto-clear display | Toggle |
| Humor Level | 0-100 slider |
| Verbosity | 0-100 slider |
| Export Format | json, txt |

## Themes

| Style | Names | Description |
|---|---|---|
| **Neon** | Orange, Pink, Green, Blue, Red, Purple, Yellow | Vibrant, high-contrast cyberpunk aesthetics. |
| **Soft Night** | Green, Blue, Purple | Eye-friendly, low-light optimized charcoal themes. |
| **Retro** | Retro Terminal, Matrix | Classic terminal aesthetics with green/cyan text. |

## Safe Storage

The AI uses **Base64 Encoding** to store data inside `ai.py` to prevent Python syntax errors:

```python
# NEON_HISTORY_START
NEON_HISTORY_B64 = '...'
# NEON_HISTORY_END
```

## Commands

Slash commands available in the chat:
- `/help` - Show help dialog
- `/clear` - Clear current display
- `/new [name]` - Create new session
- `/delete [number]` - Delete session by number
- `/rename [number] [name]` - Rename session
- `/export` - Export current chat to JSON
- `/load` - Import chat from JSON
- `/exit` - Quit application

## Optional Image Support

```bash
pip install pillow
```

Supported formats: `.png`, `.jpg`, `.jpeg`, `.webp`

---

**🌈 N30N C0R3 AI v2.0** is your advanced local intelligence hub with 7-color ASCII art generation, combining creativity with knowledge. No external models, no cloud, just raw code and built-in intelligence.