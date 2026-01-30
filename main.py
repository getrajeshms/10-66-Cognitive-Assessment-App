# app.py
# Bilingual 10/66 Cognitive Assessment App
# Excel = variable-wise | PDF = domain-wise report
# RESET FIXED – PRODUCTION SAFE

import streamlit as st
import pandas as pd
from datetime import date
from io import BytesIO

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors

# ----------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------
st.set_page_config(page_title="10/66 Cognitive Assessment", layout="wide")

# ----------------------------------------------------
# RESET BUTTON (SAFE)
# ----------------------------------------------------
if st.button("🔄 New Subject / Reset"):
    st.session_state.clear()
    st.rerun()

# ----------------------------------------------------
# LANGUAGE TOGGLE
# ----------------------------------------------------
language = st.radio(
    "Language / ಭಾಷೆ",
    ["English", "Kannada"],
    horizontal=True
)

WORD_LIST = (
    ["Butter", "Arm", "Letter", "Queen", "Ticket",
     "Grass", "Corner", "Stone", "Book", "Stick"]
    if language == "English"
    else
    ["ಬೆಣ್ಣೆ", "ತೋಳು", "ಅಕ್ಷರ", "ರಾಣಿ", "ಟಿಕೆಟ್",
     "ಹುಲ್ಲು", "ಮೂಲೆ", "ಕಲ್ಲು", "ಪುಸ್ತಕ", "ಕಡ್ಡಿ"]
)

# ----------------------------------------------------
# UI THEME
# ----------------------------------------------------
st.markdown("""
<style>
button {font-size:18px !important;}
label {font-size:18px !important;}
</style>
""", unsafe_allow_html=True)

st.title("🧠 10/66 Cognitive Assessment")

# ====================================================
# 1. SUBJECT DETAILS
# ====================================================
st.header("1. Subject Details")

c1, c2, c3 = st.columns(3)
with c1:
    subject_id = st.text_input("Subject ID")
    age = st.number_input("Age", 50, 120)

with c2:
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    education = st.selectbox(
        "Education",
        ["No formal education", "Primary", "Secondary",
         "Higher Secondary", "Graduate", "Postgraduate"]
    )

with c3:
    interview_date = st.date_input("Date", date.today())
    investigator = st.text_input("Interviewer Name")

# ====================================================
# 2. WORD LIST LEARNING
# ====================================================
st.header("2. Word List Learning")

st.markdown(
    "I am going to read out a list of words. Please listen carefully. "
    "I will ask you to repeat them back to me when I have finished."
)
st.markdown("*Read slowly, pausing ~1 second between words.*")

learn_scores = {}
for learn in ["LEARN1", "LEARN2", "LEARN3"]:
    st.subheader(learn)
    cols = st.columns(5)
    total = 0
    for i, word in enumerate(WORD_LIST):
        with cols[i % 5]:
            total += st.radio(
                word, [0, 1],
                index=0,
                horizontal=True,
                key=f"{learn}_{word}"
            )
    learn_scores[learn] = total

learn_mean = round(sum(learn_scores.values()) / 3, 2)

st.info(
    f"LEARN1: {learn_scores['LEARN1']} | "
    f"LEARN2: {learn_scores['LEARN2']} | "
    f"LEARN3: {learn_scores['LEARN3']} | "
    f"Mean LEARN: {learn_mean}"
)

# ====================================================
# NAME REGISTRATION
# ====================================================
st.markdown(
    f"I would like you to remember my name. My name is **{investigator}**. "
    "Can you repeat that please?"
)

name = st.radio(
    "Immediate recall of interviewer name",
    [0, 1],
    horizontal=True
)

# ====================================================
# OBJECT NAMING
# ====================================================
st.header("Object Naming")

st.markdown(
    "We will begin with naming things. I will point to something and "
    "I would like you to tell me the name of the object."
)

objects = ["Pencil", "Watch", "Chair", "Shoes", "Knuckle", "Elbow", "Shoulder"]
object_naming_score = sum(
    st.radio(obj, [0, 1], horizontal=True, key=f"obj_{obj}")
    for obj in objects
)

# ====================================================
# SEMANTIC MEMORY
# ====================================================
st.header("Semantic Memory")

st.markdown(
    "Now I will tell you the name of something and I want you to describe what it is."
)

semantic_questions = ["Bridge", "Hammer", "Temple", "Medical Store"]
semantic_score = sum(
    st.radio(q, [0, 1], horizontal=True, key=f"semantic_{q}")
    for q in semantic_questions
)

# ====================================================
# SENTENCE REPETITION
# ====================================================
st.markdown("Repeat: *Adhu Houdhu, Aadhare Idhu Alla*")

sentence_repeat = st.radio(
    "Sentence repetition",
    [0, 1],
    horizontal=True
)

# ====================================================
# DELAYED RECALL – WORD LIST
# ====================================================
st.markdown(
    "Do you remember the list of words that I read out to you 3 times?"
)

delayed_words_10 = st.number_input(
    "Word List Delayed Recall (0–10)",
    0, 10, 0
)

# ====================================================
# DELAYED NAME
# ====================================================
name_delayed = st.radio(
    "Delayed recall of interviewer name",
    [0, 1],
    horizontal=True
)

