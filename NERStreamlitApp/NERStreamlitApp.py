import streamlit as st
import spacy
from spacy.pipeline import EntityRuler
from spacy import displacy

st.title("Custom NER App with spaCy + Streamlit")
nlp = spacy.load("en_core_web_sm")

# Form + session storage
if "custom_patterns" not in st.session_state:
    st.session_state.custom_patterns = []

# Sidebar pattern form
with st.sidebar.form(key="pattern_form"):
    label = st.text_input("Entity Label (e.g., BRAND)")
    pattern = st.text_input("Pattern (e.g., Purely Pressed)")
    add_button = st.form_submit_button("Add Pattern")

if add_button and label and pattern:
    st.session_state.custom_patterns.append((pattern, label.upper()))
    st.sidebar.success(f"Added pattern: {pattern} as {label.upper()}")

# REBUILD the EntityRuler before processing input
if "entity_ruler" in nlp.pipe_names:
    nlp.remove_pipe("entity_ruler")

ruler = nlp.add_pipe("entity_ruler", before="ner")

# Add all stored patterns
for text, label in st.session_state.custom_patterns:
    ruler.add_patterns([{
        "label": label,
        "pattern": [{"LOWER": w.lower()} for w in text.split()]
    }])
# Show all current custom patterns
if st.session_state.custom_patterns:
    st.sidebar.markdown("### Current Custom Patterns:")
    for text, label in st.session_state.custom_patterns:
        st.sidebar.markdown(f"- **{text}** → `{label}`")
# NOW process user input
user_text = st.text_input("Text here:")

if user_text:
    st.markdown("### Analyzing Your Input")
    doc = nlp(user_text)
    if doc.ents:
        html = displacy.render(doc, style="ent", jupyter=False)
        st.components.v1.html(html, scrolling=True, height=250)
    else:
        st.info("No named entities found in the user input.")
