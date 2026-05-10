import streamlit as st  # Streamlit is the library that turns this Python script into a web app
import json              # json lets us read our questions.json file
import random            # random is used for shuffling, sampling, and simulating lifelines
from styles import inject_css # This is a custom module we created to inject CSS styles into the app


# ─────────────────────────────────────────
# LOAD QUESTIONS
# ─────────────────────────────────────────
def load_questions(filepath="questions.json"):
    # Open the JSON file and load its contents into a Python list of dictionaries.
    # "r" means read-only, encoding="utf-8" ensures special characters are handled correctly.
    # The result is a list like: [{"question": "...", "A": "...", "correct": "A", ...}, ...]
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


# ─────────────────────────────────────────
# PRIZE LADDER
# ─────────────────────────────────────────

# This list stores the prize amount for each question.
# Index 0 = Question 1 = 100 euros, index 14 = Question 15 = 1,000,000 euros.
# We use the question index (q_index) to look up the prize: PRIZE_LADDER[q_index]
PRIZE_LADDER = [
    100, 200, 300, 500, 1000,       # Questions 1-5  (easy)
    2000, 4000, 8000, 16000, 32000, # Questions 6-10 (medium)
    64000, 125000, 250000, 500000, 1000000  # Questions 11-15 (hard)
]

# These lists store the indices (0-based) of the safe level questions.
# Index 4 = Question 5 (1,000 euros), index 9 = Question 10 (32,000 euros).
# If a player answers wrong, we use these to find how much money they keep.
CHECKPOINTS_CLASSIC = [4, 9]   # Classic mode: two safe levels
CHECKPOINTS_RISKY   = [4]      # Risky mode: only one safe level


# ─────────────────────────────────────────
# INITIALIZE SESSION STATE
# ─────────────────────────────────────────
def init_state():
    # st.session_state is Streamlit's way of remembering values between reruns.
    # Every time the user clicks something, Streamlit reruns the whole script.
    # Without session_state, all variables would reset to their initial values on every click.
    #
    # We check if "phase" exists in session_state — if it doesn't, this is the very first run,
    # so we set up all variables with their starting values.
    # We only check one variable ("phase") because they are all created together at the same time.
    if "phase" not in st.session_state:
        st.session_state.phase             = "setup"           # which screen to show: "setup", "playing", or "game_over"
        st.session_state.player_name       = ""                # the name the player types in
        st.session_state.game_mode         = ""                # "Classic" or "Risky"
        st.session_state.q_index           = 0                 # which question we are on (0 = first question)
        st.session_state.money             = 0                 # current winnings in euros
        st.session_state.questions         = []                # the 15 questions selected for this game
        st.session_state.checkpoints       = []                # the safe level indices for the chosen mode
        st.session_state.lifelines         = []                # the lifeline names available in this mode
        st.session_state.used_lifelines    = []                # lifelines the player has already used
        st.session_state.remaining_options = ["A", "B", "C", "D"]  # answer options still visible (50:50 removes 2)
        st.session_state.audience_votes    = None              # stores audience vote percentages (or None if unused)
        st.session_state.phone_message     = None              # stores the friend's message (or None if unused)


# ─────────────────────────────────────────
# PREPARE QUESTIONS FOR A GAME SESSION
# ─────────────────────────────────────────
def prepare_questions(all_questions):
    """
    Takes the full question dataset and selects 5 questions per difficulty level,
    then returns them sorted from easiest to hardest (15 questions total).
    This means every game is different because questions are randomly sampled.
    """

    # Group all questions by their difficulty value into a dictionary.
    # Example result: {1: [q1, q2, ...], 2: [q6, q7, ...], 3: [q11, q12, ...]}
    by_difficulty = {}
    for q in all_questions:
        d = q["difficulty"]
        # setdefault creates the key with an empty list if it doesn't exist yet,
        # then appends the question to that list.
        by_difficulty.setdefault(d, []).append(q)

    selected = []
    # Loop through difficulty levels in ascending order (1, 2, 3, ...)
    for level in sorted(by_difficulty.keys()):
        pool = by_difficulty[level]
        # random.sample picks 'n' unique items from the list without replacement.
        # min(5, len(pool)) makes sure we don't try to pick more questions than exist.
        selected.extend(random.sample(pool, min(5, len(pool))))

    return selected  # returns a flat list of 15 questions, easy to hard


