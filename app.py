import pandas as pd
import plotly.express as px
import streamlit as st
from core import demo_data,validate

st.set_page_config(page_title="Data Quality Pipeline",page_icon="✅",layout="wide")
st.title("✅ Automated Data Quality Pipeline")
upload=st.file_uploader("Upload order CSV",type="csv")
data=pd.read_csv(upload) if upload else demo_data()
report,score=validate(data)
a,b,c=st.columns(3)
a.metric("Quality score",f"{score:.1f}%")
b.metric("Rows checked",len(data))
c.metric("Issues found",len(report))
st.progress(score/100)
if not report.empty:
    counts=report.groupby("rule").size().reset_index(name="issues")
    st.plotly_chart(px.bar(counts,x="rule",y="issues",title="Issues by rule"),use_container_width=True)
st.subheader("Exception report")
st.dataframe(report,use_container_width=True)
st.download_button("Download exceptions",report.to_csv(index=False),"data_quality_exceptions.csv")
with st.expander("Input preview"):
    st.dataframe(data,use_container_width=True)
