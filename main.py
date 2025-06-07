import os
import pandas as pd
from PIL import Image
from datetime import datetime
import imagehash
import hashlib
from PIL.ExifTags import TAGS
import streamlit as st 
from dotenv import load_dotenv
import socket


computer_name = socket.gethostname()

load_dotenv()

# 처리할 이미지 확장자
image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.webp']
video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.wmv']

if computer_name == "DESKTOP-HU8FOFR":
    source_folder = os.getenv('source_folder')  # 기본값 포함
else:
    source_folder = os.getenv('source_folder2')  # 기본값 포함
    
thumbnail_folder = os.getenv('thumbnail_folder')  # 기본값 포함
result_output = os.getenv('result_output')  # 기본값 포함

def get_file_hash(file_path):
    hasher = hashlib.md5()  # SHA256 도 가능
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            hasher.update(chunk)
    return hasher.hexdigest()

def get_taken_date(img_path):
    image = Image.open(img_path)
    exif_data = image._getexif()

    if not exif_data:
        return "촬영 날짜 없음"

    for tag_id, value in exif_data.items():
        tag = TAGS.get(tag_id, tag_id)
        if tag == 'DateTimeOriginal':  # 촬영 날짜
            return value


def make_thumbnail(source_path, thumbnail_path):
    try:
        with Image.open(source_path) as img:
            width, height = img.size
            new_size = (int(width * 0.1), int(height * 0.1))
            img = img.resize(new_size)
            os.makedirs(os.path.dirname(thumbnail_path), exist_ok=True)
            img.save(thumbnail_path)
            return 'Success'
    except Exception as e:
        print(f"썸네일 생성 실패: {source_path} -> {e}")
        return f"Fail: {source_path} -> {e}"


def make_report_file(source_root, thumbnail_root, csv_output, limit_n):
    file_data = []

    # 재귀적으로 파일 스캔
    i=0
    for root, _, files in os.walk(source_root):
        for file in files:
            i=i+1
            if i>limit_n and limit_n > 0:  # limit_n이 0보다 크면 제한된 개수만 처리
                break
            file_path = os.path.join(root, file)
            ext = os.path.splitext(file)[1].lower()
            print(i)

            if ext in image_extensions + video_extensions:
                stat = os.stat(file_path)
                rel_path = os.path.relpath(file_path, source_root)
                file_hash = get_file_hash(file_path)
                if ext in image_extensions:
                # 이미지 파일의 경우 해시와 유사도 해시 생성
                    file_average_hash = imagehash.average_hash(Image.open(file_path)) # 유사도 검색
                    picture_dttm =get_taken_date(file_path)
                else:
                    file_average_hash = pd.NaT  # 동영상의 경우 촬영일 정보 없음
                    picture_dttm = pd.NaT  # 동영상의 경우 촬영일 정보 없음
                file_type = "사진" if ext in image_extensions else "동영상"

                file_data.append({
                    "파일경로": rel_path,
                    "파일명": file,
                    "파일수정일": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
                    "파일생성일": datetime.fromtimestamp(stat.st_ctime).strftime("%Y-%m-%d %H:%M:%S"),
                    "촬영일": picture_dttm,
                    "파일유형": file_type,
                    "파일크기(Byte)": stat.st_size,
                    "파일해쉬": file_hash,
                    "파일유사도해쉬": str(file_average_hash),
                })

                # 썸네일 생성
                if ext in image_extensions:
                    thumb_path = os.path.join(thumbnail_root, rel_path)
                    result_thumbnail = make_thumbnail(file_path, thumb_path)
                else: 
                    result_thumbnail = "Not Applicable"

                file_data[-1]["썸네일생성결과"] = result_thumbnail
        
    # CSV 저장
    df = pd.DataFrame(file_data)
    df['촬영일']=df['촬영일'].apply(lambda x: x.replace(":", "-") if isinstance(x, str) else x)  # ':' 문자를 '-'로 변경
    df.to_csv(csv_output, index=False, encoding="utf-8-sig")
    print(f"\n완료: {len(file_data)}개의 파일 처리됨{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}. 결과 -> {csv_output}")
    return "success"

# 설정
st.set_page_config(
    page_title="사진 통계 및 썸네일 생성 앱",
    page_icon="📷",
    layout="wide"
)

# 세션 상태 초기화
if 'processing' not in st.session_state:
    st.session_state.processing = False
    
if 'result_message' not in st.session_state:
    st.session_state.result_message = None

print("컴퓨터 이름:", computer_name)

st.sidebar.header( f"컴퓨터명: {computer_name}")
st.sidebar.text("이미지 및 동영상 파일의 통계와 썸네일을 생성합니다.")

with st.sidebar:
    source_folder = st.text_input("source_folder", source_folder)
    thumbnail_folder = st.text_input("thumbnail_folder", thumbnail_folder)
    result_output = st.text_input("result_output", result_output)
    limit_n = st.number_input("처리할 파일 개수", min_value=0, max_value=100, value=10, step=1)
    if st.button("실행", disabled=st.session_state.processing, on_click=lambda: st.session_state.update(processing=True)):
        st.session_state.processing = True

        with st.spinner("파일 처리 중..."):
            result=make_report_file(source_folder, thumbnail_folder, result_output, limit_n)

        if result == "success":
            st.session_state.processing = False
            st.session_state.result_message = f'''📁 파일 {limit_n} 처리 완료! 
            ({datetime.now().strftime("%Y-%m-%d %H:%M:%S")})'''
        else: 
            st.session_state.processing = False
            st.session_state.result_message = f'''📁 파일 {limit_n} 처리 실패!
            {result} ({datetime.now().strftime("%Y-%m-%d %H:%M:%S")})'''
            st.error(st.session_state.result_message)   
        st.rerun()

    if 'result_message' in st.session_state and st.session_state.result_message:
        if "실패" in st.session_state.result_message:
            st.error(st.session_state.result_message)
        else:
            st.success(st.session_state.result_message)   