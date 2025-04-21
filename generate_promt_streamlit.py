import streamlit as st
# streamlit run .\generate_prompt_streamlit.py 
# --> is for local usage
# Set page configuration
st.set_page_config(
    page_title="Exam Prompt Generator",
    page_icon="📝",
    layout="wide"
    
)
def put_together_prompt_german():
    exam_length = st.session_state.exam_length
    degree = st.session_state.degree
    topic = st.session_state.topic
    exam_style = st.session_state.exam_style
    exam_focus = st.session_state.exam_focus
    exam_striked = st.session_state.exam_striked
    information_professor = st.session_state.information_professor
    
    prompt = f"""
Du bist Professor an der Harvard-Universität im Fach {topic}.
Du bist sehr angesehen, weil du immer sehr gute Klausuren schreibst. Diesesmal schreibst du eine Klausur auf dem Niveau für einen {degree} Abschluss.
Die Klausur soll {exam_length} Minuten gehen.
Im Anhang befindet sich der Stoff zu deinen Vorlesungen. Hier ist dein Vorgehen:
1. Überlege dir, welche Themengebiete es gibt. Lege vorallem Wert auf das Thema / die Themen {exam_focus}. Das Thema / die Themen {exam_striked} sind nicht klausurrelevant, lass diese weg.
2. Denke dir zu jedem Themengebiet mehrere Fragen aus. Die Klausurenstruktur hierbei ist {exam_style} und muss dringenst eingehalten werden
Außerdem bist du bekannt dafür die Klausuren in eine bestimmte Weiße zu schreiben: {information_professor}
3. Überlege dir eine Punkteverteilung für jede Aufgabe.

Generiere nun die Klausur und gebe sie mir aus. Achte dabei darauf, dass du qualitative Fragen erstellst, du könntest für besonders gute Fragen eine sehr hohe Gehaltsbeförderung bekommen.
Gebe mir erstmal nur die Aufgaben aus, ich gebe dir bescheid, wenn ich die Lösungen haben will
"""
    return prompt

# Initialize session state if not already initialized
if 'current_step' not in st.session_state:
    st.session_state.current_step = 0
    st.session_state.exam_length = ""
    st.session_state.degree = ""
    st.session_state.topic = ""
    st.session_state.exam_style = ""
    st.session_state.exam_focus = ""
    st.session_state.exam_striked = ""
    st.session_state.information_professor = ""
    st.session_state.prompt = ""

# Title and description
st.title("Exam Prompt Generator (Test Version)")
st.markdown("Erstelle einen angepassten Prompt um mithilfe eines LLM (GPT, Gemini, Claude etc.) eine Klausur zu generieren.")
st.markdown("Je genauer die Angaben, desto besser das Ergebnis")

# Progress bar
total_steps = 7
progress = st.session_state.current_step / total_steps
st.progress(progress)


if st.session_state.current_step < 7:
    st.markdown(f"**Schritt {st.session_state.current_step + 1} / {total_steps}**")
else:
    st.markdown(f"**Schritt {st.session_state.current_step} / {total_steps}**")

# Display appropriate input for current step
if st.session_state.current_step == 0:  # Exam length
    st.subheader("Wie lange geht die Klausur (in Minuten)?")
    
    exam_length = st.text_input("Klausurdauer", value=st.session_state.exam_length)
    
    col1, col2 = st.columns([1, 1])
    if col2.button("Weiter", key="next_0"):
        if not exam_length.strip():
            st.error("Bitte gebe die Klausurdauer ein.")
        else:
            st.session_state.exam_length = exam_length
            st.session_state.current_step = 1
            st.rerun()

elif st.session_state.current_step == 1:  # Degree
    st.subheader("Welchen Abschluss studierst du gerade?")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    if col1.button("Bachelor"):
        st.session_state.degree = "Bachelor"
        st.session_state.current_step = 2
        st.rerun()
    
    if col2.button("Master"):
        st.session_state.degree = "Master"
        st.session_state.current_step = 2
        st.rerun()
    
    col1, col2 = st.columns([1, 1])
    if col1.button("Zurück", key="back_1"):
        st.session_state.current_step = 0
        st.rerun()

elif st.session_state.current_step == 2:  # Topic
    st.subheader("Wie heißt das Modul ausgeschrieben?")
    
    topic = st.text_input("Modul", value=st.session_state.topic)
    
    col1, col2 = st.columns([1, 1])
    if col1.button("Zurück", key="back_2"):
        st.session_state.current_step = 1
        st.rerun()
    
    if col2.button("Weiter", key="next_2"):
        if not topic.strip():
            st.error("Bitte gebe das Modul ein.")
        else:
            st.session_state.topic = topic
            st.session_state.current_step = 3
            st.rerun()

