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

    </style>
    """, unsafe_allow_html=True)


def show_host(comment: str = ""):
    """
    Renders Joao in the top-right corner using position:fixed CSS.
    joao.png is served from the static/ folder at the project root.
    The image has a transparent background so it blends into the dark theme.
    The speech bubble floats above him with a downward pointing tail.
    """

    # Speech bubble — only rendered when there is a comment to show
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
                padding: 8px 12px;
                font-size: 0.75rem;
                font-family: Georgia, serif;
                font-style: italic;
                max-width: 140px;
                text-align: center;
                box-shadow: 0 2px 8px rgba(0,0,0,0.5);
                line-height: 1.4;
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

    # Character image — transparent PNG so he blends into the dark background
    # served from static/joao.png at the project root via Streamlit static serving
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