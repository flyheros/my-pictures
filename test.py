import streamlit as st
import pandas as pd

# 먼저 데이터프레임이 제대로 생성되었는지 확인
try:
    # 기존 get_file_stat 함수 대신 테스트용 데이터 직접 생성
    test_data = {
        '파일해쉬': ['hash1', 'hash2', 'hash3'],
        '파일명': ['file1.jpg', 'file2.png', 'file3.jpg'],
        '파일생성일': ['2023-01-01', '2023-01-02', '2023-01-03'],
        '파일수정일': ['2023-02-01', '2023-02-02', '2023-02-03'],
        '촬영일': ['2022-12-01', '2022-12-02', '2022-12-03']
    }
    df = pd.DataFrame(test_data)
    
    st.write("테스트 데이터 생성 완료")
    st.write(f"데이터프레임 형태: {df.shape}")
    
    # 정렬 옵션
    sort_column = st.selectbox("정렬할 컬럼 선택", df.columns)
    sort_ascending = st.radio("정렬 순서", ["오름차순", "내림차순"]) == "오름차순"
    
    # 정렬 실행
    df_sorted = df.sort_values(by=sort_column, ascending=sort_ascending)
    
    # 결과 출력
    st.write("### 정렬된 데이터:")
    st.dataframe(df_sorted)
    
except Exception as e:
    st.error(f"오류 발생: {e}")
    st.write("오류 세부 정보:", e.__class__.__name__)