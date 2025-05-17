import streamlit as st
import pandas as pd
import os
from PIL import Image
import base64
from io import BytesIO

# 설정
source_root = r"D:\사진\원본\핸드폰사진_핸드폰에 그대로있음"
thumbnail_root = r"d:\썸네일"
csv_path = r"D:\workspace\my-pictures\file_result.csv"

# 제목
st.title("사진 데이터 미리보기")

# CSV 파일 읽기
df = pd.read_csv(csv_path)

# 동영상 제거
df = df[~df['파일유형'].str.lower().str.contains("동영상")]
df = df.drop(['썸네일생성결과', '파일유형'], axis=1)

# 썸네일 경로 생성
df['썸네일경로'] = df['파일경로'].apply(lambda x: os.path.join(thumbnail_root, x))

df['번호'] = range(1, len(df) + 1)




# 이미지 파일 여부 확인
def is_image_file(filepath):
    ext = os.path.splitext(filepath)[-1].lower()
    return ext in [".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tiff"]

# 이미지 → base64
def image_to_base64(filepath, max_size=(100, 100)):
    try:
        img = Image.open(filepath)
        img.thumbnail(max_size)
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        encoded = base64.b64encode(buffer.getvalue()).decode()
        return f'<img src="data:image/png;base64,{encoded}" width="100"/>'
    except:
        return "불러오기 실패"

# 미리보기 이미지 컬럼 추가
df['미리보기'] = df['썸네일경로'].apply(
    lambda x: image_to_base64(x) if os.path.exists(x) else '파일 없음'
)
df = df.drop('썸네일경로', axis=1)

# 컬럼 순서 지정
columns_to_show =  ['번호']  + [col for col in df.columns if col != '번호']  
 
# 가로로 2열 생성
col1, col2 = st.columns([1, 1])  # 비율을 바꿔도 됨

# 왼쪽: 페이징 개수 선택
with col1:
    items_per_page = st.number_input("페이징 개수", min_value=1, max_value=200, value=50, step=1)

# 전체 페이지 수 계산
total_pages = (len(df) - 1) // items_per_page + 1

# 오른쪽: 페이지 선택
with col2:
    page = st.number_input("페이지 선택", min_value=1, max_value=total_pages, value=1, step=1)

start_idx = (page - 1) * items_per_page
end_idx = start_idx + items_per_page
df_page = df.iloc[start_idx:end_idx]

# 기본 to_html로 생성
html_table = df_page[columns_to_show].to_html(escape=False, index=False)

# ✅ <table> 태그에 width: 90% 스타일 직접 삽입
html_table = html_table.replace('<table border="1" class="dataframe">', '<table border="1" class="dataframe" style="width:100%">')


# CSS 포함 (800px 고정 너비 또는 90% 너비 설정)
st.markdown("""
    <style>
        .centered-table {
            display: flex;
            justify-content: center;
            width: 600px;
        }
        table {
            width: 800px; /* 고정 너비 800px로 설정 */
            border-collapse: collapse;
        }
        th, td {
            padding: 6px;
            text-align: left;
            vertical-align: top;
        }
    </style>
""", unsafe_allow_html=True)



st.markdown(f'<div class="centered-table">{html_table}</div>', unsafe_allow_html=True)