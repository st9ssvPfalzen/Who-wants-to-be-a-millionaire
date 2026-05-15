import streamlit as st  # Streamlit is the library that turns this Python script into a web app
import json              # json lets us read our questions.json file
import random            # random is used for shuffling, sampling, and simulating lifelines
from styles import inject_css, show_host, show_money_rain  # show_money_rain replaces st.balloons()


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
# JOAO'S COMMENTS
# ─────────────────────────────────────────

# These are the lines João can say in different situations.
# random.choice() picks one randomly each time so he doesn't repeat himself.
# The correct and idle lists are long because they can show up up to 14 times per game.
# Accents are correct throughout: Olá, João.

JOAO_INTRO = "Olá! I am João, your host. Let's see if you have what it takes!"

# 20 options for correct answers — needed because this can show up 14 times in one game
JOAO_CORRECT = [
    "Correct! Even I knew that one.",
    "Well done. I had my doubts about you.",
    "Right again. Don't let it go to your head.",
    "Impressive... for a beginner.",
    "Correct. You may continue.",
    "That one was almost too easy. Almost.",
    "Good. Keep it up. I dare you.",
    "You got lucky. Or did you? I cannot tell.",
    "Right answer. Wrong attitude, but right answer.",
    "Correct! The audience is mildly impressed.",
    "Another one down. Only a few more to go.",
    "I'll admit, I did not expect that.",
    "Correct. I've seen worse. Not often, but I have.",
    "You continue to surprise me. Faintly.",
    "Right. Let's see how long this lasts.",
    "Correct again. João is... cautiously optimistic.",
    "Well. You clearly studied. Or guessed well.",
    "That is correct. Don't celebrate too early.",
    "Yes. That is the right answer. Well done.",
    "Correct! João nods. Grudgingly.",
]

JOAO_WRONG = [
    "Oh dear. That was painful to watch.",
    "I knew that one. Did you not?",
    "Perhaps quiz shows are not your calling.",
    "Back to school, perhaps?",
    "Ah. So close. Not really, but still.",
    "Wrong! João sighs deeply.",
    "That... was not it. Not even close.",
]

JOAO_FIFTY = [
    "Fifty-fifty! Eliminating the obvious ones, are we?",
    "Do you need the options reduced? How charming.",
    "Two gone. You still have to pick correctly, you know.",
    "50:50. A classic move for the uncertain mind.",
    "Half the options gone. Half your excuses too.",
]

JOAO_AUDIENCE = [
    "The audience! Always fun to see what the masses think.",
    "Let's see if the crowd is smarter than you. Likely, yes.",
    "Asking the audience? Bold. Or desperate. Hard to tell.",
    "Democracy in action. How quaint.",
    "The people have spoken. Whether you listen is up to you.",
]

JOAO_PHONE = [
    "Phoning a friend! Do you have intelligent friends?",
    "Let's hope your friend is sharper than you.",
    "A phone call! How retro. And how telling.",
    "Your friend better be smarter than you look.",
    "Calling for help already? João raises an eyebrow.",
]

JOAO_SWITCH = [
    "Switching the question? Running away, are we?",
    "A fresh question. Let's hope you find this one easier.",
    "Cowardly, but legal. Here is a new one.",
    "Switching! A bold move. Or a desperate one.",
    "New question coming. Try not to switch again.",
]

JOAO_CHECKPOINT = [
    "You've reached a safe level. Don't get comfortable.",
    "A checkpoint! Even I will admit — well played.",
    "Safe at last. For now.",
    "Safe level reached. João tips his hat. Slightly.",
    "You are guaranteed something. Not a million, but something.",
]

JOAO_WALKAWAY = [
    "Walking away? Wise, perhaps. Or cowardly. Both, probably.",
    "Taking the money! Sensible. Not exciting, but sensible.",
    "You walk away. I stay here. As always.",
    "A safe exit. João approves. Grudgingly.",
    "Smart play. Or just scared. Hard to say.",
]

JOAO_MILLIONAIRE = [
    "A MILLIONAIRE! I am... actually impressed. Well done.",
    "You did it! I never doubted you. (I doubted you.)",
    "One million euros! João is speechless. Almost.",
    "Extraordinary. Truly. João bows. Just this once.",
]

