import os 
from PIL import Image
from datetime import datetime
import hashlib
from PIL.ExifTags import TAGS
import streamlit as st
import pandas as pd

# 설정 

csv_path = r"D:\workspace\my-pictures\file_result.csv"
csv_path = r"C:\workspace\my-pictures\file_result.csv"


df = pd.read_csv(csv_path)

df['파일생성일'] = pd.to_datetime(df['파일생성일시'])
df['파일수정일'] = pd.to_datetime(df['파일수정일시시'])
df['create_dt'] = df['파일생성일시'].dt.to_period('D')
df['update_dt'] = df['파일수정일시시'].dt.to_period('D')
df['picture_dt'] = pd.to_datetime(df['촬영일시'].str[:10].str.replace(":", "-")).dt.to_period('D')
df['file_name'] = df['파일명']
df['file_hash'] = df['파일해쉬'] 
# df['촬영일'] = pd.to_datetime(df['촬영일'])
 

 
def save_file_hash(df, key_col):
    df_tmp = pd.DataFrame()

    df_tmp = df.groupby([key_col]).agg(
    file_count=("create_dt", "count"),
    file_name_min=("file_name", "min"),
    file_name_max=("file_name", "max"),
    file_hash_min=("file_hash", "min"),
    file_hash_max=("file_hash", "max"),
    create_dt_min=("create_dt", "min"),
    create_dt_max=("create_dt", "max"),
    picture_dt_min=("picture_dt", "min"),
    picture_dt_max=("picture_dt", "max")).reset_index().sort_values(by=['file_count'], ascending=False)
    

    df_tmp['key_col'] = key_col 
    file_path=csv_path.replace("result.csv", f"result_{key_col}.csv")
    df_tmp.to_csv( f"{file_path}", index=False, encoding="utf-8-sig") 
    print(f"완료: {len(df_tmp)}개의 파일 처리됨. 결과 -> {file_path}")

print(df[:10])
# 해쉬별로 파일 만들기 
save_file_hash(df, 'file_hash') 
save_file_hash(df, 'file_name')
