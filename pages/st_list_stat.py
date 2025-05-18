import os 
from PIL import Image
from datetime import datetime
import hashlib
from PIL.ExifTags import TAGS
import streamlit as st
import pandas as pd
from st_utils import get_page_url

    
 
def go_to_picutre(selected_col, selected_val):
    """게시물 상세 페이지로 이동하는 함수"""
    st.session_state.selected_col = selected_col
    st.session_state.selected_val = selected_val
    st.session_state.page = 'st_list_picture'

def show_list_stat():
    
    st.set_page_config(
        page_title="사진 통계 리스트 ",
        page_icon="🔍",
        layout="wide"
    )

    csv_path = r"C:\workspace\my-pictures\file_result.csv"
    df = pd.read_csv(csv_path) 
    
    def get_file_stat(df, key_col):

        df_tmp = df.groupby([key_col]).agg(
        file_count=("파일명", "count"),
        file_name_min=("파일명", "min"),
        file_name_max=("파일명", "max"),
        file_hash_min=("파일해쉬", "min"),
        file_hash_max=("파일해쉬", "max"),
        create_dt_min=("파일생성일", "min"),
        create_dt_max=("파일생성일", "max"),
        picture_dt_min=("촬영일", "min"),
        picture_dt_max=("촬영일", "max")).reset_index().sort_values(by=['file_count'], ascending=False)
        
        return df_tmp

        # file_path=csv_path.replace("result.csv", f"result_{key_col}.csv")
        # df_tmp.to_csv( f"{file_path}", index=False, encoding="utf-8-sig") 
        # print(f"완료: {len(df_tmp)}개의 파일 처리됨. 결과 -> {file_path}")




    sort_column = ['파일명', '파일해쉬', '촬영일', '파일생성일']
    key_col = st.selectbox("정렬할 컬럼 선택", sort_column, index=0)
    df = get_file_stat(df, key_col)


    # 가로로 2열 생성
    col1, col2 = st.columns([1, 1])  # 비율을 바꿔도 됨

    # 정렬 옵션
    with col1:
        col1_1, col1_2 = st.columns([1,1])
        with col1_1:
            sort_column = st.selectbox("정렬할 컬럼 선택", df.columns)
        with col1_2:
            sort_ascending = st.radio("정렬 순서", ["오름차순", "내림차순"]) == "오름차순"
        df_sorted = df.sort_values(by=sort_column, ascending=sort_ascending)

    # 페이징 처리
    with col2:
        items_per_page = 10
        total_pages = (len(df_sorted) - 1) // items_per_page + 1 
        page = st.number_input("페이지 번호", min_value=1, max_value=total_pages, value=1, step=1)
    
    # 게시물 목록 표시
    start_idx = (page - 1) * items_per_page
    end_idx = start_idx + items_per_page
    st.write(f"**(총 {len(df)}건)   페이지 {page} / {total_pages}**")

    if st.button("상세보기"):
        go_to_picutre('촬영일', '2024-07-26')

    # 각 셀에 링크 추가하는 함수
    def add_links_to_dataframe(df):
        # 데이터프레임 복사
        df_with_links = df.copy()
        
        # 각 열에 대해 처리
        for col in df.columns:
            # 각 셀에 링크 추가
            df_with_links[col] = df_with_links.apply(
                lambda row:  f'<a href="st_list_picture?col={col}&val={row[col]}" target="_self">{row[col]}</a>' if col in sort_column else row[col],
                axis=1)
        
        return df_with_links
    
    df_display = df_sorted.iloc[start_idx:end_idx].reset_index(drop=True)
    if df_display.empty:
        st.warning("선택한 페이지에 데이터가 없습니다.")
        return
    
    # 링크가 추가된 데이터프레임 생성
    df_with_links = add_links_to_dataframe(df_display)

    # 상단 설명
    st.subheader("통계 데이터")
    st.info("각 셀을 클릭하면 해당 열(col_name)과 값(value)으로 필터링된 결과를 확인할 수 있습니다.")

    # HTML로 렌더링
    st.markdown(df_with_links.to_html(escape=False), unsafe_allow_html=True)

    # 원본 데이터프레임도 표시 (참고용)
    st.subheader("원본 데이터 (링크 없음)")
    st.dataframe(df_display)
show_list_stat()