# ─────────────────────────────────────────
# HELPER — GET CURRENT CHECKPOINT PRIZE
# ─────────────────────────────────────────
def get_checkpoint_prize():
    """
    When the player answers wrong, this function calculates how much money they keep.
    It looks for the highest checkpoint the player has already passed.
    If no checkpoint has been reached yet, the player goes home with 0 euros.
    """
    # Filter the checkpoints list to only those the player has already passed.
    # A checkpoint at index i has been passed if the player is now on a question AFTER it (q_index > i).
    reached = [i for i in st.session_state.checkpoints if i < st.session_state.q_index]

    if reached:
        # max(reached) gives the most recent checkpoint index.
        # We use it to look up the prize for that question in PRIZE_LADDER.
        return PRIZE_LADDER[max(reached)]

    return 0  # No checkpoint reached yet — player goes home with nothing


# ─────────────────────────────────────────
# SETUP SCREEN
# ─────────────────────────────────────────
def show_setup():
    """Renders the game setup screen where the player enters their name and picks a mode."""

    st.title("Who Wants to Be a Millionaire?")
    st.write("---")  # horizontal divider line

    # st.expander creates a collapsible section — clicking it reveals the rules.
    # This keeps the setup screen clean and uncluttered.
    with st.expander("How to play — click to read the rules"):
        st.markdown("""
        **Goal:** Answer 15 multiple-choice questions correctly to win 1,000,000 euros!

        **Prize ladder:** Each correct answer moves you up the ladder. Questions get harder as the prize grows.

        **Safe levels (checkpoints):**
        - **Classic mode:** Two checkpoints at 1,000 and 32,000 euros. If you answer wrong, you fall back to the last checkpoint reached.
        - **Risky mode:** Only one checkpoint at 1,000 euros.

        **Lifelines:**
        - **Classic:** 3 lifelines — 50:50, Ask the Audience, Phone a Friend
        - **Risky:** 4 lifelines — same as Classic + Switch the Question
        Each lifeline can only be used **once** per game.

        **Walk away:** Before answering any question (after Q1), you can walk away and keep your current winnings.
        """)

    st.write("### Enter your details to start")

    # st.text_input renders a text box and returns whatever the user has typed.
    # The placeholder text is shown in grey before the user types anything.
    player_name = st.text_input("Your name:", placeholder="e.g. Alex")

    st.write("**Choose your game mode:**")

    # st.columns(2) splits the page into 2 side-by-side columns.
    # col1 = left column, col2 = right column.
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Classic")
        st.markdown("""
        - 3 lifelines
        - 2 checkpoints (1,000 and 32,000 euros)
        - Safer, more forgiving
        """)
        # st.button renders a clickable button and returns True the moment it is clicked.
        # use_container_width=True makes the button stretch to fill the full column width.
        classic_btn = st.button("Play Classic", use_container_width=True)

    with col2:
        st.markdown("### Risky")
        st.markdown("""
        - 4 lifelines
        - 1 checkpoint (1,000 euros only)
        - Higher risk, higher reward
        """)
        risky_btn = st.button("Play Risky", use_container_width=True)

    # This block runs only when one of the two mode buttons has been clicked.
    if classic_btn or risky_btn:

        # .strip() removes any accidental spaces at the start or end of the name.
        # We check if the name is empty before allowing the game to start.
        if not player_name.strip():
            st.warning("Please enter your name before starting!")
        else:
            # Save the player's name and chosen mode to session_state so we remember them later.
            st.session_state.player_name = player_name.strip()
            st.session_state.game_mode   = "Classic" if classic_btn else "Risky"

            # Load all questions from the JSON file, then randomly select 15 for this game.
            all_questions = load_questions()
            st.session_state.questions = prepare_questions(all_questions)

            # Set checkpoints and lifelines based on the chosen game mode.
            if st.session_state.game_mode == "Classic":
                st.session_state.checkpoints = CHECKPOINTS_CLASSIC
                st.session_state.lifelines   = ["50:50", "Ask the Audience", "Phone a Friend"]
            else:
                st.session_state.checkpoints = CHECKPOINTS_RISKY
                st.session_state.lifelines   = ["50:50", "Ask the Audience", "Phone a Friend", "Switch the Question"]

            # Switch to the playing phase and immediately rerun the script.
            # st.rerun() tells Streamlit to re-execute the file from the top,
            # which will now show the question screen instead of the setup screen.
            st.session_state.phase = "playing"
            st.rerun()


