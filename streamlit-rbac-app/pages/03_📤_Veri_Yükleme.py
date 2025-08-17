import streamlit as st
import pandas as pd
from sqlalchemy import select
from core.rbac import require_permission
from core.db import get_session
from services.upload_service import import_dataframe
from models.domain_tables import Record

checker = require_permission("data.upload")
user, db = checker()

st.title("📤 Veri Yükleme")

uploaded = st.file_uploader("CSV veya Excel dosyası yükleyin", type=["csv","xlsx"])
if st.button("Örnek Dosya Göster"):
    st.write("`sample_data/demo.xlsx` dosyasını kullanabilirsiniz.")

if uploaded:
    if uploaded.name.endswith(".csv"):
        df = pd.read_csv(uploaded)
    else:
        df = pd.read_excel(uploaded)
    st.write("Önizleme:", df.head())
    if st.button("İçe Aktar"):
        import_dataframe(df, db)
        st.success("Kayıtlar eklendi.")

st.subheader("Kayıtlar")
rows = db.execute(select(Record)).scalars().all()
st.write(f"Toplam {len(rows)} kayıt.")
if rows:
    st.dataframe(pd.DataFrame([{"Tarih": r.date, "Hesap": r.account, "Açıklama": r.description, "Tutar": r.amount} for r in rows]), use_container_width=True)
