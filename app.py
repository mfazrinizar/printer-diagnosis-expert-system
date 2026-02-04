import streamlit as st
from pathlib import Path

from src.knowledge_base import KnowledgeBase
from src.inference_engine import InferenceEngine


def init_session_state():
    if "current_index" not in st.session_state:
        st.session_state.current_index = 0
    if "answers" not in st.session_state:
        st.session_state.answers = {}
    if "finished" not in st.session_state:
        st.session_state.finished = False


def reset_session():
    st.session_state.current_index = 0
    st.session_state.answers = {}
    st.session_state.finished = False


def render_chat_message(role: str, content: str):
    with st.chat_message(role):
        st.markdown(content)


def render_symptom_question(symptom: dict, index: int, total: int):
    code = symptom["code"]
    description = symptom["description"]

    render_chat_message(
        "assistant",
        f"**Pertanyaan {index + 1} dari {total}**\n\n"
        f"Apakah printer Anda mengalami gejala berikut?\n\n"
        f"**{code}: {description}**"
    )

    current_answer = st.session_state.answers.get(code)

    col1, col2, col3 = st.columns([1, 1, 2])

    with col1:
        if st.button("Ya", key=f"yes_{code}", use_container_width=True):
            st.session_state.answers[code] = True
            st.rerun()

    with col2:
        if st.button("Tidak", key=f"no_{code}", use_container_width=True):
            st.session_state.answers[code] = False
            st.rerun()

    if current_answer is not None:
        answer_text = "Ya" if current_answer else "Tidak"
        render_chat_message("user", f"Jawaban: **{answer_text}**")


def render_navigation(index: int, total: int):
    has_answer = st.session_state.answers.get(
        list(st.session_state.answers.keys())[index]
        if index < len(st.session_state.answers)
        else None
    ) is not None

    symptoms = kb.get_symptoms()
    current_code = symptoms[index]["code"]
    has_current_answer = current_code in st.session_state.answers

    col1, col2, col3 = st.columns([1, 1, 2])

    with col1:
        if index > 0:
            if st.button("Sebelumnya", use_container_width=True):
                st.session_state.current_index -= 1
                st.rerun()

    with col2:
        if has_current_answer:
            if index < total - 1:
                if st.button("Selanjutnya", use_container_width=True):
                    st.session_state.current_index += 1
                    st.rerun()
            else:
                if st.button("Lihat Hasil", use_container_width=True, type="primary"):
                    st.session_state.finished = True
                    st.rerun()


def render_previous_answers(symptoms: list[dict], current_index: int):
    for i in range(current_index):
        symptom = symptoms[i]
        code = symptom["code"]
        if code in st.session_state.answers:
            answer = "Ya" if st.session_state.answers[code] else "Tidak"
            with st.chat_message("assistant"):
                st.caption(f"{symptom['description']}")
            with st.chat_message("user"):
                st.caption(f"{answer}")


def render_diagnosis_result(engine: InferenceEngine):
    selected = [
        code for code, answer in st.session_state.answers.items() if answer
    ]

    render_chat_message(
        "assistant",
        "**Analisis selesai!**\n\n"
        f"Gejala yang Anda pilih: **{len(selected)}** dari {len(st.session_state.answers)}"
    )

    if selected:
        render_chat_message(
            "user",
            "Gejala yang dialami:\n" +
            "\n".join([f"- {code}" for code in selected])
        )

    results = engine.diagnose(selected)

    if results:
        render_chat_message("assistant", "**Hasil Diagnosis:**")
        for result in results:
            with st.chat_message("assistant"):
                st.markdown(f"### {result['diagnosis']}")
                st.markdown(f"**Kode:** {result['code']}")
                st.markdown(f"**Kondisi terpenuhi:** {', '.join(result['matched_conditions'])}")
                st.info(f"**Solusi:** {result['solution']}")
    else:
        render_chat_message(
            "assistant",
            "Tidak ditemukan diagnosis yang cocok dengan gejala yang dipilih.\n\n"
            "Pastikan Anda memilih semua gejala yang dialami, atau konsultasikan dengan teknisi."
        )

    st.divider()
    if st.button("Mulai Diagnosis Baru", type="primary"):
        reset_session()
        st.rerun()


# Main App
st.set_page_config(
    page_title="Sistem Pakar Diagnosis Printer",
    page_icon="",
    layout="centered"
)

st.title("Sistem Pakar Diagnosis Printer")
st.caption("Jawab pertanyaan berikut untuk mendiagnosis masalah printer Anda.")

# Initialize
init_session_state()

kb_path = Path(__file__).parent / "data" / "knowledge_base.json"
kb = KnowledgeBase(str(kb_path))
engine = InferenceEngine(kb)

symptoms = kb.get_symptoms()
total_symptoms = len(symptoms)

st.divider()

if st.session_state.finished:
    render_previous_answers(symptoms, total_symptoms)
    render_diagnosis_result(engine)
else:
    current_index = st.session_state.current_index

    render_previous_answers(symptoms, current_index)
    render_symptom_question(symptoms[current_index], current_index, total_symptoms)
    render_navigation(current_index, total_symptoms)
