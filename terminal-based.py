import time
import os
import sys
import random

# Global variable to track items collected
inventory = []

# Global variable for development mode
DEV_MODE = False 
dev_key = "dev"

# Global text speed
TEXT_SPEED = 0.003


def clear_screen():
    """Clears the console screen for a fresh view."""
    os.system('cls' if os.name == 'nt' else 'clear')


def choose_speed():
    """Ask the user for the text speed every game start."""
    global TEXT_SPEED

    print("\nChoose text speed:")
    print("  [1] Slow (0.03)")
    print("  [2] Fast (0.003)")
    print("  [3] Instant (0)")

    while True:
        choice = input("> ").strip()
        if choice == "1":
            TEXT_SPEED = 0.03
            break
        elif choice == "2":
            TEXT_SPEED = 0.003
            break
        elif choice == "3":
            TEXT_SPEED = 0
            break
        else:
            print("Not understood. Choose 1, 2, or 3.")


def print_slow(text, delay=None):
    """Types out text using selected speed unless overridden."""
    if delay is None:
        delay = TEXT_SPEED

    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print("\n")


def pause():
    """Waits for user input to proceed."""
    print("\n")
    global DEV_MODE
    if DEV_MODE:
        print(">> DEV MODE: Skipping pause...")
        time.sleep(0.5)
    else:
        input(">> Press ENTER to continue...")
    print("\n")


def get_choice(options):
    """
    Handles user input safely.
    Scrambles the display order so '2' isn't always the answer.
    """
    global DEV_MODE
    
    original_keys = list(options.keys())
    winning_key = original_keys[1] if len(original_keys) > 1 else original_keys[0]

    display_items = list(options.items())
    random.shuffle(display_items)
    
    ui_map = {}
    
    print("What will you do?")
    for index, (orig_key, description) in enumerate(display_items):
        ui_num = str(index + 1)
        ui_map[ui_num] = orig_key
        print(f"  [{ui_num}] {description}")

    if DEV_MODE:
        target_ui = next(u for u, k in ui_map.items() if k == winning_key)
        print(f"\n(DEV MODE: Auto-choosing '{options[winning_key]}')")
        print(f"> {target_ui}")
        time.sleep(0.5)
        return winning_key

    while True:
        choice = input("\n> ").strip()
        
        if choice in ui_map:
            return ui_map[choice]
        else:
            print("I did not understand that. Please type the number of your choice.")


# --- SCENES ---

def start():
    global inventory
    inventory = []

    clear_screen()
    choose_speed()  # <-- NEW: ask speed every game

    print("="*60)
    print("       T H E   B A L L G A M E   O F   X I B A L B A")
    print("="*60)
    print("\n")
    print_slow("Many years ago, the First Twins played ball too loudly.")
    print_slow("The Lords of the Underworld (Xibalba) were annoyed.")
    print_slow("The First Twins failed the tests and were defeated.")
    print("\n")
    print_slow("Now, YOU are the New Twins: Hunahpu and Xbalanque.")
    print_slow("You have accepted the challenge to restore honor to your family.")
    
    global DEV_MODE
    print("\n")
    initial_input = input(">> Press ENTER to continue: ").strip().lower()
    if initial_input == dev_key:
        DEV_MODE = True
        print_slow("\nDEV MODE ACTIVATED! The game will now play itself.")
        time.sleep(1)
    print("\n")
    
    crossroads()


def crossroads():
    clear_screen()
    print("--- THE CROSSROADS ---")
    print("You descend deep into the earth. You arrive at four paths:")
    print("Red, White, Yellow, and Black.")
    print("\nThe Lords are hiding. A mosquito named Xan buzzes near your ear.")
    print("\n")

    options = {
        "1": "Walk the Black Path alone",
        "2": "Send Xan the Mosquito ahead to scout",
        "3": "Walk the White Path alone",
        "4": "Walk the Yellow Path alone",
        "5": "Walk the Red Path alone"
    }
    choice = get_choice(options)

    if choice == "1":
        print_slow("You walk into the dark. The Lords trick you immediately!")
        game_over_screen("You were lost in the dark.")
    else:
        print_slow("Smart choice. Xan flies ahead.")
        print_slow("Xan bites the wooden dummies. They are silent.")
        print_slow("Xan bites the REAL Lords. They yell 'Ouch!' revealing their names.")
        inventory.append("Secret Names")
        pause()
        throne_room()


def throne_room():
    clear_screen()
    print("--- THE GREETING ---")
    print("You enter the court knowing the Lords' names.")
    print("They look surprised, but they smile wickedly.")
    print("\nThey point to a large, beautiful stone bench.")
    print("'Welcome, Twins! Please, rest on our throne of honor.'")
    print("\n")

    options = {
        "1": "Sit on the Throne",
        "2": "Sit on the Floor"
    }
    choice = get_choice(options)

    if choice == "1":
        print_slow("AAAAH! The stone is boiling hot!")
        game_over_screen("You were burned and cannot play.")
    else:
        print_slow("You politely decline: 'This seat is too good for us.'")
        print_slow("You sit on the cool floor.")
        print_slow("The Lords scowl. You have passed the first test.")
        pause()
        house_of_gloom()


