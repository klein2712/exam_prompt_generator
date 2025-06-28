import streamlit as st
import base64

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
    
    # Create exam_style string based on percentages
    exam_style = ""
    if st.session_state.offene_fragen_percentage > 0:
        exam_style += f"{st.session_state.offene_fragen_percentage}% offene Fragen"
    
    if st.session_state.multiple_choice_percentage > 0:
        if exam_style:
            exam_style += ", "
        exam_style += f"{st.session_state.multiple_choice_percentage}% Multiple Choice"
    
    if st.session_state.single_choice_percentage > 0:
        if exam_style:
            exam_style += ", "
        exam_style += f"{st.session_state.single_choice_percentage}% Single Choice"
    
    exam_focus = st.session_state.exam_focus
    exam_striked = st.session_state.exam_striked
    information_professor = st.session_state.information_professor
    
    prompt = f"""
Du bist Professor an der Harvard-Universität im Fach {topic}.
Du bist sehr angesehen, weil du immer sehr gute Klausuren schreibst. Diesesmal schreibst du eine Klausur auf dem Niveau für einen {degree} Abschluss.
Die Klausur soll {exam_length} Minuten gehen.
Im Anhang befindet sich der Stoff zu deinen Vorlesungen. Hier ist dein Vorgehen:
1. Überlege dir, welche Themengebiete es gibt. Lege vorallem Wert auf das Thema / die Themen {exam_focus}. Das Thema / die Themen {exam_striked} sind nicht klausurrelevant, lass diese weg.
2. Denke dir zu jedem Themengebiet mehrere Fragen aus. Die Klausurenstruktur hierbei ist {exam_style} und muss dringenst eingehalten werden. Bei Single und Multiple Choice Fragen sollst du gleich mehrere Fragen generieren, da diese schneller zu beantworten sind.
Außerdem bist du bekannt dafür die Klausuren in eine bestimmte Weiße zu schreiben: {information_professor}
3. Überlege dir eine Punkteverteilung für jede Aufgabe.

Generiere nun die Klausur und gebe sie mir aus. Achte dabei darauf, dass du qualitative Fragen erstellst, du könntest für besonders gute Fragen eine sehr hohe Gehaltsbeförderung bekommen.
Gebe mir erstmal nur die Aufgaben aus, ich gebe dir bescheid, wenn ich die Lösungen haben will
"""
    return prompt

# Function to create a download link
def get_download_link(text, filename, link_text):
    """Generate a link to download the given text as a file"""
    b64 = base64.b64encode(text.encode()).decode()  # Convert to base64
    href = f'<a href="data:text/plain;base64,{b64}" download="{filename}">{link_text}</a>'
    return href

# Function to check if percentages sum to 100
def validate_percentages():
    total = (st.session_state.offene_fragen_percentage + 
             st.session_state.multiple_choice_percentage + 
             st.session_state.single_choice_percentage)
    return total == 100

# Initialize session state if not already initialized
if 'current_step' not in st.session_state:
    st.session_state.current_step = 0
    st.session_state.exam_length = ""
    st.session_state.degree = ""
    st.session_state.topic = ""
    # Replace single exam_style with three percentage variables
    st.session_state.offene_fragen_percentage = 0
    st.session_state.multiple_choice_percentage = 0
    st.session_state.single_choice_percentage = 0
    st.session_state.exam_focus = ""
    st.session_state.exam_striked = ""
    st.session_state.information_professor = ""
    st.session_state.prompt = ""

# Title and description
st.title("Exam Prompt Generator (Version 2)")
st.markdown("Erstelle einen angepassten Prompt um mithilfe eines LLM (GPT, Gemini, Claude etc.) und einer von dir gefertigeten Zusammenfassung eine Klausur zu generieren.")
st.markdown("Je genauer die Angaben möglich sind, desto besser wird das Ergebnis.")

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

elif st.session_state.current_step == 3:  # Exam style - UPDATED WITH PERCENTAGES
    st.subheader("Wie ist der Aufbau der Klausur? (Prozentuale Verteilung)")
    st.markdown("Gib für jede Fragenart einen Prozentsatz an. Die Summe muss 100% ergeben.")
    
    # Define callback functions for each input
    def on_offene_change():
        st.session_state.offene_fragen_percentage = st.session_state.offene_input
        
    def on_multiple_change():
        st.session_state.multiple_choice_percentage = st.session_state.multiple_input
        
    def on_single_change():
        st.session_state.single_choice_percentage = st.session_state.single_input
    
    # Create input fields for percentages with callbacks
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.number_input("Offene Fragen (%)", 
                         min_value=0, 
                         max_value=100, 
                         value=st.session_state.offene_fragen_percentage,
                         step=10,
                         key="offene_input",
                         on_change=on_offene_change)
    
    with col2:
        st.number_input("Multiple Choice (%)", 
                         min_value=0, 
                         max_value=100, 
                         value=st.session_state.multiple_choice_percentage,
                         step=10,
                         key="multiple_input",
                         on_change=on_multiple_change)
    
    with col3:
        st.number_input("Single Choice (%)", 
                         min_value=0, 
                         max_value=100, 
                         value=st.session_state.single_choice_percentage,
                         step=10,
                         key="single_input",
                         on_change=on_single_change)
    
    # Calculate and display total
    total_percentage = (st.session_state.offene_fragen_percentage + 
                       st.session_state.multiple_choice_percentage + 
                       st.session_state.single_choice_percentage)
    
    st.markdown(f"**Gesamtsumme: {total_percentage}%**")
    if total_percentage != 100:
        st.warning("Die Summe muss genau 100% ergeben.")
    
    col1, col2 = st.columns([1, 1])
    if col1.button("Zurück", key="back_3"):
        st.session_state.current_step = 2
        st.rerun()
    
    if col2.button("Weiter", key="next_3"):
        if validate_percentages():
            st.session_state.current_step = 4
            st.rerun()
        else:
            st.error("Die Summe muss genau 100% ergeben, bevor du fortfahren kannst.")

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
    
    st.markdown("Gebe diesen Prompt zusammen mit deiner Zusammenfassung des Moduls an ein LLM und lass dir deine Klausur generieren")
    
    # Display the generated prompt
    prompt_text = st.text_area("Prompt", value=st.session_state.prompt, height=300)
    
    # Create a column layout for buttons
    col1, col2, col3 = st.columns([1, 1, 1])
    
    # Simple Streamlit download button - more reliable than clipboard JS
    with col1:
        st.download_button(
            label="📥 Prompt herunterladen",
            data=prompt_text,
            file_name="exam_prompt.txt",
            mime="text/plain"
        )
    
    # Copy button (simpler approach using HTML)
    with col2:
        if st.button("📋 Prompt markieren"):
            st.info("Text im Feld oben wurde markiert! Drücke STRG+C zum Kopieren.")
            # Use JavaScript to select all text in the textarea
            js = """
            <script>
                var textareas = parent.document.querySelectorAll('textarea');
                var targetTextarea = textareas[textareas.length-1];
                targetTextarea.select();
            </script>
            """
            st.components.v1.html(js, height=0)
    
    # Reset button
    with col3:
        if st.button("🔄 Neu starten"):
            # Reset all variables
            st.session_state.current_step = 0
            st.session_state.exam_length = ""
            st.session_state.degree = ""
            st.session_state.topic = ""
            st.session_state.offene_fragen_percentage = 0
            st.session_state.multiple_choice_percentage = 0
            st.session_state.single_choice_percentage = 0
            st.session_state.exam_focus = ""
            st.session_state.exam_striked = ""
            st.session_state.information_professor = ""
            st.session_state.prompt = ""
            st.rerun()