# ─────────────────────────────────────────
# SIDEBAR — PRIZE LADDER
# ─────────────────────────────────────────
def show_prize_ladder():
    """
    Displays the full prize ladder in the left sidebar.
    The current question is highlighted, and checkpoints are marked as [SAFE].
    The ladder is shown in reverse order so the highest prize is at the top,
    which matches how the real TV show displays it.
    """
    with st.sidebar:  # everything inside this block appears in the left sidebar
        st.markdown("## Prize Ladder")
        checkpoints = st.session_state.checkpoints
        q_index     = st.session_state.q_index

        # range(14, -1, -1) counts from 14 down to 0, so we display Q15 at the top
        # and Q1 at the bottom — highest prize first, just like the real show.
        for i in range(len(PRIZE_LADDER) - 1, -1, -1):
            prize = PRIZE_LADDER[i]
            label = f"EUR {prize:,}"  # {:,} formats numbers with commas e.g. 1,000,000

            if i == q_index:
                # Current question — gold highlight with arrow, styled via inline HTML
                st.markdown(
                    f"<div style='background:linear-gradient(90deg,#1a3a6b,#2a5aaa);"
                    f"border:1px solid #f0c040;border-radius:6px;padding:4px 8px;"
                    f"margin:2px 0;color:#f0c040;font-weight:bold;'>"
                    f"▶ Q{i+1} — {label}</div>",
                    unsafe_allow_html=True
                )
            elif i in checkpoints:
                # Safe level — green tint with checkmark
                st.markdown(
                    f"<div style='background:#0a2010;border:1px solid #3a8a3a;"
                    f"border-radius:6px;padding:4px 8px;margin:2px 0;color:#6adf6a;'>"
                    f"✓ Q{i+1} — {label} [SAFE]</div>",
                    unsafe_allow_html=True
                )
            else:
                # Regular question — plain dim text
                st.markdown(
                    f"<div style='padding:2px 8px;margin:1px 0;"
                    f"color:#a8b8c8;font-size:0.85rem;'>"
                    f"Q{i+1} — {label}</div>",
                    unsafe_allow_html=True
                )