# 20 options for idle comments — needed because this shows up with every question played
JOAO_IDLE = [
    "Take your time. I am not going anywhere.",
    "Thinking? Good. A rare sight on this show.",
    "The suspense is almost interesting.",
    "I have seen faster thinkers. Not many, but some.",
    "João waits. Patiently. Mostly.",
    "Still thinking? João checks his watch.",
    "No rush. The million will wait.",
    "Concentration is key. Or so I am told.",
    "I've hosted many contestants. Few were this slow.",
    "The clock is not ticking. But João is watching.",
    "Read all the options. Carefully. Please.",
    "Take a breath. Then answer correctly.",
    "João adjusts his glasses. Still waiting.",
    "This is the part where you answer the question.",
    "One question at a time. You can do this. Probably.",
    "I have seen braver decisions. And worse ones.",
    "The answer is there. Somewhere. Think.",
    "João sips his coffee. He has time.",
    "Every second counts. Except when it doesn't.",
    "The next question is harder. Just so you know.",
]


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
        st.session_state.phase             = "splash"          # first screen shown is the splash/logo screen
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
        st.session_state.popup             = None              # stores the current popup message (or None if none)
        st.session_state.joao_comment      = JOAO_INTRO        # João's current speech bubble line


# ─────────────────────────────────────────
# PREPARE QUESTIONS FOR A GAME SESSION
# ─────────────────────────────────────────
def prepare_questions(all_questions):
    """
    Takes the full question dataset and selects 1 question per difficulty level,
    returning a list of 15 questions sorted from easiest (level 1) to hardest (level 15).
    The dataset has 15 difficulty levels with 50 questions each, so every game
    is different because 1 question is randomly sampled from each level's pool.
    This maps directly onto the prize ladder: level 1 = EUR 100, level 15 = EUR 1,000,000.
    """

    # Group all questions by their difficulty value (1 through 15) into a dictionary.
    # Example result: {1: [q1, q2, ...50 questions], 2: [...], ..., 15: [...]}
    by_difficulty = {}
    for q in all_questions:
        d = q["difficulty"]
        # setdefault creates the key with an empty list if it doesn't exist yet,
        # then appends the question to that list.
        by_difficulty.setdefault(d, []).append(q)

    selected = []
    # Loop through all 15 difficulty levels in ascending order.
    # We pick exactly 1 question per level so the game has 15 questions
    # that map directly onto the 15 prize ladder steps.
    for level in sorted(by_difficulty.keys()):
        pool = by_difficulty[level]
        # random.sample picks 1 unique question randomly from the pool for this level.
        # min(1, len(pool)) is a safety check in case a level somehow has no questions.
        selected.extend(random.sample(pool, min(1, len(pool))))

    return selected  # returns a flat list of 15 questions, one per difficulty level


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
# SPLASH SCREEN
# ─────────────────────────────────────────
def show_splash():
    """
    The very first screen shown when the app loads.
    Displays the game logo centred on the dark background with a single
    'Start Playing' button below it. Clicking the button moves to the setup screen.
    No player name or mode is collected here — that happens on the next screen.
    """

    # Show João with his intro comment in the corner
    show_host(st.session_state.joao_comment)

    # Centre the logo using three columns — the middle column holds the image.
    # col widths [0.2, 6, 0.2] give the logo maximum horizontal space so it appears large.
    col_left, col_mid, col_right = st.columns([0.2, 6, 0.2])
    with col_mid:
        # Logo served via app/static/ URL — same approach as joao.png in styles.py.
        # This must be inside a raw HTML img tag; st.image() cannot use this URL path.
        st.markdown(
            "<img src='app/static/logo.png' style='width:100%;display:block;margin:auto;'>",
            unsafe_allow_html=True
        )

    st.write("")  # spacing below the logo
    st.write("")

    # Centre the start button — narrower column than the logo so it doesn't stretch too wide
    col_left, col_mid, col_right = st.columns([2, 1, 2])
    with col_mid:
        if st.button("Start Playing", use_container_width=True):
            # Move to the setup screen where the player enters their name and picks a mode
            st.session_state.phase = "setup"
            st.rerun()


