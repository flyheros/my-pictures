import streamlit as st
import pandas as pd

df = pd.DataFrame({
    "col1": ["a", "b", "c"],
    "col2": ["x", "y", "z"],
    "col3": [1, 2, 3]
})

params = st.experimental_get_query_params()
selected_col = params.get("col", [None])[0]
selected_val = params.get("val", [None])[0]

st.title("🔍 상세 보기 페이지")

if selected_col and selected_val:
    st.write(f"선택된 컬럼: `{selected_col}`")
    st.write(f"선택된 값: `{selected_val}`")

    # 값 타입 정제
    if df[selected_col].dtype != "object":
        try:
            selected_val = int(selected_val)
        except:
            pass

    filtered = df[df[selected_col] == selected_val]
    st.dataframe(filtered)
else:
    st.warning("파라미터(col, val)가 없습니다.")
