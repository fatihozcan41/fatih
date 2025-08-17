import streamlit as st
from core.auth import login_form, get_current_user, logout
from core.db import get_session
import pathlib

st.set_page_config(page_title="Kontrol Paneli", layout="wide")

# Inject minimal bootstrap-like css
with open("static/bootstrap.min.css", "r", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
with open("static/app.css", "r", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def navbar():
    user = get_current_user()
    st.markdown('<div class="navbar"><div><strong>RBAC Demo</strong></div><div>{}</div></div>'.format(
        (user.name if user else "")
    ), unsafe_allow_html=True)

navbar()

user = get_current_user()
if not user:
    login_form()
else:
    col1, col2 = st.columns([1,5])
    with col1:
        if st.button("Çıkış Yap"):
            logout()
    with col2:
        st.write("Hoş geldiniz,", f"**{user.name}**")

    st.info("Sol menüden sayfalar arasında gezinebilirsiniz.")

st.caption("© 2025 Streamlit RBAC Uygulaması")
