import streamlit as st
from sqlalchemy import select
from core.rbac import require_permission
from core.db import get_session
from models.domain_tables import Ratio

checker = require_permission("ratios.manage")
user, db = checker()

st.title("⚙️ Oran Yönetimi")

col1, col2 = st.columns(2)
with col1:
    name = st.text_input("Oran Adı")
with col2:
    value = st.number_input("Değer", value=0.0, step=0.01)

if st.button("Ekle/Güncelle"):
    # basit örnek: aynı ad varsa güncelle
    existing = db.execute(select(Ratio).where(Ratio.name==name)).scalar_one_or_none()
    if existing:
        existing.value = float(value)
    else:
        db.add(Ratio(name=name, value=float(value)))
    db.commit()
    st.success("Kaydedildi.")
    st.experimental_rerun()

st.subheader("Tanımlı Oranlar")
ratios = db.execute(select(Ratio)).scalars().all()
if ratios:
    for r in ratios:
        st.write(f"- **{r.name}** = {r.value}")
else:
    st.info("Henüz oran yok.")