# ─────────────────────────────────────────
# SETUP SCREEN
# ─────────────────────────────────────────
def show_setup():
    """Renders the game setup screen where the player enters their name and picks a mode."""

    # Show João with his intro line on the setup screen
    show_host(st.session_state.joao_comment)

    # Logo shown in a wide column for good visibility on the setup screen.
    # Served via app/static/ URL, same as joao.png.
    col_left, col_mid, col_right = st.columns([1, 2, 1])
    with col_mid:
        st.markdown(
            "<img src='app/static/logo.png' style='width:100%;display:block;margin:auto;'>",
            unsafe_allow_html=True
        )

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
        - **Classic mode:** 3 lifelines — 50:50, Ask the Audience, Phone a Friend
        - **Risky mode:** 4 lifelines — same as Classic + Switch the Question
                
        Each lifeline can only be used **once** per game.

        **Walk away:** Before answering any question (after Q1), you can walk away and keep your current winnings.
        """)

    st.write("### Enter your name to start")

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

            # João greets the player by name as the game starts
            st.session_state.joao_comment = f"Welcome, {st.session_state.player_name}. Try not to embarrass yourself."

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
# CORRECT ANSWER POPUP
# ─────────────────────────────────────────
def show_popup():
    """
    Displays a styled green popup when the player answers correctly.
    If a checkpoint was just reached, a gold checkpoint badge is shown below it.
    The popup message is stored in st.session_state.popup and cleared after display.
    A 'Continue' button dismisses the popup and moves on to the next question.
    """

    # popup is a dict: {"message": str, "checkpoint": bool}
    # It is set in handle_answer() when the player is correct, and cleared here after dismissal.
    popup = st.session_state.popup

    st.markdown(f"""
        <div class='popup-correct'>
            <h2>Correct!</h2>
            <p>{popup['message']}</p>
        </div>
    """, unsafe_allow_html=True)

    # If this correct answer also landed on a checkpoint, show the gold badge below
    if popup.get("checkpoint"):
        checkpoint_prize = PRIZE_LADDER[st.session_state.q_index - 1]
        st.markdown(f"""
            <div class='popup-checkpoint'>
                <p>SAFE LEVEL REACHED — EUR {checkpoint_prize:,} is guaranteed!</p>
            </div>
        """, unsafe_allow_html=True)

    st.write("")

    # The Continue button dismisses the popup.
    # Clicking it clears the popup from session_state and reruns — the question screen appears.
    if st.button("Continue", use_container_width=True):
        st.session_state.popup = None
        # After a correct answer João makes an idle comment while the player reads the next question
        st.session_state.joao_comment = random.choice(JOAO_IDLE)
        st.rerun()


# ─────────────────────────────────────────
# PLAYING PHASE — QUESTION SCREEN
# ─────────────────────────────────────────
def show_question():
    """
    The main game screen. Shows the current question, four answer buttons,
    lifeline buttons, lifeline results (if any were used), and the walk away button.
    If a correct-answer popup is pending, it is shown instead of the question.
    The playing screen uses half_logo.png instead of the full logo.
    After 50:50 is used, eliminated answer buttons are replaced with dim HTML divs
    that sit in the same grid position — so the layout never shifts or reorders.
    """

    # Show the prize ladder in the sidebar first
    show_prize_ladder()

    # Show João with his current comment
    show_host(st.session_state.joao_comment)

    # If a popup is waiting (player just answered correctly), show it and stop here.
    # The question screen is hidden until the player clicks Continue.
    if st.session_state.popup:
        show_popup()
        return  # stop rendering the rest of the question screen

    # Get the current question index and fetch the corresponding question dictionary
    q_index = st.session_state.q_index
    q       = st.session_state.questions[q_index]
    # q is now a dictionary like: {"question": "...", "A": "...", "B": "...", "correct": "A", ...}

    # --- Header — half logo left, game name right ---
    # The playing screen uses half_logo.png served from app/static/ — the exact same
    # URL approach as joao.png and logo.png. Width 220px so it is clearly visible.
    col_logo, col_title = st.columns([1, 4])
    with col_logo:
        st.markdown(
            "<img src='app/static/half_logo.png' style='width:220px;'>",
            unsafe_allow_html=True
        )
    with col_title:
        # Accent on João correct in the game title
        st.markdown("<h1 style='text-align:left;font-size:1.5rem;'>Who Wants To Impress João?</h1>",
                    unsafe_allow_html=True)
        st.markdown(f"<p style='color:#a8b8c8;margin:0;'>{st.session_state.player_name} &nbsp;|&nbsp; {st.session_state.game_mode} Mode</p>",
                    unsafe_allow_html=True)

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

    # --- Answer buttons arranged in a fixed 2x2 grid ---
    # All four options are always rendered to keep the grid layout stable.
    # Options eliminated by 50:50 are shown as dim static HTML divs that match
    # the button shape and size — they cannot be clicked and stay in their grid
    # position so the layout never shifts when options are removed.
    # Active options are rendered as normal st.button() elements.
    remaining = st.session_state.remaining_options
    options   = ["A", "B", "C", "D"]

    col1, col2 = st.columns(2)  # two side-by-side columns for the answer buttons

    for i, option in enumerate(options):
        # i % 2 == 0 → left column (A and C), i % 2 != 0 → right column (B and D)
        # This mapping is fixed regardless of which options remain after 50:50
        col = col1 if i % 2 == 0 else col2

        with col:
            if option not in remaining:
                # Eliminated by 50:50 — render as a dim non-clickable HTML div.
                # The div matches the button's border-radius, padding and height
                # so the grid position is preserved and nothing shifts.
                st.markdown(f"""
                    <div style="
                        background: #080e1c;
                        color: #2a3a4a;
                        border: 1px solid #1a2a3a;
                        border-radius: 30px;
                        font-size: 1rem;
                        font-weight: bold;
                        padding: 0.6rem 1rem;
                        width: 100%;
                        text-align: center;
                        opacity: 0.4;
                        margin-bottom: 8px;
                        min-height: 46px;
                        line-height: 2;
                        box-sizing: border-box;
                    ">{option}: {q[option]}</div>
                """, unsafe_allow_html=True)
            else:
                # Active option — normal clickable button.
                # key= gives each button a unique identifier so Streamlit can tell them apart.
                if st.button(f"{option}: {q[option]}", use_container_width=True, key=f"ans_{option}"):
                    handle_answer(option, q)  # process the player's answer choice

    st.write("---")

    # --- Lifeline results ---
    # If the player used "Ask the Audience" or "Phone a Friend", show the result here.
    # This function checks session_state and only displays something if a result exists.
    show_lifeline_results()

    # --- Lifeline buttons ---
    # Each lifeline gets a symbol prefix so they are visually distinct.
    # Used lifelines are passed disabled=True which triggers the dim CSS style in styles.py.
    st.markdown("**Lifelines:**")
    used = st.session_state.used_lifelines  # list of lifeline names already used this game

    # Symbols for each lifeline — shown to the left of the label inside the button
    lifeline_symbols = {
        "50:50":               "✂️",
        "Ask the Audience":    "👥",
        "Phone a Friend":      "📞",
        "Switch the Question": "🔄"
    }

    # Create one column per lifeline so they appear side by side in a row
    lifeline_cols = st.columns(len(st.session_state.lifelines))

    for i, lifeline in enumerate(st.session_state.lifelines):
        with lifeline_cols[i]:
            # A lifeline is disabled if it has already been used
            disabled = lifeline in used

            # Build the button label: symbol + name, or symbol + name + (used)
            symbol    = lifeline_symbols.get(lifeline, "")
            btn_label = f"{symbol} {lifeline} (used)" if disabled else f"{symbol} {lifeline}"

            # disabled=True makes the button unclickable and triggers the CSS disabled style
            # defined in styles.py which makes it visually dark, faded and dashed
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
            st.session_state.money        = walk_prize   # lock in the winnings
            st.session_state.phase        = "game_over"  # end the game
            st.session_state.end_reason   = "walk_away"  # tells the end screen why the game ended
            st.session_state.joao_comment = random.choice(JOAO_WALKAWAY)
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
        # Correct answer

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

        # Check if the player just landed exactly on a checkpoint index.
        # q_index has already been incremented, so the checkpoint is at q_index - 1.
        just_hit_checkpoint = (st.session_state.q_index - 1) in st.session_state.checkpoints

        # Build the popup message and set João's comment
        if just_hit_checkpoint:
            st.session_state.joao_comment = random.choice(JOAO_CHECKPOINT)
        else:
            st.session_state.joao_comment = random.choice(JOAO_CORRECT)

        popup_msg = f"You are now playing for EUR {PRIZE_LADDER[min(st.session_state.q_index, 14)]:,}!"

        # Check if the player just answered the last question (index 15 = beyond question 15)
        if st.session_state.q_index >= 15:
            st.session_state.phase        = "game_over"
            st.session_state.end_reason   = "won"
            st.session_state.joao_comment = random.choice(JOAO_MILLIONAIRE)
            st.session_state.popup        = None  # no popup needed — go straight to end screen
        else:
            st.session_state.phase = "playing"
            # Store the popup so show_question() can display it before the next question
            st.session_state.popup = {
                "message":    popup_msg,
                "checkpoint": just_hit_checkpoint
            }

    else:
        # Wrong answer

        # Calculate fallback prize using the checkpoint helper function
        st.session_state.money = get_checkpoint_prize()

        # Save the correct answer so we can reveal it on the end screen
        st.session_state.correct_answer = q["correct"]           # e.g. "D"
        st.session_state.correct_text   = q[q["correct"]]        # e.g. "Anna Karenina"

        st.session_state.phase        = "game_over"
        st.session_state.end_reason   = "wrong"
        st.session_state.joao_comment = random.choice(JOAO_WRONG)

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

    # Set João's comment based on which lifeline was chosen, then apply the effect
    if lifeline == "50:50":
        st.session_state.joao_comment = random.choice(JOAO_FIFTY)
        apply_fifty_fifty(q)
    elif lifeline == "Ask the Audience":
        st.session_state.joao_comment = random.choice(JOAO_AUDIENCE)
        apply_ask_audience(q)
    elif lifeline == "Phone a Friend":
        st.session_state.joao_comment = random.choice(JOAO_PHONE)
        apply_phone_friend(q)
    elif lifeline == "Switch the Question":
        st.session_state.joao_comment = random.choice(JOAO_SWITCH)
        apply_switch_question()

    # Rerun the page so the lifeline effect is immediately visible
    st.rerun()


# ─────────────────────────────────────────
# LIFELINE LOGIC
# ─────────────────────────────────────────
def apply_fifty_fifty(q):
    """
    Removes 2 wrong answers from the screen, leaving only the correct answer
    and 1 randomly chosen wrong answer. The eliminated options are replaced with
    dim static HTML divs in their original grid position — so the layout never
    shifts or reorders after 50:50 is used.
    """
    # Build a list of all wrong options (all options except the correct one)
    wrong = [opt for opt in ["A", "B", "C", "D"] if opt != q["correct"]]

    # Shuffle the wrong options so the elimination is random each time
    random.shuffle(wrong)

    # Take the first 2 from the shuffled list — these will be eliminated
    eliminated = wrong[:2]

    # Update remaining_options to only the options NOT eliminated.
    # show_question() uses this list to decide which options get the dim HTML div.
    st.session_state.remaining_options = [
        opt for opt in ["A", "B", "C", "D"] if opt not in eliminated
    ]


def apply_ask_audience(q):
    """
    Simulates the audience voting lifeline.
    The correct answer usually gets the most votes (45-75%), but not always —
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
    Replaces the current question with a different question at the same difficulty level.
    Only available in Risky mode. The player gets a fresh question with no penalty.
    With 15 difficulty levels and 50 questions per level, there are always plenty
    of replacement candidates available at the same level.
    """
    # Get the difficulty level of the current question
    current_q  = st.session_state.questions[st.session_state.q_index]
    difficulty = current_q["difficulty"]

    # Load the full question dataset to search for a replacement
    all_questions  = load_questions()
    used_questions = st.session_state.questions  # the 15 questions already in this game

    # Find questions that:
    # 1. Have exactly the same difficulty level as the current question
    # 2. Are not already in the current game's question list
    # With 50 questions per level this will almost always find a replacement.
    candidates = [
        q for q in all_questions
        if q["difficulty"] == difficulty and q not in used_questions
    ]

    if candidates:
        new_q = random.choice(candidates)  # pick a random replacement from the same level
        st.session_state.questions[st.session_state.q_index] = new_q  # replace in place

        # Reset 50:50 in case it was active on the old question —
        # the new question has all 4 fresh options available
        st.session_state.remaining_options = ["A", "B", "C", "D"]
    else:
        # Edge case: no replacement found at this level — extremely unlikely with 50 per level
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
    Each outcome uses a distinct styled box (red, gold, blue) defined in styles.py.
    On a win, show_money_rain() is called instead of st.balloons() for a themed celebration.
    The logo is displayed larger on the win screen using wider column proportions.
    """

    # Show João with his end-of-game comment
    show_host(st.session_state.joao_comment)

    # end_reason tells us WHY the game ended — set in handle_answer() or the walk away button
    reason = st.session_state.get("end_reason", "")
    # .get() is used here instead of direct access as a safety measure —
    # if "end_reason" somehow doesn't exist, it returns "" instead of crashing

    if reason == "won":
        # On the win screen the logo is shown extra large using [1, 3, 1] columns —
        # wider than the setup screen to make the branding more celebratory.
        col_left, col_mid, col_right = st.columns([1, 3, 1])
        with col_mid:
            st.markdown(
                "<img src='app/static/logo.png' style='width:100%;display:block;margin:auto;'>",
                unsafe_allow_html=True
            )
        st.write("---")
        # Player answered all 15 questions correctly — gold styled box
        st.markdown(f"""
            <div class='end-won'>
                <h2>MILLIONAIRE!</h2>
                <p>Incredible, {st.session_state.player_name}!</p>
                <p>You answered all 15 questions correctly.</p>
                <p>You won <strong>EUR 1,000,000</strong>!</p>
                <p>João is impressed. Finally.</p>
            </div>
        """, unsafe_allow_html=True)
        # Money rain animation — euro bills fall down the screen instead of st.balloons()
        show_money_rain()

    else:
        # For wrong and walk_away screens the logo is shown at normal size
        col_left, col_mid, col_right = st.columns([1, 3, 1])
        with col_mid:
            st.markdown(
                "<img src='app/static/logo.png' style='width:100%;display:block;margin:auto;'>",
                unsafe_allow_html=True
            )
        st.write("---")

        if reason == "wrong":
            # Player answered incorrectly — red styled box
            correct      = st.session_state.get("correct_answer", "")
            correct_text = st.session_state.get("correct_text", "")
            st.markdown(f"""
                <div class='end-wrong'>
                    <h2>Wrong Answer!</h2>
                    <p>The correct answer was <strong>{correct}: {correct_text}</strong></p>
                    <p>You go home with <strong>EUR {st.session_state.money:,}</strong></p>
                </div>
            """, unsafe_allow_html=True)

        elif reason == "walk_away":
            # Player chose to walk away voluntarily — blue styled box
            st.markdown(f"""
                <div class='end-walkaway'>
                    <h2>You Walked Away!</h2>
                    <p>A bold decision, {st.session_state.player_name}.</p>
                    <p>You leave with <strong>EUR {st.session_state.money:,}</strong></p>
                </div>
            """, unsafe_allow_html=True)

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
      - phase == "splash"    → show the logo splash screen
      - phase == "setup"     → show the setup screen
      - phase == "playing"   → show the question screen
      - phase == "game_over" → show the end screen
    """

    # Always run init_state() first — it sets up session_state on the very first run
    # and does nothing on subsequent reruns (because the "if" check prevents overwriting)
    inject_css()  # inject our custom CSS styles into the app
    init_state()

    if st.session_state.phase == "splash":
        show_splash()

    elif st.session_state.phase == "setup":
        show_setup()

    elif st.session_state.phase == "playing":
        show_question()

    elif st.session_state.phase == "game_over":
        show_end_screen()


# This is the only line that directly calls a function at the top level.
# Everything else is triggered from inside main().
main()