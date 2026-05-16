import streamlit as st


def inject_css():
    st.markdown("""
    <style>

    /* ── Page background ── */
    .stApp {
        background: radial-gradient(ellipse at center, #0a1628 0%, #000510 100%);
        color: #e8d48b;
        font-family: 'Georgia', serif;
    }

    /* ── Hide Streamlit default chrome ── */
    #MainMenu, footer, header { visibility: hidden; }

    /* ── Titles and headers ── */
    h1 {
        color: #f0c040 !important;
        text-align: center !important;
        font-size: 2.2rem !important;
        text-shadow: 0 0 20px rgba(240, 192, 64, 0.6);
        letter-spacing: 2px;
    }
    h2, h3 {
        color: #c8a020 !important;
        text-align: center !important;
    }

    /* ── All buttons — base style ── */
    .stButton > button {
        background: linear-gradient(180deg, #1a3a6b 0%, #0d1f3c 100%);
        color: #e8d48b !important;
        border: 2px solid #4a7fd4;
        border-radius: 30px;
        font-size: 1rem;
        font-weight: bold;
        padding: 0.6rem 1rem;
        width: 100%;
        transition: all 0.2s ease;
        text-shadow: 0 0 8px rgba(232, 212, 139, 0.4);
        box-shadow: 0 0 10px rgba(74, 127, 212, 0.3);
    }
    .stButton > button:hover {
        background: linear-gradient(180deg, #2a5aaa 0%, #1a3a6b 100%);
        border-color: #f0c040;
        color: #ffffff !important;
        box-shadow: 0 0 20px rgba(240, 192, 64, 0.5);
        transform: scale(1.02);
    }

    /* ── Lifeline buttons — fixed height so all are the same size ── */
    [data-testid="stHorizontalBlock"] .stButton > button {
        height: 70px;
        font-size: 0.82rem;
        white-space: normal;
        line-height: 1.3;
        padding: 0.4rem 0.6rem;
    }

    /* ── Disabled lifeline buttons — clearly inactive so players know they cannot be used ── */
    /* Streamlit adds the disabled attribute when disabled=True is passed to st.button() */
    [data-testid="stHorizontalBlock"] .stButton > button:disabled {
        background: #0a0f1a !important;          /* very dark, almost black */
        color: #3a4a5a !important;               /* dim grey text — clearly inactive */
        border: 2px dashed #2a3a4a !important;   /* dashed dim border instead of solid */
        opacity: 0.5 !important;                 /* fade the whole button */
        text-shadow: none !important;
        box-shadow: none !important;
        cursor: not-allowed !important;
        transform: none !important;
    }

    /* ── Eliminated answer buttons — shown after 50:50 removes two wrong options ── */
    /* These are dimmer than normal buttons but not as dark as used lifelines,      */
    /* so the player can still see which options were removed and where they were.   */
    /* The button stays in its grid position so the layout does not jump around.    */
    .answer-eliminated .stButton > button {
        background: #080e1c !important;          /* dark but not black — visibly different */
        color: #2a3a4a !important;               /* dim text, clearly not selectable */
        border: 1px solid #1a2a3a !important;    /* faint border, no glow */
        opacity: 0.4 !important;                 /* noticeably faded */
        text-shadow: none !important;
        box-shadow: none !important;
        cursor: default !important;              /* normal cursor — not a hand or not-allowed */
        transform: none !important;
        pointer-events: none;                    /* prevents any click or hover interaction */
    }

    /* ── Question box ── */
    .question-box {
        background: linear-gradient(180deg, #0f2347 0%, #071428 100%);
        border: 2px solid #4a7fd4;
        border-radius: 12px;
        padding: 1.5rem 2rem;
        margin: 1rem 0;
        text-align: center;
        font-size: 1.25rem;
        color: #ffffff;
        box-shadow: 0 0 25px rgba(74, 127, 212, 0.4);
    }

    /* ── Prize display ── */
    .prize-display {
        text-align: center;
        font-size: 1.1rem;
        color: #f0c040;
        margin-bottom: 0.5rem;
        letter-spacing: 1px;
    }

    /* ── Correct answer popup ── */
    .popup-correct {
        background: linear-gradient(135deg, #0a2f0a 0%, #0d4a0d 100%);
        border: 2px solid #4adf4a;
        border-radius: 16px;
        padding: 1.5rem 2rem;
        margin: 1rem 0;
        text-align: center;
        box-shadow: 0 0 30px rgba(74, 223, 74, 0.4);
    }
    .popup-correct h2 {
        color: #4adf4a !important;
        font-size: 1.8rem !important;
        margin: 0 0 0.5rem 0;
        text-shadow: 0 0 15px rgba(74, 223, 74, 0.6);
    }
    .popup-correct p {
        color: #a8f0a8;
        font-size: 1.1rem;
        margin: 0;
    }

    /* ── Checkpoint popup ── */
    .popup-checkpoint {
        background: linear-gradient(135deg, #2a1a00 0%, #4a3000 100%);
        border: 2px solid #f0c040;
        border-radius: 12px;
        padding: 0.8rem 1.5rem;
        margin-top: 0.8rem;
        text-align: center;
        box-shadow: 0 0 20px rgba(240, 192, 64, 0.4);
    }
    .popup-checkpoint p {
        color: #f0c040;
        font-size: 1rem;
        margin: 0;
        font-weight: bold;
        letter-spacing: 1px;
    }

    /* ── End screen — Wrong (red) ── */
    .end-wrong {
        background: linear-gradient(135deg, #2a0000 0%, #4a0000 100%);
        border: 2px solid #df4a4a;
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        box-shadow: 0 0 40px rgba(223, 74, 74, 0.5);
        margin: 1rem 0;
    }
    .end-wrong h2 {
        color: #ff6060 !important;
        font-size: 2rem !important;
        text-shadow: 0 0 20px rgba(255, 96, 96, 0.7);
        margin-bottom: 0.5rem;
    }
    .end-wrong p {
        color: #ffaaaa;
        font-size: 1.1rem;
        margin: 0.3rem 0;
    }

    /* ── End screen — Won (gold) ── */
    .end-won {
        background: linear-gradient(135deg, #1a1400 0%, #2a2200 100%);
        border: 2px solid #f0c040;
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        box-shadow: 0 0 50px rgba(240, 192, 64, 0.6);
        margin: 1rem 0;
    }
    .end-won h2 {
        color: #f0c040 !important;
        font-size: 2.2rem !important;
        text-shadow: 0 0 25px rgba(240, 192, 64, 0.8);
        margin-bottom: 0.5rem;
    }
    .end-won p {
        color: #e8d48b;
        font-size: 1.1rem;
        margin: 0.3rem 0;
    }

    /* ── End screen — Walk away (blue) ── */
    .end-walkaway {
        background: linear-gradient(135deg, #001a2a 0%, #00253d 100%);
        border: 2px solid #4ab0f0;
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        box-shadow: 0 0 40px rgba(74, 176, 240, 0.4);
        margin: 1rem 0;
    }
    .end-walkaway h2 {
        color: #4ab0f0 !important;
        font-size: 2rem !important;
        text-shadow: 0 0 20px rgba(74, 176, 240, 0.6);
        margin-bottom: 0.5rem;
    }
    .end-walkaway p {
        color: #a8d8f0;
        font-size: 1.1rem;
        margin: 0.3rem 0;
    }

    /* ── Dividers ── */
    hr {
        border-color: #2a4a7f !important;
    }

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #050e1f 0%, #000510 100%) !important;
        border-right: 1px solid #2a4a7f;
    }
    [data-testid="stSidebar"] * {
        color: #e8d48b !important;
    }

    /* ── Text input ── */
    .stTextInput > div > div > input {
        background-color: #0d1f3c !important;
        color: #e8d48b !important;
        border: 2px solid #4a7fd4 !important;
        border-radius: 8px;
    }

    /* ── Expander ── */
    .streamlit-expanderHeader {
        background-color: #0d1f3c !important;
        color: #f0c040 !important;
        border-radius: 8px;
    }

    /* ── Alert/info boxes ── */
    .stAlert {
        border-radius: 10px;
    }

    /* ── Money rain animation — shown on the win screen instead of balloons ── */
    /* The bills are rendered as emoji characters falling from the top of the screen. */
    /* Each bill is absolutely positioned and animated with a unique delay and speed */
    /* so they fall at different times, creating a natural rain effect.              */
    .money-rain {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;   /* clicks pass through so the Play Again button still works */
        z-index: 9000;
        overflow: hidden;
    }
    .bill {
        position: absolute;
        top: -80px;             /* start above the visible screen */
        font-size: 2.5rem;
        animation: fall linear forwards;
        opacity: 0.9;
    }
    @keyframes fall {
        0%   { transform: translateY(0) rotate(0deg);       opacity: 0.9; }
        80%  { opacity: 0.9; }
        100% { transform: translateY(110vh) rotate(360deg); opacity: 0; }
    }

    </style>
    """, unsafe_allow_html=True)