# ─────────────────────────────────────────
# PLAYING PHASE — QUESTION SCREEN
# ─────────────────────────────────────────
def show_question():
    """
    The main game screen. Shows the current question, four answer buttons,
    lifeline buttons, lifeline results (if any were used), and the walk away button.
    """

    # Show the prize ladder in the sidebar first
    show_prize_ladder()

    # Get the current question index and fetch the corresponding question dictionary
    q_index = st.session_state.q_index
    q       = st.session_state.questions[q_index]
    # q is now a dictionary like: {"question": "...", "A": "...", "B": "...", "correct": "A", ...}

    # --- Header ---
    st.title("Who Wants to Be a Millionaire?")
    st.markdown(f"### {st.session_state.player_name} | {st.session_state.game_mode} Mode")
    st.write("---")

    # --- Question text and current prize ---
    current_prize = PRIZE_LADDER[q_index]  # prize for answering THIS question correctly

    # prize-display and question-box are custom CSS classes defined in styles.py.
    # unsafe_allow_html=True is required whenever we pass raw HTML to st.markdown().
    st.markdown(
        f"<div class='prize-display'>Question {q_index + 1} of 15 &nbsp;|&nbsp; Playing for: EUR {current_prize:,}</div>",
        unsafe_allow_html=True
    )
    # q_index + 1 because q_index is 0-based, but we want to show "Question 1", not "Question 0"
    st.markdown(
        f"<div class='question-box'>{q['question']}</div>",
        unsafe_allow_html=True
    )
    st.write("")  # empty line for spacing

    # --- Answer buttons arranged in a 2x2 grid ---
    # remaining_options tracks which answers are still visible.
    # Normally it is ["A", "B", "C", "D"], but after 50:50 it may be e.g. ["A", "C"].
    remaining = st.session_state.remaining_options
    options   = ["A", "B", "C", "D"]

    col1, col2 = st.columns(2)  # two side-by-side columns for the answer buttons

    for i, option in enumerate(options):
        # If this option was eliminated by 50:50, skip it — don't show the button at all
        if option not in remaining:
            continue

        # i % 2 == 0 is True for i=0 (A) and i=2 (C) → left column
        # i % 2 == 0 is False for i=1 (B) and i=3 (D) → right column
        # This gives us: A and C on the left, B and D on the right
        col = col1 if i % 2 == 0 else col2
        with col:
            # key= gives each button a unique identifier so Streamlit can tell them apart.
            # Without unique keys, Streamlit would get confused when multiple buttons exist.
            if st.button(f"{option}: {q[option]}", use_container_width=True, key=f"ans_{option}"):
                handle_answer(option, q)  # process the player's answer choice

    st.write("---")

    # --- Lifeline results ---
    # If the player used "Ask the Audience" or "Phone a Friend", show the result here.
    # This function checks session_state and only displays something if a result exists.
    show_lifeline_results()

    # --- Lifeline buttons ---
    st.markdown("**Lifelines:**")
    used = st.session_state.used_lifelines  # list of lifeline names already used this game

    # Create one column per lifeline so they appear side by side in a row
    lifeline_cols = st.columns(len(st.session_state.lifelines))

    for i, lifeline in enumerate(st.session_state.lifelines):
        with lifeline_cols[i]:
            # A lifeline is disabled if it has already been used
            disabled = lifeline in used

            # Change the button label to indicate it has been used
            btn_label = f"{lifeline} (used)" if disabled else lifeline

            # disabled=True makes the button unclickable and visually greyed out
            if st.button(btn_label, disabled=disabled, use_container_width=True, key=f"lf_{i}"):
                handle_lifeline(lifeline, q)  # apply the chosen lifeline

    # --- Walk Away button ---
    # The walk away option is only shown after Q1 (q_index > 0),
    # because on the first question the player has 0 euros — there is nothing to walk away with.
    if q_index > 0:
        st.write("---")
        # The walk away prize is the prize from the PREVIOUS question (already won)
        walk_prize = PRIZE_LADDER[q_index - 1]
        if st.button(f"Walk Away with EUR {walk_prize:,}", use_container_width=True):
            st.session_state.money      = walk_prize   # lock in the winnings
            st.session_state.phase      = "game_over"  # end the game
            st.session_state.end_reason = "walk_away"  # tells the end screen why the game ended
            st.rerun()


# ─────────────────────────────────────────
# ANSWER HANDLING
# ─────────────────────────────────────────
def handle_answer(chosen_option, q):
    """
    Called when the player clicks an answer button.
    Checks if the answer is correct and updates the game state accordingly.
    """

    if chosen_option == q["correct"]:
        # ✅ Correct answer

        # Update the player's winnings to the prize for the current question
        st.session_state.money   = PRIZE_LADDER[st.session_state.q_index]

        # Move to the next question
        st.session_state.q_index += 1  # += 1 is shorthand for q_index = q_index + 1

        # Reset all per-question state so the next question starts clean:
        # - 50:50 is reset so all 4 options are visible again
        # - audience votes and phone message are cleared
        st.session_state.remaining_options = ["A", "B", "C", "D"]
        st.session_state.audience_votes    = None
        st.session_state.phone_message     = None

        # Check if the player just answered the last question (index 15 = beyond question 15)
        if st.session_state.q_index >= 15:
            st.session_state.phase      = "game_over"
            st.session_state.end_reason = "won"       # the player wins!
        else:
            st.session_state.phase = "playing"        # continue to the next question

    else:
        # ❌ Wrong answer

        # Calculate fallback prize using the checkpoint helper function
        st.session_state.money = get_checkpoint_prize()

        # Save the correct answer so we can reveal it on the end screen
        st.session_state.correct_answer = q["correct"]           # e.g. "D"
        st.session_state.correct_text   = q[q["correct"]]        # e.g. "Anna Karenina"

        st.session_state.phase      = "game_over"
        st.session_state.end_reason = "wrong"

    # st.rerun() forces Streamlit to re-execute the script immediately,
    # so the new phase is reflected on screen right away.
    st.rerun()


