# st_utils.py
import streamlit as st
from urllib.parse import urlencode

def get_page_url(page_name, **params):
    """
    주어진 페이지 이름과 파라미터로 URL을 생성합니다.
    
    Args:
        page_name (str): 페이지 이름 (예: "st_main")
        **params: 쿼리 파라미터로 전달할 키-값 쌍
    
    Returns:
        str: 생성된 URL
    """
    # 기본 URL 구조
    base_url = f"/?page={page_name}"
    
    # 파라미터가 있으면 추가
    if params:
        query_string = urlencode(params)
        return f"{base_url}&{query_string}"
    
    return base_url


def go_picture(**params):
    print(params)
    """게시물 상세 페이지로 이동하는 함수"""
    st.session_state.page = "st_list_picture"
    st.session_state.selected_col = params['selected_col']
    st.session_state.selected_val = params['selected_val']
 