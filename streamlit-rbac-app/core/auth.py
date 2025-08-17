import streamlit as st
from sqlalchemy import select
from sqlalchemy.exc import OperationalError
from datetime import datetime

from .db import get_session
from .security import verify_password
from models.user import User

SESSION_USER_KEY = "current_user"

def login_form():
    st.subheader("Giriş Yap")
    username_or_email = st.text_input("Kullanıcı adı veya e-posta")
    password = st.text_input("Parola", type="password")
    if st.button("Giriş"):
        if not username_or_email or not password:
            st.error("Bilgileri doldurunuz.")
            return False
        from core.bootstrap import ensure_db_initialized
        with get_session() as db:
            try:
                q = db.execute(
                    select(User).where((User.email == username_or_email) | (User.username == username_or_email))
                ).scalar_one_or_none()
            except OperationalError:
                ensure_db_initialized()
                q = db.execute(
                    select(User).where((User.email == username_or_email) | (User.username == username_or_email))
                ).scalar_one_or_none()
            if not q or not q.status:
                st.error("Kullanıcı bulunamadı veya pasif.")
                return False
            if not verify_password(password, q.password_hash):
                st.error("Parola hatalı.")
                return False
            q.last_login_at = datetime.utcnow()
            db.commit()
            st.session_state[SESSION_USER_KEY] = {"id": q.id, "name": q.name, "email": q.email}
            st.success("Giriş başarılı.")
            st.rerun()
    return False


def get_current_user(db=None):
    data = st.session_state.get(SESSION_USER_KEY)
    if not data:
        return None
    if db is None:
        from .db import get_session
        with get_session() as dbs:
            return dbs.get(User, data["id"])
    else:
        return db.get(User, data["id"])


def logout():
    if SESSION_USER_KEY in st.session_state:
        del st.session_state[SESSION_USER_KEY]
    st.rerun()


def user_has_permission(user: User, slug: str, db) -> bool:
    """Kullanıcının rol/izin ilişkilerinden hedef izne sahip olup olmadığını kontrol eder."""
    if not user:
        return False
    u = db.get(User, user.id)
    if u is None:
        return False
    for r in u.roles:
        for p in r.permissions:
            if p.slug == slug:
                return True
    return False
