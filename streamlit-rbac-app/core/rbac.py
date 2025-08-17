import streamlit as st
from .auth import get_current_user, user_has_permission, login_form
from .db import get_session

def require_permission(slug: str):
    def checker():
        db = get_session()  # keep session open for page
        user = get_current_user(db)
        if not user:
            st.info("Bu sayfa için giriş yapmalısınız.")
            login_form()
            st.stop()
        if not user_has_permission(user, slug, db):
            st.error(f"Bu alan için yetkiniz yok: {slug}")
            st.stop()
        return user, db
    return checker
