import os
import pandas as pd
from PIL import Image
from datetime import datetime
import imagehash
import hashlib
from PIL.ExifTags import TAGS

# 설정
source_root = r"C:\사진_20240726_1231"
# source_root= r"D:\사진\원본\핸드폰사진_핸드폰에 그대로있음"
thumbnail_root = r"C:\썸네일"
# thumbnail_root = r"d:\썸네일"
csv_output = "file_result.csv"

# 처리할 이미지 확장자
image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.webp']
video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.wmv']

file_data = []


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

# 재귀적으로 파일 스캔
i=0
for root, _, files in os.walk(source_root):
    for file in files:

        # if i>10:
        #     break       
        i=i+1
        file_path = os.path.join(root, file)
        ext = os.path.splitext(file)[1].lower()

        if ext in image_extensions + video_extensions:
            stat = os.stat(file_path)
            rel_path = os.path.relpath(file_path, source_root)
            file_hash = get_file_hash(file_path)
 
            if ext in image_extensions :
                create_dt=get_taken_date(file_path)
                file_average_hash = imagehash.average_hash(Image.open(file_path)) # 유사도 검색
            else: 
                create_dt = ""
                file_average_hash = ""

            file_type = "사진" if ext in image_extensions else "동영상"

            file_data.append({
                "파일경로": file_path,
                "파일명": file,
                "파일수정일시": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
                "파일생성일시": datetime.fromtimestamp(stat.st_ctime).strftime("%Y-%m-%d %H:%M:%S"),
                "촬영일시": create_dt, 
                "파일유형": file_type,
                "파일크기(Byte)": stat.st_size,
                "파일해쉬": file_hash,
                "파일유사도해쉬": str(file_average_hash),
            })
            print(i)

            # 썸네일 생성
            if ext in image_extensions:
                thumb_path = os.path.join(thumbnail_root, rel_path)
                result_thumbnail = make_thumbnail(file_path, thumb_path)
            else: 
                result_thumbnail = ""

            file_data[-1]["썸네일생성결과"] = result_thumbnail
    
    if i>100:
        break
    

# CSV 저장
df = pd.DataFrame(file_data)


df['파일생성일'] = pd.to_datetime(df['파일생성일시'])
df['파일수정일'] = pd.to_datetime(df['파일수정일시'])
df['파일생성일'] = df['파일생성일'].dt.to_period('D')
df['파일수정일'] = df['파일수정일'].dt.to_period('D')
df['촬영일'] = pd.to_datetime(df['촬영일시'].str[:10].str.replace(":", "-")).dt.to_period('D')
 

df.to_csv(csv_output, index=False, encoding="utf-8-sig")

print(f"\n완료: {len(file_data)}개의 파일 처리됨. 결과 -> {csv_output}")
