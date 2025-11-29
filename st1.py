import base64
import streamlit as st
import random
import time
import os
import streamlit.components.v1 as components

# Configure page settings for a better game feel
st.set_page_config(
    page_title="Popol Vuh: The Ballgame",
    page_icon="☀️",
    layout="wide"
)

#####################
# Helper/Init functions
#####################

def render_scene_media(scene_name, container=st):
    """
    Checks for a folder named after the scene and renders media files 
    into the specified container (e.g., a column).
    """
    if os.path.exists(scene_name) and os.path.isdir(scene_name):
        # Get all files in the directory
        files = sorted(os.listdir(scene_name))
        
        for file in files:
            file_path = os.path.join(scene_name, file)
            
            # Check extensions and render accordingly
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                container.image(file_path, use_container_width=True)
            elif file.lower().endswith(('.mp4', '.mov', '.webm')):
                container.video(file_path)
            elif file.lower().endswith(('.mp3', '.wav', '.ogg')):
                # Read audio file and convert to base64
                with open(file_path, 'rb') as audio_file:
                    audio_bytes = audio_file.read()
                    audio_base64 = base64.b64encode(audio_bytes).decode()
    
                # Determine MIME type
                ext = file.lower().split('.')[-1]
                mime_types = {'mp3': 'audio/mpeg', 'wav': 'audio/wav', 'ogg': 'audio/ogg'}
                mime = mime_types.get(ext, 'audio/mpeg')
    
                # Inject hidden autoplay audio
                audio_html = f"""
                    <audio autoplay loop style="display:none;">
                        <source src="data:{mime};base64,{audio_base64}" type="{mime}">
                    </audio>
                """
                st.markdown(audio_html, unsafe_allow_html=True)

def initialize_state():
    if "scene" not in st.session_state:
        st.session_state.scene = "start"
    if "inventory" not in st.session_state:
        st.session_state.inventory = []
    if "score" not in st.session_state:
        st.session_state.score = 0
    if "rounds" not in st.session_state:
        st.session_state.rounds = 0
    if "game_over_reason" not in st.session_state:
        st.session_state.game_over_reason = ""

def reset_for_restart():
    st.session_state.inventory = []
    st.session_state.score = 0
    st.session_state.rounds = 0
    st.session_state.game_over_reason = ""

def show_hud():
    """Displays a persistent Heads-Up Display in the sidebar."""
    with st.sidebar:
        st.header("🎒 Hero Status")
        st.divider()

        # Score / Inventory display
        st.metric("Ballgame Score", st.session_state.score)

        st.subheader("Inventory")
        if st.session_state.inventory:
            for item in st.session_state.inventory:
                st.success(f"✨ {item}")
        else:
            st.caption("Your inventory is empty.")

        st.divider()
        if st.button("🔄 Restart Game"):
            reset_for_restart()
            st.session_state.scene = "start"
            st.rerun()

#####################
# Scenes
#####################

def start():
    # Layout: Text Left (2), Image Right (1)
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("<h1 style='text-align: left;'>☀️ Popol Vuh 🌑</h1>", unsafe_allow_html=True)
        st.markdown("<h3>The Ballgame of the Gods</h3>", unsafe_allow_html=True)
        st.divider()

        st.info("Many years ago, the First Twins played ball too loudly. The Lords of Xibalbadefeated them.")
        st.write("Now, **YOU** are the New Twins: **Hunahpu** and **Xbalanque**.")
        st.write("You have accepted the challenge to restore honor to your family.")

        st.write("")
        if st.button("Begin Adventure", type="primary", use_container_width=True):
            st.session_state.scene = "crossroads"
            st.rerun()

    with col2:
        render_scene_media("start", container=col2)

def crossroads():
    st.progress(10, text="The Journey Begins")
    st.header("The Crossroads")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.write("You descend deep into the earth. You arrive at four paths: Red, White, Yellow, and Black.")
        st.write("The Lords are hiding. A mosquito named **Xan** buzzes near your ear.")

        options = {
            "1": "Walk the Black Path alone",
            "2": "Send Xan the Mosquito ahead to scout",
            "3": "Walk the White Path alone",
            "4": "Walk the Yellow Path alone",
            "5": "Walk the Red Path alone"
        }

        items = list(options.items())
        display_values = [desc for key, desc in items]

        choice = st.radio("What will you do?", display_values)

        if st.button("Make Choice", type="primary"):
            selected_key = next(key for key, desc in items if desc == choice)

            if selected_key == "1":
                st.session_state.game_over_reason = "You walked into the dark. The Lords tricked you immediately!"
                st.session_state.scene = "game_over"
                st.rerun()
            elif selected_key == "2":
                st.toast("Success! Xan helped you.")
                st.session_state.inventory.append("Secret Names")
                st.session_state.scene = "throne_room"
                st.rerun()
            else:
                st.session_state.game_over_reason = "You took the wrong path and got lost forever."
                st.session_state.scene = "game_over"
                st.rerun()
                
    with col2:
        render_scene_media("crossroads", container=col2)