# ─────────────────────────────────────────
# LIFELINE HANDLING
# ─────────────────────────────────────────
def handle_lifeline(lifeline, q):
    """
    Called when the player clicks a lifeline button.
    Marks the lifeline as used, applies its effect, then reruns the page.
    """

    # Add this lifeline to the used list so it becomes disabled for the rest of the game
    st.session_state.used_lifelines.append(lifeline)

    # Call the appropriate function based on which lifeline was chosen
    if lifeline == "50:50":
        apply_fifty_fifty(q)
    elif lifeline == "Ask the Audience":
        apply_ask_audience(q)
    elif lifeline == "Phone a Friend":
        apply_phone_friend(q)
    elif lifeline == "Switch the Question":
        apply_switch_question()

    # Rerun the page so the lifeline effect is immediately visible
    st.rerun()


# ─────────────────────────────────────────
# LIFELINE LOGIC
# ─────────────────────────────────────────
def apply_fifty_fifty(q):
    """
    Removes 2 wrong answers from the screen, leaving only the correct answer
    and 1 randomly chosen wrong answer.
    """
    # Build a list of all wrong options (all options except the correct one)
    wrong = [opt for opt in ["A", "B", "C", "D"] if opt != q["correct"]]

    # Shuffle the wrong options so the elimination is random each time
    random.shuffle(wrong)

    # Take the first 2 from the shuffled list — these will be eliminated
    eliminated = wrong[:2]

    # Update remaining_options to only contain the options NOT eliminated
    # This list is used in show_question() to decide which buttons to display
    st.session_state.remaining_options = [
        opt for opt in ["A", "B", "C", "D"] if opt not in eliminated
    ]


def apply_ask_audience(q):
    """
    Simulates the audience voting lifeline.
    The correct answer usually gets the most votes (45–75%), but not always —
    this keeps the lifeline realistic and not a guaranteed giveaway.
    """
    options = ["A", "B", "C", "D"]
    correct = q["correct"]

    # Give the correct answer a random share between 45% and 75%
    correct_share = random.randint(45, 75)

    # The remaining percentage is split among the 3 wrong answers
    remaining = 100 - correct_share

    # Pick 2 random cut points within the remaining percentage to split it into 3 parts.
    # sorted() ensures cuts[0] < cuts[1], which makes the math work correctly below.
    cuts = sorted(random.sample(range(1, remaining), 2))

    # The 3 wrong shares are: [first_cut, gap_between_cuts, rest_after_second_cut]
    wrong_shares = [cuts[0], cuts[1] - cuts[0], remaining - cuts[1]]

    # Shuffle so the wrong answers don't always get the same distribution
    random.shuffle(wrong_shares)

    # Build the votes dictionary: {option: percentage}
    votes = {}
    wi = 0  # index into wrong_shares
    for opt in options:
        if opt == correct:
            votes[opt] = correct_share
        else:
            votes[opt] = wrong_shares[wi]
            wi += 1

    # Store in session_state so show_lifeline_results() can display it
    st.session_state.audience_votes = votes


def apply_phone_friend(q):
    """
    Simulates the Phone a Friend lifeline with 4 possible outcomes,
    each assigned a probability weight.
    """
    correct = q["correct"]
    options = ["A", "B", "C", "D"]

    # random.choices() picks one outcome based on the given weights.
    # weights=[40, 30, 20, 10] means:
    #   40% chance the friend knows the correct answer
    #   30% chance the friend thinks it is correct but is unsure
    #   20% chance the friend gives a wrong answer
    #   10% chance the friend does not answer in time
    outcome = random.choices(
        ["knows", "unsure_correct", "wrong", "no_answer"],
        weights=[40, 30, 20, 10]
    )[0]  # random.choices returns a list, [0] gets the single chosen item

    if outcome == "knows":
        msg = f"I am pretty confident it is **{correct}: {q[correct]}**. Go for it!"

    elif outcome == "unsure_correct":
        msg = f"I think it might be **{correct}: {q[correct]}**, but I am not 100% sure..."

    elif outcome == "wrong":
        # Pick a random wrong option to give as the (incorrect) answer
        wrong_opt = random.choice([o for o in options if o != correct])
        msg = f"I think it is **{wrong_opt}: {q[wrong_opt]}**, but do not take my word for it!"

    else:  # "no_answer"
        msg = "Sorry, I did not have enough time to think! I am not sure..."

    # Store the message in session_state so show_lifeline_results() can display it
    st.session_state.phone_message = msg


