import streamlit as st

questions = [
    {"question": "What is the capital of France?",
     "A": "Paris", "B": "Rome", "C": "Berlin", "D": "Madrid",
     "correct": "A", "difficulty": 1},
    {"question": "What is 2 + 2?",
     "A": "3", "B": "4", "C": "5", "D": "6",
     "correct": "B", "difficulty": 1},
]

prize_ladder = [100, 200, 300, 500, 1000]

if "q_index" not in st.session_state:
    st.session_state.q_index = 0
    st.session_state.money = 0
    st.session_state.phase = "playing"

if st.session_state.phase == "playing":
    q = questions[st.session_state.q_index]
    st.title("Who Wants to Be a Millionaire?")
    st.write(f"**Question {st.session_state.q_index + 1}:** {q['question']}")
    st.write(f"Current prize: {st.session_state.money} euros")
    for option in ["A", "B", "C", "D"]:
        if st.button(f"{option}: {q[option]}"):
            if option == q["correct"]:
                st.session_state.money = prize_ladder[st.session_state.q_index]
                st.session_state.q_index += 1
                if st.session_state.q_index >= len(questions):
                    st.session_state.phase = "won"
                st.rerun()
            else:
                st.session_state.phase = "lost"
                st.rerun()

elif st.session_state.phase == "lost":
    st.error(f"Wrong! You go home with {st.session_state.money} euros")

elif st.session_state.phase == "won":
    st.success(f"You won {st.session_state.money} euros!")