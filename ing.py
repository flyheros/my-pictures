import os
import pandas as pd
from PIL import Image
from datetime import datetime
import hashlib
from PIL.ExifTags import TAGS
# import streamlit as st
import pandas as pd

# 설정 

csv_path = r"D:\workspace\my-pictures\file_result.csv"


df = pd.read_csv(csv_path)

print(df.columns)



df_stat = df.groupby(['파일해쉬쉬']).agg({"파일생성일":"count", "파일경로":"min", "파일경로": "max"}).reset_index()
df['파일생성일'] = pd.to_datetime(df['파일생성일'])
df['파일수정일'] = pd.to_datetime(df['파일수정일'])
# df['촬영일'] = pd.to_datetime(df['촬영일'])



촬용일에서 YYYY-MM-DD를 추출 
# print(df[pd.to_datetime(df['촬영일'], errors='coerce').isna()]['촬영일'].drop_duplicates())
print(df['촬영일'].apply(lambda x : x[:8])[:10])

print('-----------------------------------------')
# df['create_dt'] = df['파일생성일'].
 
print(df.info())

df['create_dt'] = df['파일생성일'].dt.to_period('D')
df['update_dt'] = df['파일수정일'].dt.to_period('D')
df['picture_dt'] = df['촬영일'].dt.to_period('D')


print(df[:1])
# ------------------------------------
# df_stat = df[:1]
# st.set_page_config(layout='wide')


 

# # 가로로 2열 생성
# col1, col2 = st.columns([1, 1])  # 비율을 바꿔도 됨

# # 정렬 옵션
# with col1:
#     col1_1, col1_2 = st.columns([1,1])
#     with col1_1:
#         sort_column = st.selectbox("정렬할 컬럼 선택", df.columns)
#     with col1_2:
#         sort_ascending = st.radio("정렬 순서", ["오름차순", "내림차순"]) == "오름차순"
#     df_sorted = df.sort_values(by=sort_column, ascending=sort_ascending)

# # 페이징 처리
# with col2:
#     items_per_page = 10
#     total_pages = (len(df_sorted) - 1) // items_per_page + 1
#     page = st.number_input("페이지 번호", min_value=1, max_value=total_pages, value=1, step=1)


# st.write(f"총 {len(df)}건")
# start_idx = (page - 1) * items_per_page
# end_idx = start_idx + items_per_page
# st.write(f"**페이지 {page} / {total_pages}**")
# st.dataframe(df_sorted.iloc[start_idx:end_idx].reset_index(drop=True))
 