def show_host(comment: str = ""):
    """
    Renders João in the top-right corner using position:fixed CSS.
    joao.png is served from app/static/joao.png — the same URL pattern used for the logo.
    The speech bubble is slightly larger than the original for readability.
    """

    # Speech bubble — only rendered when there is a comment to show.
    # Font size 0.88rem and max-width 160px for comfortable reading.
    if comment:
        safe = comment.replace("'", "&#39;").replace('"', '&quot;')
        st.markdown(f"""
            <div style="
                position: fixed;
                top: 70px;
                right: 20px;
                background: #ffffff;
                color: #0a1628;
                border-radius: 12px;
                padding: 10px 14px;
                font-size: 0.88rem;
                font-family: Georgia, serif;
                font-style: italic;
                max-width: 160px;
                text-align: center;
                box-shadow: 0 2px 8px rgba(0,0,0,0.5);
                line-height: 1.5;
                z-index: 9999;
            ">{safe}
            <div style="
                position: absolute;
                bottom: -8px;
                left: 50%;
                transform: translateX(-50%);
                border-width: 8px 6px 0 6px;
                border-style: solid;
                border-color: #ffffff transparent transparent transparent;
            "></div>
            </div>
        """, unsafe_allow_html=True)

    # Character image — transparent PNG served from app/static/
    st.markdown("""
        <div style="
            position: fixed;
            top: 170px;
            right: 18px;
            z-index: 9998;
            width: 110px;
        ">
            <img src="app/static/joao.png" width="110"
                 style="display:block;" />
        </div>
    """, unsafe_allow_html=True)


