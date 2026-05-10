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

    /* ── Titles ── */
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

    /* ── All buttons ── */
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