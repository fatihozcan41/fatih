import streamlit as st
from core.rbac import require_permission
from core.db import get_session
from services.report_service import summary_by_account
import plotly.express as px

checker = require_permission("reports.read")
user, db = checker()

st.title("🧭 Kontrol Paneli")
df = summary_by_account(db)
if df.empty:
    st.warning("Özet veri bulunamadı. 'Veri Yükleme' sayfasından örnek veri yükleyin.")
else:
    st.dataframe(df)
    fig = px.bar(df, x="Hesap", y="Toplam", title="Hesap Bazında Toplamlar")
    st.plotly_chart(fig, use_container_width=True)
