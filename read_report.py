import os
import pandas as pd
from PIL import Image
from datetime import datetime
import imagehash
import hashlib
from PIL.ExifTags import TAGS

# 설정 

csv_path = r"D:\workspace\my-pictures\file_result.csv"


df = pd.read_csv(csv_path)

print(df.columns)


df_1 = df.groupby(['파일해쉬쉬']).agg({"파일생성일":"count", "파일경로":"min", "파일경로": "max"}).reset_index()


print(df_1[df_1['파일생성일']>=2].sort_values(by="파일경로", ascending=False))
print('===========')
print(df_1[df_1['파일경로']>=2]['파일경로'].drop_duplicates())