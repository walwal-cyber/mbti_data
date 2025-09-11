import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="MBTI 외향/내향 분석", layout="wide")
st.title("😎 MBTI 외향(E) vs 내향(I) 분석")

# 파일 경로 확인 (같은 폴더 우선)
file_path = "countriesMBTI_16types.csv"
if os.path.exists(file_path):
    df = pd.read_csv(file_path)
else:
    uploaded_file = st.file_uploader("📂 CSV 파일 업로드", type=["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
    else:
        st.warning("CSV 파일이 필요합니다.")
        st.stop()

# MBTI 유형 분류
mbti_types = [
    "INTJ","INTP","ENTJ","ENTP",
    "INFJ","INFP","ENFJ","ENFP",
    "ISTJ","ISFJ","ESTJ","ESFJ",
    "ISTP","ISFP","ESTP","ESFP"
]

e_types = [t for t in mbti_types if t.startswith("E")]
i_types = [t for t in mbti_types if t.startswith("I")]

# 외향 / 내향 비율 계산
df["Extraversion"] = df[e_types].sum(axis=1)
df["Introversion"] = df[i_types].sum(axis=1)
df["Total"] = df["Extraversion"] + df["Introversion"]
df["Extraversion_ratio"] = df["Extraversion"] / df["Total"] * 100
df["Introversion_ratio"] = df["Introversion"] / df["Total"] * 100

# 📊 국가별 외향/내향 비율 비교
st.subheader("🌍 국가별 외향 vs 내향 비율")
country = st.selectbox("국가 선택", df["Country"].unique())

selected = df[df["Country"] == country][["Extraversion_ratio", "Introversion_ratio"]].melt(
    var_name="유형", value_name="비율"
)

fig = px.bar(
    selected,
    x="유형", y="비율", color="유형", text="비율",
    title=f"{country}의 외향(E) vs 내향(I) 비율",
    color_discrete_map={
        "Extraversion_ratio": "dodgerblue",
        "Introversion_ratio": "mediumpurple"
    }
)
fig.update_traces(texttemplate='%{text:.2f}%', textposition="outside")
st.plotly_chart(fig, use_container_width=True)

# 🏆 외향형 / 내향형 상위 국가 랭킹
st.subheader("🏆 외향형 / 내향형 국가 랭킹")

col1, col2 = st.columns(2)

with col1:
    top_e = df.nlargest(10, "Extraversion_ratio")[["Country", "Extraversion_ratio"]]
    fig_e = px.bar(top_e, x="Country", y="Extraversion_ratio", text="Extraversion_ratio",
                   title="🌟 외향(E) TOP 10 국가", color="Country")
    fig_e.update_traces(texttemplate='%{text:.2f}%', textposition="outside")
    st.plotly_chart(fig_e, use_container_width=True)

with col2:
    top_i = df.nlargest(10, "Introversion_ratio")[["Country", "Introversion_ratio"]]
    fig_i = px.bar(top_i, x="Country", y="Introversion_ratio", text="Introversion_ratio",
                   title="🌙 내향(I) TOP 10 국가", color="Country")
    fig_i.update_traces(texttemplate='%{text:.2f}%', textposition="outside")
    st.plotly_chart(fig_i, use_container_width=True)