# ====================================================
# VERBAL FLUENCY
# ====================================================
animals = st.number_input(
    "Animals named in 1 minute",
    0, 60, 0
)

# ====================================================
# WORD IMMEDIATE (3 WORDS)
# ====================================================
st.header("Word Immediate (Boat, House, Fish)")

wordimm_immediate = (
    st.radio("Boat", [0, 1], horizontal=True) +
    st.radio("House", [0, 1], horizontal=True) +
    st.radio("Fish", [0, 1], horizontal=True)
)

wordimm_delayed = st.number_input(
    "Delayed recall – 3 words (0–3)",
    0, 3, 0
)

# ====================================================
# ORIENTATION
# ====================================================
st.header("Orientation")

orientation_items = ["Month", "Day", "Year", "Season"]
orientation_score = sum(
    st.radio(item, [0, 1], horizontal=True, key=f"orient_{item}")
    for item in orientation_items
)

# ====================================================
# PRAXIS
# ====================================================
st.header("Praxis")

praxis_items = ["Nod", "Point", "Paper fold", "Circle", "Pentagon"]
praxis_score = sum(
    st.radio(item, [0, 1], horizontal=True, key=f"praxis_{item}")
    for item in praxis_items
)

# ====================================================
# STORY
# ====================================================
story_score = st.radio(
    "Story recall",
    [0, 1, 2, 3, 4, 5],
    horizontal=True
)

# ====================================================
# SCORES
# ====================================================
memory_score = (
    learn_scores["LEARN3"] +
    delayed_words_10 +
    wordimm_delayed +
    name +
    name_delayed +
    wordimm_immediate
)

language_score = animals + sentence_repeat + object_naming_score

total_score = (
    memory_score +
    language_score +
    orientation_score +
    praxis_score +
    semantic_score +
    story_score
)

cognitive_score = total_score - (animals + delayed_words_10 + wordimm_immediate)

flag = (
    "⚠️ Possible Cognitive Impairment"
    if total_score < 20
    else "✅ Within expected range"
)

st.warning(flag)

# ====================================================
# EXCEL EXPORT
# ====================================================
data = {
    "Subject ID": subject_id,
    "Age": age,
    "Gender": gender,
    "Education": education,
    "LEARN1": learn_scores["LEARN1"],
    "LEARN2": learn_scores["LEARN2"],
    "LEARN3": learn_scores["LEARN3"],
    "Mean LEARN": learn_mean,
    "Delayed Recall (10)": delayed_words_10,
    "Immediate Name Recall": name,
    "Delayed Name Recall": name_delayed,
    "Verbal Fluency": animals,
    "Immediate 3 Words": wordimm_immediate,
    "Delayed 3 Words": wordimm_delayed,
    "Object Naming": object_naming_score,
    "Semantic Memory": semantic_score,
    "Orientation": orientation_score,
    "Praxis": praxis_score,
    "Story Recall": story_score,
    "Memory Score": memory_score,
    "Language Score": language_score,
    "Total Score": total_score,
    "Cognitive Score": cognitive_score,
    "Flag": flag,
}

df = pd.DataFrame([data])
excel_buffer = BytesIO()
df.to_excel(excel_buffer, index=False)

st.download_button(
    "⬇️ Download Excel",
    excel_buffer.getvalue(),
    "cognitive_assessment.xlsx",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

# ====================================================
# PDF REPORT
# ====================================================
def generate_pdf_report(d):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()

    elements = [
        Paragraph("<b>10/66 Cognitive Assessment Report</b>", styles["Title"]),
        Spacer(1, 12),
    ]

    table_data = [
        ["Domain", "Details"],
        ["Subject", f"ID: {d['Subject ID']} | Age: {d['Age']} | Gender: {d['Gender']} | Education: {d['Education']}"],
        ["Word List Learning", f"L1={d['LEARN1']}, L2={d['LEARN2']}, L3={d['LEARN3']}"],
        ["Name Recall", f"Immediate={d['Immediate Name Recall']} | Delayed={d['Delayed Name Recall']}"],
        ["Object Naming", d["Object Naming"]],
        ["Verbal Fluency", d["Verbal Fluency"]],
        ["Immediate Words", d["Immediate 3 Words"]],
        ["Delayed Words", f"10-word={d['Delayed Recall (10)']} | 3-word={d['Delayed 3 Words']}"],
        ["Semantic Memory", d["Semantic Memory"]],
        ["Orientation", d["Orientation"]],
        ["Praxis", d["Praxis"]],
        ["Story Recall", d["Story Recall"]],
        ["Scores", f"Total={d['Total Score']} | Cognitive={d['Cognitive Score']}"],
        ["Flag", d["Flag"]],
    ]

    table = Table(table_data, colWidths=[150, 350])
    table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))

    elements.append(table)
    doc.build(elements)
    buffer.seek(0)
    return buffer

pdf_buffer = generate_pdf_report(data)

st.download_button(
    "⬇️ Download PDF Report",
    pdf_buffer,
    "cognitive_assessment_report.pdf",
    "application/pdf"
)

st.success("Assessment complete ✔")