def show_money_rain():
    """
    Renders an animated rain of money bill emoji falling down the screen.
    Used on the win screen instead of st.balloons() to match the game theme.
    Each bill gets a random horizontal position, fall duration, and start delay
    so the effect looks natural rather than uniform.
    Bills use the euro banknote emoji which is green and universally supported.
    """

    import random as _random

    # Generate 40 bills with randomised position, speed and delay.
    # We build the HTML for each bill as a separate div and inject them all at once.
    bills_html = ""
    for _ in range(40):
        # Random horizontal position across the full screen width
        left     = _random.randint(0, 95)        # percent
        # Fall duration between 2 and 5 seconds — mix of fast and slow bills
        duration = _random.uniform(2.0, 5.0)
        # Start delay up to 3 seconds so bills don't all appear at once
        delay    = _random.uniform(0.0, 3.0)
        # Alternate between euro note emoji and money bag for variety
        emoji    = _random.choice(["💶", "💶", "💶", "💰"])

        bills_html += (
            f"<div class='bill' style='"
            f"left:{left}%;"
            f"animation-duration:{duration:.1f}s;"
            f"animation-delay:{delay:.1f}s;"
            f"'>{emoji}</div>"
        )

    st.markdown(
        f"<div class='money-rain'>{bills_html}</div>",
        unsafe_allow_html=True
    )