def apply_switch_question():
    """
    Replaces the current question with a different question of the same difficulty.
    Only available in Risky mode. The player gets a fresh question with no penalty.
    """
    # Get the difficulty level of the current question
    current_q  = st.session_state.questions[st.session_state.q_index]
    difficulty = current_q["difficulty"]

    # Load the full question dataset to search for a replacement
    all_questions  = load_questions()
    used_questions = st.session_state.questions  # the 15 questions already in this game

    # Find questions that:
    # 1. Have the same difficulty level as the current question
    # 2. Are not already in the current game's question list
    candidates = [
        q for q in all_questions
        if q["difficulty"] == difficulty and q not in used_questions
    ]

    if candidates:
        new_q = random.choice(candidates)  # pick a random replacement
        st.session_state.questions[st.session_state.q_index] = new_q  # replace the question

        # Reset 50:50 in case it was active on the old question —
        # the new question has all 4 fresh options available
        st.session_state.remaining_options = ["A", "B", "C", "D"]
    else:
        # Edge case: no replacement found — inform the player
        st.warning("No replacement question available for this difficulty level!")


# ─────────────────────────────────────────
# DISPLAY LIFELINE RESULTS
# ─────────────────────────────────────────
def show_lifeline_results():
    """
    Displays the results of audience votes or the phone a friend message,
    if either of those lifelines has been used on the current question.
    Both audience_votes and phone_message are reset when moving to a new question,
    so this only shows results relevant to the current question.
    """

    # audience_votes is None by default — it only has a value after Ask the Audience is used
    if st.session_state.audience_votes:
        st.write("---")
        st.markdown("**Ask the Audience results:**")
        # Loop through each option and its percentage and display them as a list
        for opt, pct in st.session_state.audience_votes.items():
            st.markdown(f"- **{opt}:** {pct}%")

    # phone_message is None by default — it only has a value after Phone a Friend is used
    if st.session_state.phone_message:
        st.write("---")
        st.markdown("**Your friend says:**")
        # st.info displays the message in a blue highlighted box
        st.info(st.session_state.phone_message)


# ─────────────────────────────────────────
# END SCREEN
# ─────────────────────────────────────────
def show_end_screen():
    """
    Displays the final screen after the game ends.
    Shows a different message depending on whether the player won, answered wrong, or walked away.
    """
    st.title("Who Wants to Be a Millionaire?")
    st.write("---")

    # end_reason tells us WHY the game ended — set in handle_answer() or the walk away button
    reason = st.session_state.get("end_reason", "")
    # .get() is used here instead of direct access as a safety measure —
    # if "end_reason" somehow doesn't exist, it returns "" instead of crashing

    if reason == "won":
        # Player answered all 15 questions correctly
        st.success(f"Incredible, {st.session_state.player_name}! You are a MILLIONAIRE!")
        st.balloons()  # triggers a fun confetti animation in the browser

    elif reason == "wrong":
        # Player answered incorrectly — show what the correct answer was
        correct      = st.session_state.get("correct_answer", "")
        correct_text = st.session_state.get("correct_text", "")
        st.error(f"Wrong answer! The correct answer was **{correct}: {correct_text}**")
        st.markdown(f"You go home with **EUR {st.session_state.money:,}**")

    elif reason == "walk_away":
        # Player chose to walk away voluntarily
        st.info(f"You walked away with **EUR {st.session_state.money:,}**. Well played!")

    st.write("---")

    # Play Again button — resets all session_state variables to start fresh
    if st.button("Play Again", use_container_width=True):
        # Delete every key in session_state so init_state() starts from scratch on the next run
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()  # rerun the script — init_state() will reinitialize everything


# ─────────────────────────────────────────
# MAIN — controls which screen is shown
# ─────────────────────────────────────────
def main():
    """
    The entry point of the app. Called once at the bottom of the file.
    It initializes the game state and then decides which screen to show
    based on the current value of st.session_state.phase.

    Think of this as a traffic controller:
      - phase == "setup"     → show the setup screen
      - phase == "playing"   → show the question screen
      - phase == "game_over" → show the end screen
    """

    # Always run init_state() first — it sets up session_state on the very first run
    # and does nothing on subsequent reruns (because the "if" check prevents overwriting)
    inject_css() # Inject our custom CSS styles into the app
    init_state()

    if st.session_state.phase == "setup":
        show_setup()

    elif st.session_state.phase == "playing":
        show_question()

    elif st.session_state.phase == "game_over":
        show_end_screen()


# This is the only line that directly calls a function at the top level.
# Everything else is triggered from inside main().
main()