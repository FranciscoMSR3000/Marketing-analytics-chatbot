import streamlit as st
import pandas as pd
from src.chain import ask

st.set_page_config(
    page_title="Marketing Analytics Chatbot",
    page_icon="📊",
    layout="wide"
)

st.markdown("""
    <style>
    .main { background-color: #0f1117; }
    .metric-card {
        background: #1e2130;
        border-radius: 12px;
        padding: 20px;
        border: 1px solid #2d3250;
    }
    .title-text {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(90deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .stChatMessage { background: #1e2130 !important; border-radius: 12px; }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<p class="title-text">Marketing Analytics Chatbot</p>', unsafe_allow_html=True)
st.caption("Powered by RAG · ChromaDB · GPT-4o-mini")

# Cargar datos
@st.cache_data
def load_data():
    return pd.read_csv("data/campaigns.csv")

df = load_data()

# Métricas globales
st.markdown("### Resumen general")
m1, m2, m3, m4, m5 = st.columns(5)

with m1:
    st.metric("Campañas", f"{len(df):,}")
with m2:
    st.metric("Canales", f"{df['channel'].nunique()}")
with m3:
    st.metric("Inversión total", f"${df['spend'].sum():,.0f}")
with m4:
    st.metric("Revenue total", f"${df['revenue'].sum():,.0f}")
with m5:
    st.metric("ROAS promedio", f"{df['roas'].mean():.2f}x")

st.divider()

# Descripción de datos disponibles
with st.expander("📂 ¿Qué información está disponible?", expanded=False):
    col_a, col_b, col_c = st.columns(3)

    with col_a:
        st.markdown("**Períodos**")
        for q in sorted(df['quarter'].unique()):
            st.markdown(f"- {q}")

        st.markdown("**Regiones**")
        for r in sorted(df['region'].unique()):
            st.markdown(f"- {r}")

    with col_b:
        st.markdown("**Canales**")
        for c in sorted(df['channel'].unique()):
            st.markdown(f"- {c}")

    with col_c:
        st.markdown("**Métricas disponibles**")
        metricas = [
            "CTR (Click-through rate)",
            "CPC (Costo por clic)",
            "ROAS (Retorno sobre inversión)",
            "Conversiones y tasa de conversión",
            "Costo por conversión",
            "Engagement rate",
            "Likes, shares y comentarios",
            "Video views",
            "Bounce rate",
            "Inversión y revenue",
        ]
        for m in metricas:
            st.markdown(f"- {m}")

    st.markdown("**Tipos de campaña**")
    tipos = sorted(df['campaign_type'].unique())
    st.markdown(" · ".join([f"`{t}`" for t in tipos]))

st.divider()

# Chat
st.markdown("### Chat")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

question = st.chat_input("Escribe tu pregunta aquí...")

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.write(question)

    with st.chat_message("assistant"):
        with st.spinner("Analizando datos..."):
            answer = ask(question)
        st.write(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})