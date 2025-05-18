import streamlit as st
import pandas as pd
from st_list_stat import show_list_stat
from st_list_picture import show_list_picture

def main():
    # 페이지 제목 설정
    st.set_page_config(
        page_title="통계 및 상세 정보 앱",
        page_icon="📊",
        layout="wide"
    )
    
    # 세션 상태 초기화
    if 'page' not in st.session_state:
        st.session_state.page = 'st_list_stat'  # 기본 페이지는 목록
    
    if 'selected_col' not in st.session_state:
        st.session_state.selected_col = None  # 선택된 컬럼럼
        
    if 'selected_val' not in st.session_state:
        st.session_state.selected_val = None

        
    try:
        # Streamlit 1.16.0 이상 버전
        params = st.query_params()
        print('--------------------------')
        print(params['page'][0])
        st.session_state.page = params['page'][0]
        st.warning(f"페이지: {st.session_state.page}")
        print('--------------------------')
    except:
        params = ""

    st.warning(f"페이지: {st.session_state.page}")
    st.warning(f"====: {params}")


    # 현재 페이지에 따라 해당 페이지 표시
    if st.session_state.page == 'st_list_stat':
        show_list_stat()
    elif st.session_state.page == 'st_list_picture':
        show_list_picture()

if __name__ == "__main__":
    main()

