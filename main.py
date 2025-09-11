import streamlit as st
import pandas as pd
import altair as alt
import os

st.set_page_config(page_title="MBTI Distribution Dashboard", layout="wide")
st.title("🌍 MBTI 유형 분포 대시보드")

# 파일 경로 확인 (같은 폴더에 있는 경우 우선 사용)
file_path = "countriesMBTI_16types.csv"
if os.path.exists(file_path):
    df = pd.read_csv(file_path)
else:
    uploaded_file = st.file_uploader("📂 CSV 파일을 업로드하세요", type=["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
    else:
        st.warning("CSV 파일이 필요합니다.")
        st.stop()

# MBTI 열 목록
mbti_types = [
    "INTJ", "INTP", "ENTJ", "ENTP",
    "INFJ", "INFP", "ENFJ", "ENFP",
    "ISTJ", "ISFJ", "ESTJ", "ESFJ",
    "ISTP", "ISFP", "ESTP", "ESFP"
]

st.sidebar.header("📌 메뉴")
menu = st.sidebar.radio("🔍 보고 싶은 내용을 선택하세요", ["📊 데이터 탐색", "🌎 전세계 평균", "🏳️ 국가별 비교", "🏆 Top3 / Bottom3"])

if menu == "📊 데이터 탐색":
    st.subheader("🔎 데이터 미리보기")
    st.dataframe(df.head(20))
    st.subheader("📈 기본 통계")
    st.write(df[mbti_types].describe())

elif menu == "🌎 전세계 평균":
    st.subheader("🌐 전세계 MBTI 평균 분포")
    avg_distribution = df[mbti_types].mean().reset_index()
    avg_distribution.columns = ["MBTI", "평균"]

    chart = (
        alt.Chart(avg_distribution)
        .mark_bar(color="cornflowerblue")
        .encode(
            x=alt.X("MBTI", sort="-y"),
            y="평균"
        )
    )
    st.altair_chart(chart, use_container_width=True)

elif menu == "🏳️ 국가별 비교":
    st.subheader("🌏 국가별 MBTI 분포 비교")
    countries = st.multiselect("🌍 국가를 선택하세요", df["Country"].unique(), default=[df["Country"].iloc[0]])

    if countries:
        selected = df[df["Country"].isin(countries)].melt(id_vars="Country", value_vars=mbti_types,
                                                           var_name="MBTI", value_name="비율")
        chart = (
            alt.Chart(selected)
            .mark_line(point=True)
            .encode(
                x="MBTI",
                y="비율",
                color="Country"
            )
        )
        st.altair_chart(chart, use_container_width=True)

elif menu == "🏆 Top3 / Bottom3":
    st.subheader("🥇 MBTI 유형별 Top3 / Bottom3 국가")

    selected_mbti = st.selectbox("✨ MBTI 유형을 선택하세요", mbti_types)

    top3 = df.nlargest(3, selected_mbti)[["Country", selected_mbti]]
    bottom3 = df.nsmallest(3, selected_mbti)[["Country", selected_mbti]]

    st.write("### 🥇 Top 3 국가")
    chart_top = (
        alt.Chart(top3)
        .mark_bar(color="seagreen")
        .encode(
            x=alt.X("Country", sort="-y"),
            y=selected_mbti
        )
    )
    st.altair_chart(chart_top, use_container_width=True)

    st.write("### 🥉 Bottom 3 국가")
    chart_bottom = (
        alt.Chart(bottom3)
        .mark_bar(color="indianred")
        .encode(
            x=alt.X("Country", sort="y"),
            y=selected_mbti
        )
    )
    st.altair_chart(chart_bottom, use_container_width=True)