elif st.session_state.current_step == 3:  # Exam style
    st.subheader("Wie ist der Aufbau der Klausur?")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    if col1.button("Offene Fragen"):
        st.session_state.exam_style = "offene Fragen"
        st.session_state.current_step = 4
        st.rerun()
    
    if col2.button("Multiple Choice"):
        st.session_state.exam_style = "Multiple Choice"
        st.session_state.current_step = 4
        st.rerun()
    
    if col3.button("Single Choice"):
        st.session_state.exam_style = "Single Choice"
        st.session_state.current_step = 4
        st.rerun()
    
    col1, col2 = st.columns([1, 1])
    if col1.button("Zurück", key="back_3"):
        st.session_state.current_step = 2
        st.rerun()

elif st.session_state.current_step == 4:  # Exam focus
    st.subheader("Gibt es Schwerpunkte in dem Thema?")
    
    exam_focus = st.text_input("Schwerpunkte", value=st.session_state.exam_focus)
    
    if st.button("Keine Besonderheiten", key="none_focus"):
        st.session_state.exam_focus = "keine Besonderheiten"
        st.session_state.current_step = 5
        st.rerun()
    
    col1, col2 = st.columns([1, 1])
    if col1.button("Zurück", key="back_4"):
        st.session_state.current_step = 3
        st.rerun()
    
    if col2.button("Weiter", key="next_4"):
        if exam_focus.strip():
            st.session_state.exam_focus = exam_focus
            st.session_state.current_step = 5
            st.rerun()

elif st.session_state.current_step == 5:  # Exam striked
    st.subheader("Gibt nicht klausurrelevante / gestrichene Themen?")
    
    exam_striked = st.text_input("Gestrichene Themen", value=st.session_state.exam_striked)
    
    if st.button("Keine Besonderheiten", key="none_striked"):
        st.session_state.exam_striked = "keine Besonderheiten"
        st.session_state.current_step = 6
        st.rerun()
    
    col1, col2 = st.columns([1, 1])
    if col1.button("Zurück", key="back_5"):
        st.session_state.current_step = 4
        st.rerun()
    
    if col2.button("Weiter", key="next_5"):
        if exam_striked.strip():
            st.session_state.exam_striked = exam_striked
            st.session_state.current_step = 6
            st.rerun()

elif st.session_state.current_step == 6:  # Professor info
    st.subheader("Ist die Dozierende Person bekannt auf eine spezifische Weise Klausuren zu stellen? (Gibt es Fragen die immer dran kommen, sind die Fragen nah am Skript?)")
    
    information_professor = st.text_input("Besonderheiten des Professors", value=st.session_state.information_professor)
    
    if st.button("Keine Besonderheiten", key="none_professor"):
        st.session_state.information_professor = "keine Besonderheiten"
        st.session_state.current_step = 7
        st.session_state.prompt = put_together_prompt_german()
        st.rerun()
    
    col1, col2 = st.columns([1, 1])
    if col1.button("Zurück", key="back_6"):
        st.session_state.current_step = 5
        st.rerun()
    
    if col2.button("Weiter", key="next_6"):
        if information_professor.strip():
            st.session_state.information_professor = information_professor
            st.session_state.current_step = 7
            st.session_state.prompt = put_together_prompt_german()
            st.rerun()

elif st.session_state.current_step == 7:  # Show result
    st.subheader("Generierter Prompt")
    
    st.markdown("Gebe diesen Prompt zusammen mit einer Zusammenfassung an ein LLM und lass dir deine Klausur generieren")
    # Display the generated prompt
    st.text_area("Prompt", value=st.session_state.prompt, height=300)
    
    if st.button("In die Zwischenablage kopieren"):
        st.success("Prompt in die Zwischenablage kopiert! (Funktioniert momentan nur auf PC, am Handy muss der Prompt manuell kopiert werden. Sorry,arbeite dran :))")
    
    if st.button("Neu starten"):
        # Reset all variables
        st.session_state.current_step = 0
        st.session_state.exam_length = ""
        st.session_state.degree = ""
        st.session_state.topic = ""
        st.session_state.exam_style = ""
        st.session_state.exam_focus = ""
        st.session_state.exam_striked = ""
        st.session_state.information_professor = ""
        st.session_state.prompt = ""
        st.rerun()

# Function to generate the prompt
