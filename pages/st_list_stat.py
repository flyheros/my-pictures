import os 
from PIL import Image
from datetime import datetime
import hashlib
from PIL.ExifTags import TAGS
import streamlit as st
import pandas as pd
from st_utils import get_page_url
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

# 설정
 
thumbnail_folder = os.getenv('thumbnail_folder', r"C:\workspace\my-pictures\thumbnail")
result_output = os.getenv('result_output', r"C:\workspace\my-pictures\result.csv") 
del_file_folder  = os.getenv('thumbnail_folder', r"C:\workspace\my-pictures\thumbnail")  
csv_path = os.path.join("." , result_output)

    
 
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
    df = pd.read_csv(csv_path) 
    df['촬영일시'] = df['촬영일'] 
    df['촬영일'] = df['촬영일시'].apply(lambda x:x[:10] if isinstance(x, str) else x)  # '촬영일' 컬럼에서 날짜 부분만 추출
    df['파일생성일시'] = df['파일생성일'] 
    df['파일생성일'] = pd.to_datetime(df['파일생성일시'], errors='coerce').dt.date  # '파일생성일' 컬럼을 datetime으로 변환
    df['folder_path'] = df['파일경로'].apply(lambda x: os.path.dirname(x))
    
    def get_file_stat(df, key_col):

        df_tmp = df.groupby([key_col]).agg(
        file_count=("파일명", "count"),
        file_name_min=("파일명", "min"),
        file_name_max=("파일명", "max"),
        file_hash_min=("파일해쉬", "min"),
        file_hash_max=("파일해쉬", "max"),
        create_dt_min=("파일생성일", "min"),
        create_dt_max=("파일생성일", "max"),
        create_dttm_min=("파일생성일시", "min"),
        create_dttm_max=("파일생성일시", "max"),
        file_path_min=("파일경로", "min"),
        file_path_max=("파일경로", "max"),
        file_folder=("folder_path", "unique"),
        picture_dt_min=("촬영일", "min"),
        picture_dt_max=("촬영일", "max"),
        picture_dttm_min=("촬영일시", "min"),
        picture_dttm_max=("촬영일시", "max")).reset_index().sort_values(by=['file_count'], ascending=False)

        if key_col=="파일명":
            keywords = ["file_name", 'picture_dt_', 'create_dt_']
            # df_tmp=df_tmp.drop(columns=[col for col in df_tmp.columns if "file_name" in col ], axis=1)  # 불필요한 컬럼 제거
            df_tmp = df_tmp.loc[:, ~df_tmp.columns.str.contains('file_name')]  # 'file_name'이 포함된 컬럼 제거
        elif key_col=="파일해쉬":
            keywords = ["file_hash", 'picture_dt_', 'create_dt_']
            # df_tmp=df_tmp.drop(columns=[col for col in df_tmp.columns if "file_hash" in col ], axis=1)  # 불필요한 컬럼 제거
            df_tmp = df_tmp.loc[:, ~df_tmp.columns.str.contains('file_hash')]  # 'file_name'이 포함된 컬럼 제거
        elif key_col=="파일생성일":
            keywords = ["create_dt", 'picture_dt_', 'create_dt_']
            # df_tmp=df_tmp.drop(columns=[col for col in df_tmp.columns if "create_dt" in col ], axis=1)  # 불필요한 컬럼 제거
            df_tmp = df_tmp.loc[:, ~df_tmp.columns.str.contains('create_dt')]  # 'file_name'이 포함된 컬럼 제거
        elif key_col=="파일경로":
            keywords = ["file_path", 'picture_dt_', 'create_dt_']
            # df_tmp=df_tmp.drop(columns=[col for col in df_tmp.columns if "file_path" in col ], axis=1)  # 불필요한 컬럼 제거
            df_tmp = df_tmp.loc[:, ~df_tmp.columns.str.contains('file_path')]  # 'file_name'이 포함된 컬럼 제거
        elif key_col=="촬영일":
            keywords = ["picture_dt", 'picture_dt_', 'create_dt_']
            # df_tmp=df_tmp.drop(columns=[col for col in df_tmp.columns if "picture_dt" in col ], axis=1)  # 불필요한 컬럼 제거
            df_tmp = df_tmp.loc[:, ~df_tmp.columns.str.contains('picture_dt')]  # 'file_name'이 포함된 컬럼 제거
            
            
        df_tmp = df_tmp.drop(columns=[col for col in df_tmp.columns if any(keyword in col for keyword in keywords)])
        print(df_tmp.columns)
        return df_tmp

        # file_path=csv_path.replace("result.csv", f"result_{key_col}.csv")
        # df_tmp.to_csv( f"{file_path}", index=False, encoding="utf-8-sig") 
        # print(f"완료: {len(df_tmp)}개의 파일 처리됨. 결과 -> {file_path}")

    # 해당 폴더의 중복파일은 하나만 남기고 삭제 폴더로 이동 
    def del_file_dup(file_path, del_hash): 
        # file_path = os.path.join(file_path, "20240726_185220 - 복사본.jpg") 
        print("삭제파일", file_path)
        # shutil.move(file_path, del_file_folder)
         
        hasher = hashlib.md5()  # SHA256 도 가능
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                hasher.update(chunk)

        if hasher.hexdigest() == del_hash:
            print("삭제파일", file_path)
            # 파일 삭제 폴더로 이동
            del_file_path = os.path.join(del_file_folder, os.path.basename(file_path))
            os.makedirs(os.path.dirname(del_file_path), exist_ok=True)  
            try:
                os.rename(file_path, del_file_path)
                print(f"삭제 완료: {file_path} -> {del_file_path}")
            except Exception as e:
                print(f"삭제 실패: {file_path} -> {e}") 


    dup_column = ['파일명', '파일해쉬', '촬영일', '파일생성일']
    key_col = st.selectbox("집계 컬럼 선택", dup_column, index=1)
    df_stat = get_file_stat(df, key_col)

    st.button("중복파일 삭제", on_click=del_file_dup, args=("C:\\사진_20240726_1231\\20241231_100853 - 복사본.jpg", "4e90ddece508a16aa7841617ab02613b"))

    # 가로로 2열 생성
    col1, col2 = st.columns([1, 1])  # 비율을 바꿔도 됨

    # 정렬 옵션
    with col1:
        col1_1, col1_2 = st.columns([1,1])
        with col1_1:
            sort_column = st.selectbox("정렬할 컬럼 선택", df_stat.columns, index=1)
        with col1_2:
            sort_ascending = st.radio("정렬 순서", ["오름차순", "내림차순"], 1) == "오름차순"
        df_sorted = df_stat.sort_values(by=sort_column, ascending=sort_ascending)

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
    st.session_state.selected_image_path = "C:\\사진_20240726_1231\\20240726_185220 - 복사본.jpg"
show_list_stat()


# 이미지 팝업 (같은 페이지 내 하단에 표시)
if st.session_state.selected_image_path:
    st.markdown("---")
    st.subheader("🖼 선택된 이미지 보기")
    try:
        # 이미지 로드
        img = Image.open(Path(st.session_state.selected_image_path))
        st.image(img, caption=Path(st.session_state.selected_image_path).name, use_column_width=True)
    except Exception as e:
        st.error(f"이미지를 불러올 수 없습니다: {e}")