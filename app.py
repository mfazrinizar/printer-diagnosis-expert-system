import streamlit as st
from pathlib import Path

from src.knowledge_base import KnowledgeBase
from src.rbr_engine import RBREngine
from src.cbr_engine import CBREngine


# Page Config & CSS

st.set_page_config(
    page_title="Sistem Pakar Diagnosis Printer",
    page_icon="🖨️",
    layout="wide",
    initial_sidebar_state="expanded"
)

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

:root {
    --primary: #6366f1;
    --primary-light: #818cf8;
    --primary-dark: #4f46e5;
    --accent: #06b6d4;
    --success: #10b981;
    --warning: #f59e0b;
    --danger: #ef4444;
    --bg-dark: #0f172a;
    --bg-card: #1e293b;
    --bg-card-hover: #334155;
    --text-primary: #f1f5f9;
    --text-secondary: #94a3b8;
    --border: #334155;
    --gradient-1: linear-gradient(135deg, #6366f1, #06b6d4);
    --gradient-2: linear-gradient(135deg, #f59e0b, #ef4444);
    --gradient-3: linear-gradient(135deg, #10b981, #06b6d4);
}

.main .block-container {
    padding-top: 1rem;
    max-width: 1200px;
}

div[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
}

div[data-testid="stSidebar"] .stMarkdown h1,
div[data-testid="stSidebar"] .stMarkdown h2,
div[data-testid="stSidebar"] .stMarkdown h3 {
    color: #f1f5f9;
}

.hero-banner {
    background: linear-gradient(135deg, #1e1b4b 0%, #312e81 30%, #4338ca 60%, #06b6d4 100%);
    padding: 2rem 2.5rem;
    border-radius: 16px;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
}

.hero-banner::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -20%;
    width: 300px;
    height: 300px;
    border-radius: 50%;
    background: rgba(6, 182, 212, 0.15);
    filter: blur(60px);
}

.hero-banner h1 {
    font-family: 'Inter', sans-serif;
    font-weight: 800;
    font-size: 2rem;
    color: #ffffff;
    margin: 0 0 0.5rem 0;
    letter-spacing: -0.02em;
}

.hero-banner p {
    font-family: 'Inter', sans-serif;
    color: #c7d2fe;
    font-size: 1rem;
    margin: 0;
    line-height: 1.6;
}

.metric-card {
    background: linear-gradient(145deg, #1e293b, #0f172a);
    border: 1px solid #334155;
    border-radius: 12px;
    padding: 1.25rem;
    text-align: center;
    transition: all 0.3s ease;
}

.metric-card:hover {
    border-color: #6366f1;
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(99, 102, 241, 0.15);
}

.metric-value {
    font-family: 'Inter', sans-serif;
    font-size: 2rem;
    font-weight: 800;
    background: var(--gradient-1);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.metric-label {
    font-family: 'Inter', sans-serif;
    font-size: 0.8rem;
    color: #94a3b8;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-top: 0.25rem;
}

.method-card {
    background: linear-gradient(145deg, #1e293b, #0f172a);
    border: 1px solid #334155;
    border-radius: 16px;
    padding: 2rem;
    transition: all 0.3s ease;
    height: 100%;
}

.method-card:hover {
    border-color: #6366f1;
    box-shadow: 0 12px 40px rgba(99, 102, 241, 0.1);
}

.method-card h3 {
    font-family: 'Inter', sans-serif;
    font-weight: 700;
    color: #f1f5f9;
    margin: 0.75rem 0;
}

.method-card p {
    color: #94a3b8;
    font-size: 0.9rem;
    line-height: 1.6;
}

.method-icon {
    font-size: 2.5rem;
    margin-bottom: 0.5rem;
}

.result-card {
    background: linear-gradient(145deg, #1e293b, #0f172a);
    border-left: 4px solid #6366f1;
    border-radius: 0 12px 12px 0;
    padding: 1.5rem;
    margin-bottom: 1rem;
}

.result-card-success {
    border-left-color: #10b981;
}

.result-card-warning {
    border-left-color: #f59e0b;
}

.result-card-danger {
    border-left-color: #ef4444;
}

.similarity-bar {
    background: #1e293b;
    border-radius: 8px;
    height: 8px;
    overflow: hidden;
    margin: 0.5rem 0;
}

.similarity-fill {
    height: 100%;
    border-radius: 8px;
    transition: width 0.5s ease;
}

.tag {
    display: inline-block;
    padding: 0.2rem 0.6rem;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 600;
    margin: 0.15rem;
}

.tag-high { background: rgba(239, 68, 68, 0.15); color: #fca5a5; }
.tag-medium { background: rgba(245, 158, 11, 0.15); color: #fcd34d; }
.tag-low { background: rgba(16, 185, 129, 0.15); color: #6ee7b7; }
.tag-primary { background: rgba(99, 102, 241, 0.15); color: #a5b4fc; }
.tag-accent { background: rgba(6, 182, 212, 0.15); color: #67e8f9; }

.trace-step {
    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 8px;
    padding: 0.75rem 1rem;
    margin-bottom: 0.5rem;
    font-size: 0.85rem;
}

.trace-fired {
    border-color: #10b981;
    background: rgba(16, 185, 129, 0.05);
}

.trace-not-fired {
    border-color: #475569;
    opacity: 0.7;
}

.case-card {
    background: linear-gradient(145deg, #1e293b, #0f172a);
    border: 1px solid #334155;
    border-radius: 12px;
    padding: 1.25rem;
    margin-bottom: 0.75rem;
    transition: all 0.3s ease;
}

.case-card:hover {
    border-color: #06b6d4;
    box-shadow: 0 4px 15px rgba(6, 182, 212, 0.1);
}

.section-header {
    font-family: 'Inter', sans-serif;
    font-weight: 700;
    color: #f1f5f9;
    border-bottom: 2px solid #334155;
    padding-bottom: 0.75rem;
    margin-bottom: 1.25rem;
}

.info-box {
    background: rgba(99, 102, 241, 0.08);
    border: 1px solid rgba(99, 102, 241, 0.2);
    border-radius: 12px;
    padding: 1.25rem;
    margin: 1rem 0;
}

.ref-list {
    list-style: none;
    padding: 0;
    margin: 0.5rem 0 0 0;
}

.ref-list li {
    padding: 0.3rem 0;
    color: #94a3b8;
    font-size: 0.85rem;
}

.ref-list li::before {
    content: '📖 ';
}
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)



# Initialize Data

@st.cache_resource
def load_engines():
    base = Path(__file__).parent
    kb_path = base / "data" / "knowledge_base.json"
    cl_path = base / "data" / "case_library.json"
    kb = KnowledgeBase(str(kb_path))
    rbr = RBREngine(kb)
    cbr = CBREngine(str(cl_path), kb)
    return kb, rbr, cbr


kb, rbr_engine, cbr_engine = load_engines()


def init_session():
    defaults = {
        "page": "home",
        "rbr_answers": {},
        "rbr_step": 0,
        "rbr_finished": False,
        "cbr_selected": [],
        "cbr_results": None,
        "cbr_proposed": None,
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val


init_session()



# Helpers

SEVERITY_MAP = {
    "high": ("🔴", "Tinggi", "tag-high"),
    "medium": ("🟡", "Sedang", "tag-medium"),
    "low": ("🟢", "Rendah", "tag-low"),
}

CATEGORY_MAP = {
    "power": ("⚡", "Power"),
    "connectivity": ("🔌", "Konektivitas"),
    "print_quality": ("🎨", "Kualitas Cetak"),
    "mechanical": ("⚙️", "Mekanik"),
    "software": ("💻", "Software"),
    "other": ("❓", "Lainnya"),
}


def severity_tag(level: str) -> str:
    icon, label, cls = SEVERITY_MAP.get(level, ("⚪", level, "tag-primary"))
    return f'<span class="tag {cls}">{icon} {label}</span>'


def category_tag(cat: str) -> str:
    icon, label = CATEGORY_MAP.get(cat, ("❓", cat))
    return f'<span class="tag tag-accent">{icon} {label}</span>'


def similarity_bar_html(value: float) -> str:
    pct = int(value * 100)
    if value >= 0.8:
        color = "linear-gradient(90deg, #10b981, #06b6d4)"
    elif value >= 0.6:
        color = "linear-gradient(90deg, #06b6d4, #6366f1)"
    elif value >= 0.4:
        color = "linear-gradient(90deg, #f59e0b, #ef4444)"
    else:
        color = "linear-gradient(90deg, #ef4444, #dc2626)"

    return f"""
    <div style="display:flex;align-items:center;gap:0.75rem;">
        <div style="flex:1;background:#1e293b;border-radius:8px;height:10px;overflow:hidden;">
            <div style="width:{pct}%;height:100%;border-radius:8px;background:{color};transition:width 0.5s ease;"></div>
        </div>
        <span style="font-weight:700;color:#f1f5f9;font-size:0.95rem;min-width:50px;text-align:right;">{pct}%</span>
    </div>
    """



# Sidebar

with st.sidebar:
    st.markdown("## 🖨️ Menu Navigasi")
    st.markdown("---")

    menu_items = [
        ("🏠", "Beranda", "home"),
        ("📋", "RBR — Rule-Based", "rbr"),
        ("📦", "CBR — Case-Based", "cbr"),
        ("📚", "Basis Pengetahuan", "knowledge"),
        ("🗂️", "Case Library", "cases"),
        ("ℹ️", "Tentang Sistem", "about"),
    ]

    for icon, label, key in menu_items:
        if st.button(f"{icon}  {label}", key=f"nav_{key}", use_container_width=True):
            st.session_state.page = key
            st.rerun()

    st.markdown("---")

    stats = cbr_engine.get_case_statistics()
    st.markdown("### 📊 Ringkasan")
    st.caption(f"**{len(kb.get_symptoms())}** Gejala terdaftar")
    st.caption(f"**{len(kb.get_rules())}** Aturan diagnosis")
    st.caption(f"**{stats.get('total_cases', 0)}** Kasus tersimpan")



# PAGE: Home

def page_home():
    st.markdown("""
    <div class="hero-banner">
        <h1>🖨️ Sistem Pakar Diagnosis Printer</h1>
        <p>Sistem pakar berbasis pengetahuan untuk mendiagnosis kerusakan printer
        menggunakan dua metode penalaran: <strong>Rule-Based Reasoning (RBR)</strong>
        dan <strong>Case-Based Reasoning (CBR)</strong>.</p>
    </div>
    """, unsafe_allow_html=True)

    # Metrics
    stats = cbr_engine.get_case_statistics()
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{len(kb.get_symptoms())}</div>
            <div class="metric-label">Gejala</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{len(kb.get_rules())}</div>
            <div class="metric-label">Aturan RBR</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{stats.get('total_cases', 0)}</div>
            <div class="metric-label">Kasus CBR</div>
        </div>""", unsafe_allow_html=True)
    with c4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">2</div>
            <div class="metric-label">Metode</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("")

    # Method Cards
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="method-card">
            <div class="method-icon">📋</div>
            <h3>Rule-Based Reasoning (RBR)</h3>
            <p>Menggunakan <strong>Forward Chaining</strong> untuk mencocokkan gejala yang dialami pengguna
            dengan aturan-aturan (IF-THEN rules) yang telah didefinisikan oleh pakar.</p>
            <p style="margin-top:0.75rem;"><span class="tag tag-primary">Forward Chaining</span>
            <span class="tag tag-primary">AND Logic</span>
            <span class="tag tag-primary">Exact Match</span></p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("▶️  Mulai Diagnosis RBR", key="home_rbr", use_container_width=True):
            st.session_state.page = "rbr"
            st.session_state.rbr_answers = {}
            st.session_state.rbr_step = 0
            st.session_state.rbr_finished = False
            st.rerun()

    with col2:
        st.markdown("""
        <div class="method-card">
            <div class="method-icon">📦</div>
            <h3>Case-Based Reasoning (CBR)</h3>
            <p>Menggunakan <strong>siklus Retrieve-Reuse-Revise-Retain</strong> untuk mencari kasus serupa
            di case library dan mengadaptasi solusinya untuk masalah saat ini.</p>
            <p style="margin-top:0.75rem;"><span class="tag tag-accent">Nearest Neighbor</span>
            <span class="tag tag-accent">Weighted Similarity</span>
            <span class="tag tag-accent">Case Library</span></p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("▶️  Mulai Diagnosis CBR", key="home_cbr", use_container_width=True):
            st.session_state.page = "cbr"
            st.session_state.cbr_selected = []
            st.session_state.cbr_results = None
            st.session_state.cbr_proposed = None
            st.rerun()

    st.markdown("---")

    # References
    st.markdown("""
    <div class="info-box">
    <h4 style="margin-top:0;">📖 Referensi Utama</h4>
    <ul class="ref-list">
        <li>Turban, E., Aronson, J.E., & Liang, T.P. (2005). <em>Decision Support Systems and Intelligent Systems</em>. Pearson.</li>
        <li>Giarratano, J.C., & Riley, G.D. (2005). <em>Expert Systems: Principles and Programming</em>. Thomson.</li>
        <li>Aamodt, A., & Plaza, E. (1994). Case-Based Reasoning: Foundational Issues. <em>AI Communications</em>, 7(1), 39-59.</li>
        <li>Kolodner, J. (1993). <em>Case-Based Reasoning</em>. Morgan Kaufmann.</li>
        <li>Watson, I. (1997). <em>Applying Case-Based Reasoning</em>. Morgan Kaufmann.</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)



# PAGE: RBR Diagnosis

def page_rbr():
    st.markdown("""
    <div class="hero-banner" style="background: linear-gradient(135deg, #312e81, #4338ca, #6366f1);">
        <h1>📋 Rule-Based Reasoning (RBR)</h1>
        <p>Diagnosis menggunakan metode <strong>Forward Chaining</strong> — menjawab pertanyaan gejala
        satu per satu, lalu sistem akan mencocokkan dengan aturan diagnosis yang ada.</p>
    </div>
    """, unsafe_allow_html=True)

    symptoms = kb.get_symptoms()
    total = len(symptoms)
    step = st.session_state.rbr_step

    if st.session_state.rbr_finished:
        render_rbr_results()
        return

    # Progress
    answered = len(st.session_state.rbr_answers)
    progress = answered / total
    st.progress(progress, text=f"Progress: {answered}/{total} gejala dijawab")

    # Show previous answers as compact summary
    if step > 0:
        with st.expander(f"📝 Jawaban sebelumnya ({step} pertanyaan)", expanded=False):
            for i in range(step):
                sym = symptoms[i]
                code = sym["code"]
                ans = st.session_state.rbr_answers.get(code)
                if ans is not None:
                    icon = "✅" if ans else "❌"
                    st.caption(f"{icon} **{code}**: {sym['description']}")

    # Current question
    if step < total:
        current = symptoms[step]
        cat_icon, cat_label = CATEGORY_MAP.get(current.get("category", "other"), ("❓", "Lainnya"))

        st.markdown(f"""
        <div style="background: linear-gradient(145deg, #1e293b, #0f172a); border: 1px solid #334155;
                    border-radius: 16px; padding: 2rem; margin: 1rem 0;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:1rem;">
                <span style="color: #94a3b8; font-size: 0.85rem;">Pertanyaan {step + 1} dari {total}</span>
                <span class="tag tag-accent">{cat_icon} {cat_label}</span>
            </div>
            <h3 style="color: #f1f5f9; margin: 0 0 0.5rem 0;">Apakah printer Anda mengalami gejala berikut?</h3>
            <p style="color: #c7d2fe; font-size: 1.15rem; font-weight: 600;">
                {current['code']}: {current['description']}
            </p>
        </div>
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            if st.button("✅ Ya", key=f"rbr_yes_{step}", use_container_width=True):
                st.session_state.rbr_answers[current["code"]] = True
                if step + 1 < total:
                    st.session_state.rbr_step += 1
                else:
                    st.session_state.rbr_finished = True
                st.rerun()
        with col2:
            if st.button("❌ Tidak", key=f"rbr_no_{step}", use_container_width=True):
                st.session_state.rbr_answers[current["code"]] = False
                if step + 1 < total:
                    st.session_state.rbr_step += 1
                else:
                    st.session_state.rbr_finished = True
                st.rerun()

        # Navigation
        st.markdown("")
        nav1, nav2 = st.columns([1, 3])
        with nav1:
            if step > 0:
                if st.button("⬅️ Kembali", key="rbr_back", use_container_width=True):
                    st.session_state.rbr_step -= 1
                    st.rerun()

    # Reset
    st.markdown("---")
    if st.button("🔄 Reset Diagnosis", key="rbr_reset"):
        st.session_state.rbr_answers = {}
        st.session_state.rbr_step = 0
        st.session_state.rbr_finished = False
        st.rerun()


def render_rbr_results():
    selected = [code for code, ans in st.session_state.rbr_answers.items() if ans]
    symptoms = kb.get_symptoms()

    # Summary
    st.markdown(f"""
    <div style="background: rgba(99, 102, 241, 0.08); border: 1px solid rgba(99, 102, 241, 0.2);
                border-radius: 12px; padding: 1.25rem; margin-bottom: 1rem;">
        <h4 style="margin-top:0; color: #a5b4fc;">📊 Ringkasan Input</h4>
        <p style="color: #94a3b8;">Gejala yang dialami: <strong style="color:#f1f5f9;">{len(selected)}</strong>
        dari {len(st.session_state.rbr_answers)} gejala yang ditanyakan</p>
    </div>
    """, unsafe_allow_html=True)

    if selected:
        with st.expander("🔍 Gejala yang dipilih", expanded=True):
            for code in selected:
                sym = kb.get_symptom_by_code(code)
                if sym:
                    cat_icon, cat_label = CATEGORY_MAP.get(sym.get("category", "other"), ("❓", "Lainnya"))
                    st.markdown(f"- **{code}**: {sym['description']} {category_tag(sym.get('category', 'other'))}", unsafe_allow_html=True)

    # Forward Chaining results
    st.markdown("### 🎯 Hasil Diagnosis (Forward Chaining)")

    exact_results = rbr_engine.forward_chaining(selected)

    if exact_results:
        for r in exact_results:
            sev_icon, sev_label, sev_cls = SEVERITY_MAP.get(r["severity"], ("⚪", "N/A", "tag-primary"))
            st.markdown(f"""
            <div class="result-card result-card-{'danger' if r['severity'] == 'high' else 'warning' if r['severity'] == 'medium' else 'success'}">
                <div style="display:flex; justify-content:space-between; align-items:start; flex-wrap:wrap; gap:0.5rem;">
                    <div>
                        <h3 style="color: #f1f5f9; margin:0 0 0.25rem 0;">{r['diagnosis']}</h3>
                        <span style="color: #94a3b8; font-size: 0.85rem;">Kode: {r['code']}</span>
                    </div>
                    <div>
                        {severity_tag(r['severity'])}
                        {category_tag(r['category'])}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            col_sol, col_cond = st.columns([3, 2])
            with col_sol:
                st.info(f"**💡 Solusi:** {r['solution']}")
            with col_cond:
                st.success("**✅ Kondisi terpenuhi:**\n" + "\n".join(
                    [f"- {d['code']}: {d['description']}" for d in r["matched_details"]]
                ))

            if r.get("references"):
                with st.expander(f"📖 Referensi ({len(r['references'])})"):
                    for ref in r["references"]:
                        st.caption(f"• {ref}")
    else:
        st.warning("Tidak ada diagnosis yang **100% cocok** dengan gejala yang dipilih.")

    # Partial matches
    if selected:
        partial_results = rbr_engine.partial_matching(selected)
        if partial_results:
            st.markdown("### 🔎 Kemungkinan Diagnosis (Partial Match)")
            for r in partial_results:
                confidence_pct = int(r["confidence"] * 100)
                partial_card = (
                    '<div class="result-card">'
                    '<div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:0.5rem;">'
                    '<div>'
                    f'<h4 style="color: #f1f5f9; margin:0;">{r["diagnosis"]}</h4>'
                    f'<span style="color: #94a3b8; font-size: 0.85rem;">Kecocokan: {confidence_pct}% '
                    f'({len(r["matched_conditions"])}/{r["total_conditions"]} kondisi)</span>'
                    '</div>'
                    f'{severity_tag(r["severity"])}'
                    '</div>'
                    f'{similarity_bar_html(r["confidence"])}'
                    '</div>'
                )
                st.markdown(partial_card, unsafe_allow_html=True)

                with st.expander(f"Detail — {r['code']}: {r['diagnosis']}"):
                    c1, c2 = st.columns(2)
                    with c1:
                        st.markdown("**✅ Kondisi terpenuhi:**")
                        for d in r["matched_details"]:
                            st.caption(f"• {d['code']}: {d['description']}")
                    with c2:
                        st.markdown("**❌ Kondisi belum terpenuhi:**")
                        for d in r["unmatched_details"]:
                            st.caption(f"• {d['code']}: {d['description']}")

    # Inference Trace
    st.markdown("### 🧠 Jejak Inferensi (Inference Trace)")
    with st.expander("Lihat detail proses Forward Chaining", expanded=False):
        trace = rbr_engine.get_inference_trace(selected)
        for t in trace:
            cls = "trace-fired" if t["fired"] else "trace-not-fired"
            st.markdown(f"""
            <div class="trace-step {cls}">
                <strong>Langkah {t['step']}</strong> — Rule {t['rule_code']}: {t['rule_diagnosis']}<br/>
                <span style="color: #94a3b8;">Kondisi: {', '.join(t['conditions_required'])} →
                Terpenuhi: {t['match_ratio']} → {t['status']}</span>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    if st.button("🔄 Mulai Diagnosis Baru", type="primary", key="rbr_restart"):
        st.session_state.rbr_answers = {}
        st.session_state.rbr_step = 0
        st.session_state.rbr_finished = False
        st.rerun()



# PAGE: CBR Diagnosis

def page_cbr():
    st.markdown("""
    <div class="hero-banner" style="background: linear-gradient(135deg, #134e4a, #0f766e, #06b6d4);">
        <h1>📦 Case-Based Reasoning (CBR)</h1>
        <p>Diagnosis menggunakan <strong>siklus Retrieve-Reuse-Revise-Retain</strong> —
        mencari kasus serupa di case library menggunakan <strong>Weighted Nearest Neighbor</strong>.</p>
    </div>
    """, unsafe_allow_html=True)

    # CBR cycle visualization
    st.markdown("""
    <div style="background: linear-gradient(145deg, #1e293b, #0f172a); border: 1px solid #334155;
                border-radius: 12px; padding: 1.25rem; margin-bottom: 1.5rem; text-align: center;">
        <span style="color: #67e8f9; font-weight: 700; font-size: 1rem;">
            🔍 Retrieve → 🔄 Reuse → ✏️ Revise → 💾 Retain
        </span>
        <p style="color: #94a3b8; font-size: 0.8rem; margin: 0.5rem 0 0 0;">
            Siklus CBR (Aamodt & Plaza, 1994)
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Step 1: Select symptoms
    st.markdown("### 🔍 Step 1: RETRIEVE — Pilih Gejala")
    st.caption("Pilih gejala yang dialami printer Anda. Sistem akan mencari kasus serupa di case library.")

    symptoms = kb.get_symptoms()
    categories = kb.get_symptom_categories()

    selected_symptoms = []

    for cat in categories:
        cat_icon, cat_label = CATEGORY_MAP.get(cat, ("❓", cat))
        cat_symptoms = kb.get_symptoms_by_category(cat)

        st.markdown(f"**{cat_icon} {cat_label}**")
        cols = st.columns(len(cat_symptoms) if len(cat_symptoms) <= 3 else 3)
        for i, sym in enumerate(cat_symptoms):
            with cols[i % len(cols)]:
                checked = st.checkbox(
                    f"{sym['code']}: {sym['description']}",
                    key=f"cbr_sym_{sym['code']}",
                    value=sym["code"] in st.session_state.cbr_selected
                )
                if checked:
                    selected_symptoms.append(sym["code"])

    st.session_state.cbr_selected = selected_symptoms

    st.markdown("---")

    if selected_symptoms:
        if st.button("🔎 Cari Kasus Serupa", type="primary", use_container_width=True, key="cbr_search"):
            results = cbr_engine.retrieve(selected_symptoms, top_k=5)
            proposed = cbr_engine.reuse(results)
            st.session_state.cbr_results = results
            st.session_state.cbr_proposed = proposed
            st.rerun()
    else:
        st.info("Pilih minimal satu gejala untuk memulai pencarian kasus.")

    # Show results
    if st.session_state.cbr_results is not None:
        render_cbr_results()


def render_cbr_results():
    results = st.session_state.cbr_results
    proposed = st.session_state.cbr_proposed
    selected = st.session_state.cbr_selected

    st.markdown("### 🔄 Step 2: REUSE — Hasil Pencarian Kasus")

    if not results:
        st.warning("Tidak ditemukan kasus yang cukup mirip di case library. "
                    "Coba pilih gejala yang berbeda atau gunakan metode RBR.")
        return

    st.success(f"Ditemukan **{len(results)}** kasus serupa di case library.")

    # Best match / Proposed solution
    if proposed:
        st.markdown("#### 💡 Solusi yang Diusulkan (dari kasus paling mirip)")

        proposed_card = (
            '<div class="result-card result-card-success">'
            '<div style="display:flex; justify-content:space-between; align-items:start; flex-wrap:wrap; gap:0.5rem;">'
            '<div>'
            f'<h3 style="color: #f1f5f9; margin:0 0 0.25rem 0;">{proposed["proposed_diagnosis"]}</h3>'
            f'<span style="color: #94a3b8; font-size: 0.85rem;">Sumber: {proposed["source_case_title"]} ({proposed["source_case_id"]})</span>'
            '</div>'
            '<div>'
            f'{severity_tag(proposed["severity"])}'
            f'<span class="tag tag-primary">Keyakinan: {proposed["confidence_level"]}</span>'
            '</div>'
            '</div>'
            '<div style="margin-top: 0.75rem;">'
            '<strong style="color: #6ee7b7;">Similarity:</strong>'
            '</div>'
            f'{similarity_bar_html(proposed["similarity"])}'
            '</div>'
        )
        st.markdown(proposed_card, unsafe_allow_html=True)

        st.info(f"**💡 Solusi:** {proposed['proposed_solution']}")
        st.caption(f"📝 **Catatan Adaptasi:** {proposed['adaptation_notes']}")

    # All retrieved cases
    st.markdown("#### 📋 Kasus yang Ditemukan")
    for i, case in enumerate(results):
        sim_pct = int(case["similarity"] * 100)
        with st.expander(
            f"#{i+1} — {case['title']} (Similarity: {sim_pct}%)",
            expanded=(i == 0)
        ):
            c1, c2 = st.columns([2, 1])
            with c1:
                st.markdown(f"**📝 Deskripsi:** {case['description']}")
                st.markdown(f"**🔍 Diagnosis:** {case['diagnosis']}")
                st.markdown(f"**💡 Solusi:** {case['solution']}")
                if case.get("technician_notes"):
                    st.caption(f"🔧 Catatan Teknisi: {case['technician_notes']}")
            with c2:
                st.markdown(f"**ID:** `{case['case_id']}`")
                st.markdown(f"**Printer:** {case.get('brand', 'N/A')} — {case.get('printer_type', 'N/A')}")
                st.markdown(f"**Tanggal:** {case.get('date', 'N/A')}")
                st.markdown(f"**Outcome:** {case.get('outcome', 'N/A')}")
                st.markdown(severity_tag(case.get("severity", "medium")), unsafe_allow_html=True)

            # Similarity breakdown
            st.markdown("**📊 Detail Perhitungan Similarity (Weighted Nearest Neighbor):**")
            breakdown = cbr_engine.get_similarity_breakdown(selected, case)

            bd_data = []
            for b in breakdown:
                bd_data.append({
                    "Kode": b["code"],
                    "Gejala": b["description"],
                    "Bobot (wᵢ)": b["weight"],
                    "Kasus Baru": "✅" if b["in_new_case"] else "❌",
                    "Kasus Lama": "✅" if b["in_old_case"] else "❌",
                    "Match": "✅" if b["matched"] else "❌",
                    "Kontribusi": f"{b['contribution']:.4f}"
                })
            st.dataframe(bd_data, use_container_width=True, hide_index=True)

            total_sim = case["similarity"]
            st.markdown(f"""
            <div style="background: rgba(6, 182, 212, 0.08); border: 1px solid rgba(6, 182, 212, 0.2);
                        border-radius: 8px; padding: 0.75rem; margin-top: 0.5rem;">
                <strong style="color: #67e8f9;">Formula:</strong>
                <span style="color: #e2e8f0;">
                    Similarity = Σ(wᵢ × matchᵢ) / Σwᵢ = <strong>{total_sim:.4f}</strong> ({sim_pct}%)
                </span>
            </div>
            """, unsafe_allow_html=True)

    # Step 3: Revise & Retain
    st.markdown("---")
    st.markdown("### ✏️ Step 3: REVISE — Evaluasi & Penyesuaian")
    st.caption("Apakah solusi yang diusulkan sesuai? Anda bisa menyesuaikan diagnosis dan solusi sebelum menyimpan kasus baru.")

    with st.form("cbr_retain_form"):
        st.markdown("### 💾 Step 4: RETAIN — Simpan Kasus Baru")

        new_title = st.text_input("Judul Kasus", value="", placeholder="Contoh: Printer HP tidak menyala setelah mati lampu")
        new_desc = st.text_area("Deskripsi Kasus", value="", placeholder="Jelaskan kondisi printer secara detail...")

        col_p1, col_p2 = st.columns(2)
        with col_p1:
            new_brand = st.selectbox("Merk Printer", ["HP", "Epson", "Canon", "Brother", "Samsung", "Lainnya"])
        with col_p2:
            new_type = st.selectbox("Tipe Printer", ["InkJet", "LaserJet", "Dot Matrix", "Thermal", "Lainnya"])

        new_diagnosis = st.text_input(
            "Diagnosis",
            value=proposed["proposed_diagnosis"] if proposed else ""
        )
        new_solution = st.text_area(
            "Solusi",
            value=proposed["proposed_solution"] if proposed else ""
        )

        col_s1, col_s2 = st.columns(2)
        with col_s1:
            new_severity = st.selectbox("Tingkat Keparahan", ["low", "medium", "high"], index=1)
        with col_s2:
            new_outcome = st.selectbox("Hasil", ["success", "failed", "pending"], index=0)

        new_notes = st.text_area("Catatan Teknisi", placeholder="Catatan tambahan...")

        submitted = st.form_submit_button("💾 Simpan Kasus Baru", use_container_width=True)

        if submitted:
            if new_title and new_diagnosis and new_solution:
                new_case = {
                    "title": new_title,
                    "description": new_desc,
                    "printer_type": new_type,
                    "brand": new_brand,
                    "symptoms": selected,
                    "diagnosis": new_diagnosis,
                    "solution": new_solution,
                    "severity": new_severity,
                    "outcome": new_outcome,
                    "technician_notes": new_notes
                }
                case_id = cbr_engine.retain(new_case)
                st.success(f"✅ Kasus baru berhasil disimpan dengan ID: **{case_id}**")
                st.cache_resource.clear()
            else:
                st.error("Mohon isi Judul, Diagnosis, dan Solusi terlebih dahulu.")



# PAGE: Knowledge Base

def page_knowledge():
    st.markdown("""
    <div class="hero-banner" style="background: linear-gradient(135deg, #581c87, #7e22ce, #a855f7);">
        <h1>📚 Basis Pengetahuan</h1>
        <p>Daftar lengkap gejala dan aturan diagnosis yang digunakan oleh
        metode <strong>Rule-Based Reasoning</strong>.</p>
    </div>
    """, unsafe_allow_html=True)

    tab_symptoms, tab_rules = st.tabs(["🔍 Daftar Gejala", "📋 Aturan Diagnosis (Rules)"])

    with tab_symptoms:
        st.markdown("#### 🔍 Tabel Gejala")
        symptoms_data = []
        for s in kb.get_symptoms():
            cat_icon, cat_label = CATEGORY_MAP.get(s.get("category", "other"), ("❓", "Lainnya"))
            symptoms_data.append({
                "Kode": s["code"],
                "Gejala": s["description"],
                "Kategori": f"{cat_icon} {cat_label}",
                "Bobot": s.get("weight", 0.5)
            })
        st.dataframe(symptoms_data, use_container_width=True, hide_index=True)

    with tab_rules:
        st.markdown("#### 📋 Tabel Aturan Diagnosis (IF-THEN)")
        for rule in kb.get_rules():
            sev = rule.get("severity", "medium")
            sev_icon, sev_label, _ = SEVERITY_MAP.get(sev, ("⚪", "N/A", ""))

            with st.expander(f"**{rule['code']}**: {rule['diagnosis']} {sev_icon}"):
                st.markdown(f"**IF** " + " **AND** ".join(
                    [f"`{c}` ({kb.get_symptom_by_code(c)['description'] if kb.get_symptom_by_code(c) else c})"
                     for c in rule["conditions"]]
                ) + f"\n\n**THEN** {rule['diagnosis']}")
                st.info(f"**Solusi:** {rule['solution']}")
                st.markdown(f"**Severity:** {severity_tag(sev)} &nbsp; **Kategori:** {category_tag(rule.get('category', 'other'))}", unsafe_allow_html=True)
                if rule.get("references"):
                    st.markdown("**Referensi:**")
                    for ref in rule["references"]:
                        st.caption(f"📖 {ref}")



# PAGE: Case Library

def page_cases():
    st.markdown("""
    <div class="hero-banner" style="background: linear-gradient(135deg, #713f12, #a16207, #eab308);">
        <h1>🗂️ Case Library</h1>
        <p>Database kasus-kasus diagnosis printer yang pernah ditangani.
        Digunakan sebagai referensi oleh metode <strong>Case-Based Reasoning</strong>.</p>
    </div>
    """, unsafe_allow_html=True)

    cases = cbr_engine.get_all_cases()
    stats = cbr_engine.get_case_statistics()

    # Stats
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Total Kasus", stats["total_cases"])
    with c2:
        st.metric("Berhasil", stats["outcomes"].get("success", 0))
    with c3:
        st.metric("Pending", stats["outcomes"].get("pending", 0))

    st.markdown("---")

    # Filter
    fcol1, fcol2 = st.columns(2)
    with fcol1:
        brands = ["Semua"] + list(stats.get("brands", {}).keys())
        filter_brand = st.selectbox("Filter Merk", brands)
    with fcol2:
        severities = ["Semua", "high", "medium", "low"]
        filter_sev = st.selectbox("Filter Severity", severities)

    filtered = cases
    if filter_brand != "Semua":
        filtered = [c for c in filtered if c.get("brand") == filter_brand]
    if filter_sev != "Semua":
        filtered = [c for c in filtered if c.get("severity") == filter_sev]

    st.caption(f"Menampilkan {len(filtered)} kasus")

    for case in filtered:
        sev = case.get("severity", "medium")
        with st.expander(f"**{case['case_id']}** — {case['title']}"):
            c1, c2 = st.columns([3, 1])
            with c1:
                st.markdown(f"**📝 Deskripsi:** {case['description']}")
                st.markdown(f"**🔍 Diagnosis:** {case['diagnosis']}")
                st.markdown(f"**💡 Solusi:** {case['solution']}")
                st.markdown(f"**Gejala:** {', '.join(case.get('symptoms', []))}")
                if case.get("technician_notes"):
                    st.caption(f"🔧 Catatan: {case['technician_notes']}")
            with c2:
                st.markdown(f"**Printer:** {case.get('brand', 'N/A')} - {case.get('printer_type', 'N/A')}")
                st.markdown(f"**Tanggal:** {case.get('date', 'N/A')}")
                st.markdown(f"**Outcome:** {case.get('outcome', 'N/A')}")
                st.markdown(severity_tag(sev), unsafe_allow_html=True)



# PAGE: About

def page_about():
    st.markdown("""
    <div class="hero-banner" style="background: linear-gradient(135deg, #1e293b, #334155, #475569);">
        <h1>ℹ️ Tentang Sistem</h1>
        <p>Informasi detail tentang arsitektur, metode, dan referensi yang digunakan
        dalam sistem pakar diagnosis printer ini.</p>
    </div>
    """, unsafe_allow_html=True)

    tab_arch, tab_rbr, tab_cbr, tab_ref = st.tabs([
        "🏗️ Arsitektur", "📋 Metode RBR", "📦 Metode CBR", "📖 Referensi"
    ])

    with tab_arch:
        st.markdown("""
        ### Arsitektur Sistem

        Sistem ini terdiri dari komponen-komponen berikut:

        | Komponen | Deskripsi |
        |---|---|
        | **Knowledge Base** | Menyimpan fakta (gejala) dan aturan (IF-THEN rules) untuk metode RBR |
        | **Case Library** | Database kasus-kasus yang pernah ditangani untuk metode CBR |
        | **RBR Engine** | Mesin inferensi Forward Chaining untuk penalaran berbasis aturan |
        | **CBR Engine** | Mesin penalaran berbasis kasus dengan siklus Retrieve-Reuse-Revise-Retain |
        | **UI Layer** | Antarmuka pengguna berbasis Streamlit |

        #### Alur Sistem
        ```
        User Input (Gejala)
            │
            ├──→ RBR Engine ──→ Forward Chaining ──→ Rule Matching ──→ Diagnosis
            │
            └──→ CBR Engine ──→ Retrieve (Similarity) ──→ Reuse ──→ Revise ──→ Retain
        ```

        #### Teknologi
        - **Python 3.10+** — Bahasa pemrograman utama
        - **Streamlit** — Framework antarmuka pengguna
        - **JSON** — Format penyimpanan knowledge base dan case library
        """)

    with tab_rbr:
        st.markdown("""
        ### Rule-Based Reasoning (RBR)

        #### Definisi
        Rule-Based Reasoning adalah pendekatan dalam sistem pakar yang menggunakan
        aturan IF-THEN (production rules) untuk merepresentasikan pengetahuan pakar.
        Sistem mencocokkan fakta (gejala) yang diberikan dengan aturan-aturan yang ada
        untuk menghasilkan kesimpulan (diagnosis).

        #### Metode: Forward Chaining
        Forward chaining (data-driven reasoning) bekerja dengan cara:
        1. **Kumpulkan fakta** — User menjawab pertanyaan tentang gejala
        2. **Cocokkan aturan** — Sistem memeriksa setiap rule apakah semua kondisi (antecedent) terpenuhi
        3. **Fire rule** — Jika semua kondisi terpenuhi, rule "terpicu" dan diagnosis dihasilkan
        4. **Ulangi** — Proses berlanjut untuk semua rule yang ada

        #### Representasi Aturan (AND Logic)
        ```
        IF B1 (Printer tidak menyala)
           AND B2 (Lampu indikator berkedip)
        THEN A1 (Kerusakan pada power supply)
        ```

        #### Kelebihan & Kekurangan
        | Kelebihan | Kekurangan |
        |---|---|
        | Transparan dan mudah dipahami | Rigid, terbatas pada aturan yang ada |
        | Deterministik dan konsisten | Sulit menangani kasus baru |
        | Mudah divalidasi | Membutuhkan pengetahuan pakar eksplisit |
        """)

    with tab_cbr:
        st.markdown("""
        ### Case-Based Reasoning (CBR)

        #### Definisi
        Case-Based Reasoning adalah pendekatan dalam sistem pakar yang menyelesaikan
        masalah baru dengan mengingat dan mengadaptasi solusi dari masalah serupa
        yang pernah diselesaikan sebelumnya (Aamodt & Plaza, 1994).

        #### Siklus CBR (4R)
        1. **RETRIEVE** — Mengambil kasus-kasus paling mirip dari case library
        2. **REUSE** — Mengadaptasi solusi dari kasus terdekat
        3. **REVISE** — Mengevaluasi dan menyesuaikan solusi
        4. **RETAIN** — Menyimpan kasus baru ke case library

        #### Metode Similarity: Weighted Nearest Neighbor
        ```
        Similarity(C_new, C_old) = Σ (wᵢ × sim(fᵢ_new, fᵢ_old)) / Σ wᵢ
        ```
        di mana:
        - **wᵢ** = bobot fitur ke-i (dari symptom weight)
        - **sim(fᵢ)** = 1 jika gejala cocok, 0 jika tidak
        - **Σ wᵢ** = total bobot semua fitur yang relevan

        #### Kelebihan & Kekurangan
        | Kelebihan | Kekurangan |
        |---|---|
        | Belajar dari pengalaman | Membutuhkan case library yang memadai |
        | Menangani kasus baru | Kualitas bergantung pada kualitas kasus |
        | Semakin baik seiring waktu | Similarity computation bisa kompleks |
        """)

    with tab_ref:
        st.markdown("""
        ### 📖 Referensi

        #### Buku & Jurnal Utama
        1. **Turban, E., Aronson, J.E., & Liang, T.P.** (2005). *Decision Support Systems
        and Intelligent Systems* (7th ed.). Pearson Prentice Hall.
            - Referensi utama untuk konsep sistem pakar dan forward chaining.

        2. **Giarratano, J.C., & Riley, G.D.** (2005). *Expert Systems: Principles and
        Programming* (4th ed.). Thomson Course Technology.
            - Referensi untuk implementasi rule-based expert systems.

        3. **Aamodt, A., & Plaza, E.** (1994). Case-Based Reasoning: Foundational Issues,
        Methodological Variations, and System Approaches. *AI Communications*, 7(1), 39-59.
            - Paper fundamental untuk CBR dan siklus 4R (Retrieve-Reuse-Revise-Retain).

        4. **Kolodner, J.** (1993). *Case-Based Reasoning*. Morgan Kaufmann Publishers.
            - Referensi komprehensif untuk teori dan aplikasi CBR.

        5. **Watson, I.** (1997). *Applying Case-Based Reasoning: Techniques for Enterprise
        Systems*. Morgan Kaufmann Publishers.
            - Referensi untuk penerapan CBR di sistem enterprise.

        #### Referensi Teknis (Printer Troubleshooting)
        - HP Support — support.hp.com
        - Canon Support — support.canon.com
        - Epson Support — support.epson.net
        - Brother Support — support.brother.com
        - Microsoft Support — support.microsoft.com

        #### Teknologi yang Digunakan
        - **Python** — python.org
        - **Streamlit** — streamlit.io
        """)



# Router

pages = {
    "home": page_home,
    "rbr": page_rbr,
    "cbr": page_cbr,
    "knowledge": page_knowledge,
    "cases": page_cases,
    "about": page_about,
}

current = st.session_state.get("page", "home")
pages.get(current, page_home)()
