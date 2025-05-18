import streamlit as st
import pandas as pd

df = pd.DataFrame({
    "col1": ["a", "b", "c"],
    "col2": ["x", "y", "z"],
    "col3": [1, 2, 3]
})

st.set_page_config(
    page_title="상세보기 페이지",
    page_icon="🔍",
    layout="wide"
)
st.title("📄 전체 데이터 목록")

df_with_links = df.copy()

# 링크는 반드시 `/b`가 아닌 "b"라는 페이지 이름을 사용해야 함
for col in df.columns:
    df_with_links[col] = df.apply(
        lambda row: f'<a href="/b?col={col}&val={row[col]}" target="_self">{row[col]}</a>',
        axis=1
    )
# HTML 출력
st.write(df_with_links.to_html(escape=False), unsafe_allow_html=True)
