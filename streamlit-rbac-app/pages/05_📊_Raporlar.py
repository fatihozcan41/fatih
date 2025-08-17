import streamlit as st
from core.rbac import require_permission
from core.db import get_session
from services.report_service import summary_by_account
import plotly.express as px

checker = require_permission("reports.read")
user, db = checker()

st.title("📊 Raporlar")
df = summary_by_account(db)
if df.empty:
    st.warning("Rapor için veri bulunamadı.")
else:
    st.dataframe(df, use_container_width=True)
    fig = px.pie(df, names="Hesap", values="Toplam", title="Hesap Dağılımı")
    st.plotly_chart(fig, use_container_width=True)