def throne_room():
    st.progress(25, text="The Greeting")
    st.header("The Throne Room")
    
    col1, col2 = st.columns([2, 1])

    with col1:
        st.write("You enter the court knowing the Lords' names. They look surprised, but smile wickedly.")
        st.warning("They point to a large, beautiful stone bench. 'Welcome, Twins! Please, rest on our throne of honor.'")

        options = {"1": "Sit on the Throne", "2": "Sit on the Floor"}
        items = list(options.items())
        display_values = [desc for key, desc in items]

        choice = st.radio("Where will you sit?", display_values)

        if st.button("Confirm"):
            selected_key = next(key for key, desc in items if desc == choice)

            if selected_key == "1":
                st.session_state.game_over_reason = "The stone was boiling hot! You were burned."
                st.session_state.scene = "game_over"
                st.rerun()
            else:
                st.toast("Wise choice.")
                st.session_state.scene = "house_of_gloom"
                st.rerun()

    with col2:
        render_scene_media("throne_room", container=col2)

def house_of_gloom():
    st.progress(40, text="House of Gloom")
    st.header("The House of Gloom")
    
    col1, col2 = st.columns([2, 1])

    with col1:
        st.write("The Lords hand you a lit torch and a cigar.")
        st.info("'Keep this light burning all night,' they say. 'But return it tomorrow UNUSED.'")
        st.write("It is a paradox. How do you keep fire without burning the wood?")

        options = {"1": "Let the torch burn normally", "2": "Swap flame for red Macaw feathers"}
        items = list(options.items())
        display_values = [desc for key, desc in items]

        choice = st.radio("Solution:", display_values)

        if st.button("Proceed"):
            selected_key = next(key for key, desc in items if desc == choice)
            if selected_key == "1":
                st.session_state.game_over_reason = "The torch turned to ash. The Lords executed you."
                st.session_state.scene = "game_over"
                st.rerun()
            else:
                st.toast("Brilliant trickery!")
                st.session_state.scene = "house_of_cold"
                st.rerun()

    with col2:
        render_scene_media("house_of_gloom", container=col2)

def house_of_cold():
    st.progress(55, text="House of Cold")
    st.header("The House of Cold")
    
    col1, col2 = st.columns([2, 1])

    with col1:
        st.write("It is freezing! Thick ice coats the walls and hail falls constantly.")
        st.write("You cannot sleep or you will freeze.")

        options = {"1": "Huddle together", "2": "Burn old pinecones"}
        items = list(options.items())
        display_values = [desc for key, desc in items]

        choice = st.radio("Survival Strategy:", display_values)

        if st.button("Act"):
            selected_key = next(key for key, desc in items if desc == choice)
            if selected_key == "1":
                st.session_state.game_over_reason = "Body heat wasn't enough. You froze solid."
                st.session_state.scene = "game_over"
                st.rerun()
            else:
                st.toast("The fire saved you.")
                st.session_state.scene = "house_of_jaguars"
                st.rerun()

    with col2:
        render_scene_media("house_of_cold", container=col2)

def house_of_jaguars():
    st.progress(70, text="House of Jaguars")
    st.header("The House of Jaguars")
    
    col1, col2 = st.columns([2, 1])

    with col1:
        st.error("The Lords throw you into a room filled with hungry Jaguars! They circle you.")

        options = {"1": "Fight with knife", "2": "Distract with bones"}
        items = list(options.items())
        display_values = [desc for key, desc in items]

        choice = st.radio("Action:", display_values)

        if st.button("Execute"):
            selected_key = next(key for key, desc in items if desc == choice)
            if selected_key == "1":
                st.session_state.game_over_reason = "There were too many jaguars to fight."
                st.session_state.scene = "game_over"
                st.rerun()
            else:
                st.toast("The jaguars are happy with the bones.")
                st.session_state.scene = "ballgame"
                st.rerun()

    with col2:
        render_scene_media("house_of_jaguars", container=col2)