def house_of_gloom():
    clear_screen()
    print("--- THE HOUSE OF GLOOM ---")
    print("The Lords hand you a lit torch and a cigar.")
    print("'Keep this light burning all night,' they say.")
    print("'But return it tomorrow UNUSED.'")
    print("\nIt is a paradox. How do you keep fire without burning the wood?")
    print("\n")

    options = {
        "1": "Let the torch burn normally",
        "2": "Swap the flame for red Macaw feathers"
    }
    choice = get_choice(options)

    if choice == "1":
        print_slow("The torch turns to ash by morning.")
        game_over_screen("The Lords execute you for failing the task.")
    else:
        print_slow("Brilliant!")
        print_slow("From a distance, the red feathers look like fire.")
        print_slow("In the morning, you return the torch unburned.")
        pause()
        house_of_cold()


def house_of_cold():
    clear_screen()
    print("--- THE HOUSE OF COLD ---")
    print("The Lords are frustrated. They shove you into the next room.")
    print("It is freezing! Thick ice coats the walls and hail falls constantly.")
    print("You cannot sleep or you will freeze.")
    print("\n")

    options = {
        "1": "Huddle together for warmth",
        "2": "Burn old pinecones found on the floor"
    }
    choice = get_choice(options)

    if choice == "1":
        print_slow("It is not enough. The magical cold freezes you solid.")
        game_over_screen("You froze in the House of Cold.")
    else:
        print_slow("You gather the dry pinecones and light a small fire.")
        print_slow("The warmth keeps you alive through the freezing night.")
        print_slow("In the morning, the Lords are shocked to see you healthy.")
        pause()
        house_of_jaguars()


def house_of_jaguars():
    clear_screen()
    print("--- THE HOUSE OF JAGUARS ---")
    print("The Lords are running out of patience.")
    print("They throw you into a stone room filled with hungry Jaguars!")
    print("The beasts roar and circle you, licking their chops.")
    print("\n")

    options = {
        "1": "Fight them with your knife",
        "2": "Throw bones to distract them"
    }
    choice = get_choice(options)

    if choice == "1":
        print_slow("There are too many! You fight bravely, but you are overwhelmed.")
        game_over_screen("The Jaguars enjoyed their meal.")
    else:
        print_slow("You throw the dry bones into the corners of the room.")
        print_slow("The Jaguars chase the bones and gnaw on them happily.")
        print_slow("They wrestle over the bones and ignore you all night.")
        pause()
        ballgame()


def ballgame():
    clear_screen()
    print("--- THE TLACHTLI COURT ---")
    print("You have survived all the Houses. Now, the sport begins.")
    print("The heavy rubber ball bounces on the stone court.")
    print("The Lords serve the ball to you.")
    print("\n")

    score = 0
    rounds = 0
    
    while rounds < 3:
        print(f"ROUND {rounds + 1} | SCORE: {score}")
        options = {
            "1": "High Lob",
            "2": "Hip Strike (Solid)",
            "3": "Low Slide"
        }
        choice = get_choice(options)

        if choice == "2":
            print("\n>> SMACK! A perfect hit off the hip. You score!\n")
            score += 1
        elif choice == "1":
            print("\n>> Too high! The Lords smash it back easily.\n")
        else:
            print("\n>> Too low! You scrape your knee on the stone.\n")
        
        rounds += 1
        time.sleep(1)

    if score >= 1:
        print_slow("The Lords are furious that you are winning.")
        print_slow("They cheat and throw the ball into the House of Fire.")
        pause()
        finale()
    else:
        game_over_screen("The Lords defeated you in the game.")


def finale():
    clear_screen()
    print("--- THE GRAND TRICK ---")
    print("The Twins realize they cannot win by normal rules.")
    print("You allow yourselves to be burned, but then you return!")
    print("\nYou perform miracles, bringing things back to life.")
    print("The Lords are amazed. 'Burn us!' they command. 'Make us young again!'")
    print("\n")

    options = {
        "1": "Burn them and REVIVE them",
        "2": "Burn them and DO NOT revive them"
    }
    choice = get_choice(options)

    if choice == "1":
        print_slow("You revive the evil Lords. They thank you... by eating you.")
        game_over_screen("You were too merciful.")
    else:
        victory()


def victory():
    clear_screen()
    print("\n" + "*"*60)
    print("                   V I C T O R Y !")
    print("*"*60 + "\n")
    print_slow("The Lords turn to ash and blow away in the wind.")
    print_slow("Xibalba is defeated.")
    print_slow("Hunahpu and Xbalanque rise into the sky.")
    print("\nThey become the SUN and the MOON.")
    print("\nCongratulations! You have completed the story.")
    input("\nPress Enter to exit.")
    sys.exit()


def game_over_screen(reason):
    print("\n" + "-"*40)
    print("G A M E   O V E R")
    print(f"Reason: {reason}")
    print("-"*40 + "\n")
    
    options = {"1": "Try Again", "2": "Quit"}
    choice = get_choice(options)
    
    if choice == "1":
        choose_speed()  # <-- ASK SPEED AGAIN ON RESTART
        start()
    else:
        print("Goodbye.")
        sys.exit()


# Start the whole thing
start()
