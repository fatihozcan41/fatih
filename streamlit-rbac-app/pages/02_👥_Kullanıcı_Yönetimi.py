import streamlit as st
from sqlalchemy import select
from core.rbac import require_permission
from core.db import get_session
from core.security import hash_password
from models.user import User
from models.role import Role

checker = require_permission("users.read")
user, db = checker()

st.title("👥 Kullanıcı Yönetimi")

tab1, tab2 = st.tabs(["Liste", "Yeni/Düzenle"])

with tab1:
    users = db.execute(select(User)).scalars().all()
    data = [{"ID": u.id, "Ad": u.name, "E-posta": u.email, "Kullanıcı Adı": u.username, "Durum": "Aktif" if u.status else "Pasif"} for u in users]
    st.dataframe(data, use_container_width=True)

with tab2:
    mode = st.radio("İşlem", ["Yeni", "Düzenle", "Sil"], horizontal=True)

    if mode == "Yeni":
        st.subheader("Yeni Kullanıcı")
        name = st.text_input("Ad Soyad")
        email = st.text_input("E-posta")
        username = st.text_input("Kullanıcı Adı (opsiyonel)")
        password = st.text_input("Parola", type="password")
        roles = db.execute(select(Role)).scalars().all()
        selected_roles = st.multiselect("Roller", [r.slug for r in roles])
        if st.button("Kaydet"):
            if not (name and email and password):
                st.error("Zorunlu alanları doldurunuz.")
            else:
                u = User(name=name, email=email, username=username, password_hash=hash_password(password), status=True)
                db.add(u); db.commit(); db.refresh(u)
                # assign roles
                for slug in selected_roles:
                    r = db.execute(select(Role).where(Role.slug==slug)).scalar_one()
                    u.roles.append(r)
                db.commit()
                st.success("Kullanıcı oluşturuldu.")
                st.experimental_rerun()

    elif mode == "Düzenle":
        user_id = st.number_input("Kullanıcı ID", min_value=1, step=1)
        target = db.get(User, int(user_id)) if user_id else None
        if target:
            name = st.text_input("Ad Soyad", target.name)
            email = st.text_input("E-posta", target.email)
            username = st.text_input("Kullanıcı Adı", target.username or "")
            status = st.checkbox("Aktif", value=bool(target.status))
            new_pass = st.text_input("Yeni Parola (opsiyonel)", type="password")
            roles = db.execute(select(Role)).scalars().all()
            current_role_slugs = [r.slug for r in target.roles]
            selected_roles = st.multiselect("Roller", [r.slug for r in roles], default=current_role_slugs)
            if st.button("Güncelle"):
                target.name, target.email, target.username, target.status = name, email, username, status
                if new_pass:
                    target.password_hash = hash_password(new_pass)
                target.roles = [db.execute(select(Role).where(Role.slug==slug)).scalar_one() for slug in selected_roles]
                db.commit()
                st.success("Kullanıcı güncellendi.")
                st.experimental_rerun()
        else:
            st.info("Geçerli bir ID giriniz.")

    elif mode == "Sil":
        user_id = st.number_input("Silinecek Kullanıcı ID", min_value=1, step=1, key="del_id")
        if st.button("Sil", type="primary"):
            target = db.get(User, int(user_id))
            if target:
                db.delete(target); db.commit()
                st.success("Kullanıcı silindi.")
                st.experimental_rerun()
            else:
                st.error("Kullanıcı bulunamadı.")
