[🇺🇸 English](./README.md) &nbsp;|&nbsp;
[🇨🇳 中文](./README_zh.md) &nbsp;|&nbsp;
[🇯🇵 日本語](./README_ja.md) &nbsp;|&nbsp;
[🇰🇷 한국어](./README_ko.md)

---

# 🤖 Desktop Pet

**A tiny interactive pixel robot living on your desktop.**

Hangs out on top of your windows. Gets hungry. Falls asleep. Wanders around. Occasionally blinks at you with pixel-perfect indifference.

---

## What it does

- Sits on your screen as a transparent, always-on-top window — no chrome, no title bar, just the robot
- Has actual needs: hunger decays, energy drains, happiness fades if you ignore it
- Roams on its own when it's bored (idle → walk auto-transition)
- Asks for nothing — but if you click it, it sparkles

## Features

- **7 pixel animations** — idle (blink), idle-sad, idle-happy, walk, sleep (lying down + ZZZ), eat, happy (sparkle eyes)
- **Mood-aware idle** — changes expression based on happiness: sad (<30), normal, sparkle-eyed (>70)
- **FSM-driven behavior** — clean state machine with defined transitions
- **System tray** — lives in your tray until you need it
- **4-language UI** — Chinese / English / Japanese / Korean, switchable in settings
- **Attribute system** — hunger / happiness / energy decay over time; passive coin income
- **In-game shop** — spend coins on food to restore attributes
- **Offline persistence** — auto-saves every 5 minutes, compensates for time away
- **Click interaction** — single click → +5 happiness + happy animation, double click → +10
- **Drag to move** — just grab it and drop it anywhere
- **Transparency mask** — click-through on empty pixels, so it doesn't eat your clicks

## Screenshots

<!-- TODO: add screenshots / gifs -->

*Coming soon — PRs welcome if you grab one first.*

## Quick start

```bash
git clone git@github.com:jiangziyong3-lgtm/desktop-pet.git
cd desktop-pet

python -m venv venv
source venv/bin/activate   # or `venv\Scripts\activate` on Windows

pip install -r requirements.txt
python main.py
```

**Requires:** Python 3.9+, PySide6 ≥ 6.5.0

## Project layout

```
main.py              → entry point + language init
pet_window.py        → transparent window, drag, context menu, status panel
state_machine.py     → finite state machine
animator.py          → frame player (loop / one-shot)
renderer.py          → per-pixel renderer with horizontal flip
sprites.py           → 16×16 sprite data (palette-indexed, 7 animations)
attributes.py        → attribute decay, coin income, critical thresholds
save_manager.py      → JSON save + offline compensation
tray.py              → system tray icon & menu
config.py            → all tunable knobs + gift codes
i18n.py              → translation system (zh / en / ja / ko)
settings_window.py   → settings dialog (language + gift code)
states/              → state behaviors (idle, walk, sleep, eat, happy, drag)
shop/                → shop ui & item definitions
```

## License

MIT — do whatever, just don't be mean to the robot.
