import streamlit as st
import json
import random

# ─────────────────────────────────────────
# LOAD QUESTIONS
# ─────────────────────────────────────────
def load_questions(filepath="questions.json"):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

# ─────────────────────────────────────────
# PRIZE LADDER
# ─────────────────────────────────────────
PRIZE_LADDER = [
    100, 200, 300, 500, 1000,
    2000, 4000, 8000, 16000, 32000,
    64000, 125000, 250000, 500000, 1000000
]

# Safe levels (question indices, 0-based)
CHECKPOINTS_CLASSIC = [4, 9]   # after Q5 and Q10
CHECKPOINTS_RISKY   = [4]      # after Q5 only

# ─────────────────────────────────────────
# INITIALIZE SESSION STATE
# ─────────────────────────────────────────
def init_state():
    if "phase" not in st.session_state:
        st.session_state.phase       = "setup"
        st.session_state.player_name = ""
        st.session_state.game_mode   = ""
        st.session_state.q_index     = 0
        st.session_state.money       = 0
        st.session_state.questions   = []
        st.session_state.checkpoints = []
        st.session_state.lifelines   = []

# ─────────────────────────────────────────
# PREPARE QUESTIONS FOR A GAME SESSION
# ─────────────────────────────────────────
def prepare_questions(all_questions):
    """
    Selects 5 questions per difficulty level (1, 2, 3)
    and returns them sorted easy → hard (15 total).
    Adjust the numbers if you add more difficulty levels.
    """
    by_difficulty = {}
    for q in all_questions:
        d = q["difficulty"]
        by_difficulty.setdefault(d, []).append(q)

    selected = []
    for level in sorted(by_difficulty.keys()):
        pool = by_difficulty[level]
        selected.extend(random.sample(pool, min(5, len(pool))))

    return selected

# ─────────────────────────────────────────
# SETUP SCREEN
# ─────────────────────────────────────────
def show_setup():
    st.title("🎰 Who Wants to Be a Millionaire?")
    st.write("---")

    # --- Rules summary ---
    with st.expander("📖 How to play — click to read the rules"):
        st.markdown("""
        **Goal:** Answer 15 multiple-choice questions correctly to win €1,000,000!

        **Prize ladder:** Each correct answer moves you up the ladder.
        The questions get harder as the prize grows.

        **Safe levels (checkpoints):**
        - 🟡 **Classic mode:** Two checkpoints at €1,000 and €32,000.
          If you answer wrong, you fall back to the last checkpoint you reached.
        - 🔴 **Risky mode:** Only one checkpoint at €1,000.
          If you answer wrong, you fall back to €1,000.

        **Lifelines:**
        - 🟡 **Classic:** 3 lifelines — 50:50, Ask the Audience, Phone a Friend
        - 🔴 **Risky:** 4 lifelines — same as Classic + Switch the Question.
        Each lifeline can only be used **once** per game.

        **Walk away:** Before answering any question, you can walk away
        and keep your current winnings.
        """)

    st.write("###  Enter your details to start")

    # --- Player name input ---
    player_name = st.text_input("Your name:", placeholder="e.g. Alex")

    # --- Game mode selection ---
    st.write("**Choose your game mode:**")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🟡 Classic")
        st.markdown("""
        - 3 lifelines
        - 2 checkpoints (€1,000 and €32,000)
        - Safer, more forgiving
        """)
        classic_btn = st.button("Play Classic", use_container_width=True)

    with col2:
        st.markdown("### 🔴 Risky")
        st.markdown("""
        - 4 lifelines
        - 1 checkpoint (€1,000 only)
        - Higher risk, higher reward
        """)
        risky_btn = st.button("Play Risky", use_container_width=True)

    # --- Handle button clicks ---
    if classic_btn or risky_btn:
        if not player_name.strip():
            st.warning("⚠️ Please enter your name before starting!")
        else:
            # Save player info
            st.session_state.player_name = player_name.strip()
            st.session_state.game_mode   = "Classic" if classic_btn else "Risky"

            # Load and prepare questions
            all_questions = load_questions()
            st.session_state.questions = prepare_questions(all_questions)

            # Set checkpoints and lifelines based on mode
            if st.session_state.game_mode == "Classic":
                st.session_state.checkpoints = CHECKPOINTS_CLASSIC
                st.session_state.lifelines   = ["50:50", "Ask the Audience", "Phone a Friend"]
            else:
                st.session_state.checkpoints = CHECKPOINTS_RISKY
                st.session_state.lifelines   = ["50:50", "Ask the Audience", "Phone a Friend", "Switch the Question"]

            # Move to the game
            st.session_state.phase = "playing"
            st.rerun()

# ─────────────────────────────────────────
# MAIN — controls which screen is shown
# WE SHOULD EDIT THIS WHEN WE HAVE THE GAME!!! 
# ─────────────────────────────────────────
def main():
    init_state()

    if st.session_state.phase == "setup":
        show_setup()

    elif st.session_state.phase == "playing":
        st.write(f"Welcome, {st.session_state.player_name}! Game coming soon...")
        # → this is where show_question() will go in the next step

    elif st.session_state.phase == "game_over":
        pass  # → show_end_screen() will go here

main()