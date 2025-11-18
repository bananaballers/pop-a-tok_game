

# **The Ballgame of Xibalba — README**

Hey @MMMMBanana and John go to [this](#-future-improvements-optional-ideas) link to see the to-do list!


## 📜 Overview

**The Ballgame of Xibalba** is an interactive text-adventure game based on the Mayan myth of the Hero Twins: **Hunahpu** and **Xbalanque**.
The player navigates trials, chooses their actions, and tries to outsmart the Lords of the Underworld.

The game features:

* Dynamic text-speed settings
* A built-in developer mode
* Randomized option ordering
* Multiple stages and endings
* Replayability with reset logic

---

## 🚀 How to Run

### **1. Requirements**

* Python 3 (any modern version)
* Terminal / command line

### **2. Run the game**

```bash
python3 xibalba.py
```

The game will immediately ask you to choose a **text speed** before beginning.

---

## ⚙️ Text Speed System

Whenever the game starts (or restarts after a Game Over), the player is prompted:

```
Choose text speed:
  [1] Slow (0.03)
  [2] Fast (0.003)
  [3] Instant (0)
```

This sets the global variable:

```python
TEXT_SPEED
```

All narrative text uses:

```python
print_slow("...", delay=TEXT_SPEED)
```

This keeps gameplay customizable and consistent across scenes.

---

## 🧪 Developer Mode (Auto-Play)

There is a hidden dev mode for debugging the full story quickly.

### **How to activate**

At the **very first prompt** (“Press ENTER to continue”), type:

```
dev
```

You will see:

```
DEV MODE ACTIVATED! The game will now play itself.
```

### **What it does**

* Automatically selects the **correct** option in every choice
* Skips pauses automatically
* Finishes the game quickly for testing

This allows you to test win/lose paths without manual input.

---

## 🎲 Choice Randomization

To prevent players from memorizing “Option 2 is always correct,” each set of options is **shuffled** before being printed.

**Internally**, choices still use their original keys (like `"1"` or `"2"`), so story logic stays consistent.

Mapping works like:

* Display random order (1,2,3,4…)
* Map UI numbers → original keys
* Return original key to the story logic

This makes the game replayable and harder to brute-force.

---

## 🧩 Game Structure (Scene Flow)

Here is the high-level structure of all scenes:

```
start()
  └─ crossroads()
      └─ throne_room()
          └─ house_of_gloom()
              └─ house_of_cold()
                  └─ house_of_jaguars()
                      └─ ballgame()
                          └─ finale()
                              └─ victory()
```

Failure at any point triggers:

```
game_over_screen()
   └─ Restart or Quit
```

Restarting resets:

* Inventory
* Text speed choice
* Dev mode stays disabled unless reactivated

---

## 📦 Inventory System

The list:

```python
inventory = []
```

Items are added and can be expanded (only one is used currently):

* `"Secret Names"` — used to pass the first trial

Future ideas:

* More items
* Branching paths using inventory states

---

## 🔧 File Layout

Everything is contained in **one Python file**:

```
xibalba.py
```

Inside the file:

* Global configuration
* Utility functions (printing, choosing, pausing)
* Scene functions
* Game-over logic
* Entry point at the bottom:

  ```python
  start()
  ```

---

# ✨ Future Improvements (Optional Ideas)

These can be added by any dev:
* **A better UI for Mr. B and users (leave the terminal)**
* Colorized output using ANSI escape codes
* Save/load system
* Multiple difficulty modes
* Branching endings
* Sound effects using `winsound` or `playsound`
* Scoreboard / statistics
* Modular scene files

If you'd like, I can scaffold any of these.

---

## 👥 For Developers

The code is designed to be:

* Readable
* Easily moddable
* Single-file for simplicity
* Friendly for new contributors

If adding scenes, just follow the pattern:

```python
def my_scene():
    clear_screen()
    print("...")
    options = { "1": "...", "2": "..." }
    choice = get_choice(options)
```

Then call `pause()` and send the player to the next scene.