def ballgame():
    st.header("THE TLACHTLI COURT")
    
    # Game is wide, so we use equal columns or give the game more space if needed.
    # Using [1, 1.5] to give the visual game a bit more room on the right.
    col1, col2 = st.columns([1, 1.5])

    with col1:
        st.write("The Lords of Xibalba sneer at you.")
        st.write("'We will not play with mere words,' they shout.")
        st.warning("'Prove your skill on the VISUAL COURT!'")

        st.markdown("""
        **INSTRUCTIONS:**
        1. Play the game to the right.
        2. Defeat the Computer (Warrior 1 vs AI).
        3. Win 3 points to get the **Sacred Code**.
        4. Enter the code below to survive.
        """)
        
        st.write("---")
        code_input = st.text_input("Enter the SACRED CODE here:")

        if st.button("Verify Sacred Code"):
            if not code_input:
                st.warning("You must enter a code.")
            elif code_input.startswith("TLACHTLI") and "P1" in code_input:
                st.balloons()
                st.success(f"ACCEPTED: {code_input}")
                st.write("The Lords recoil in shock! You have defeated them on the court!")
                time.sleep(2)
                st.session_state.scene = "finale"
                st.rerun()
            elif "P2" in code_input:
                st.error("The code turns red and crumbles. The Lords defeated you.")
                st.session_state.death_reason = "Lost the ballgame."
                st.session_state.scene = "game_over"
                st.rerun()
            else:
                st.error("The Lords laugh. 'That is not a valid code!'")

    with col2:
        # Load and Display the HTML Game (Iframe)
        # We also check for any static media in the ballgame folder
        render_scene_media("ballgame", container=col2)
        
        try:
            with open("game.html", "r", encoding="utf-8") as f:
                html_code = f.read()
            components.html(html_code, height=600, width=None, scrolling=False)
        except FileNotFoundError:
            st.error("Error: 'game.html' not found.")

def finale():
    st.progress(95, text="The Grand Trick")
    st.header("The Grand Trick")
    
    col1, col2 = st.columns([2, 1])

    with col1:
        st.write("You perform miracles, bringing things back to life. The Lords are amazed.")
        st.info("'Burn us!' they command. 'Make us young again!'")

        options = {"1": "Burn them and REVIVE them", "2": "Burn them and DO NOT revive them"}
        items = list(options.items())
        display_values = [desc for key, desc in items]

        choice = st.radio("The Final Decision:", display_values)

        if st.button("Cast the Spell"):
            selected_key = next(key for key, desc in items if desc == choice)
            if selected_key == "1":
                st.session_state.game_over_reason = "You revived the evil Lords. They ate you."
                st.session_state.scene = "game_over"
                st.rerun()
            else:
                st.session_state.scene = "victory"
                st.rerun()

    with col2:
        render_scene_media("finale", container=col2)

def victory():
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.balloons()
        st.markdown("<h1 style='text-align: left; color: gold;'>VICTORY!</h1>", unsafe_allow_html=True)
        st.divider()
        st.write("The Lords turn to ash and blow away in the wind. Xibalba isdefeated.")
        st.success("Hunahpu and Xbalanque rise into the sky to become the SUN and the MOON.")

        if st.button("Play Again", type="primary"):
            reset_for_restart()
            st.session_state.scene = "start"
            st.rerun()

    with col2:
        render_scene_media("victory", container=col2)

def game_over():
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("<h1 style='text-align: left; color: red;'>GAME OVER</h1>", unsafe_allow_html=True)
        st.error(f"**Fate:** {st.session_state.get('game_over_reason', 'Unknown')}")

        if st.button("Try Again", type="primary", use_container_width=True):
            reset_for_restart()
            st.session_state.scene = "start"
            st.rerun()

    with col2:
        render_scene_media("game_over", container=col2)

#####################
# MAIN APP LOGIC
#####################

initialize_state()

# Show HUD on all screens except Start and Game Over
if st.session_state.scene not in ["start", "game_over", "victory"]:
    show_hud()

# Scene Router
if st.session_state.scene == "start":
    start()
elif st.session_state.scene == "crossroads":
    crossroads()
elif st.session_state.scene == "throne_room":
    throne_room()
elif st.session_state.scene == "house_of_gloom":
    house_of_gloom()
elif st.session_state.scene == "house_of_cold":
    house_of_cold()
elif st.session_state.scene == "house_of_jaguars":
    house_of_jaguars()
elif st.session_state.scene == "ballgame":
    ballgame()
elif st.session_state.scene == "finale":
    finale()
elif st.session_state.scene == "victory":
    victory()
elif st.session_state.scene == "game_over":
    game_over()
else:
    st.session_state.scene = "start"
    st.rerun()
