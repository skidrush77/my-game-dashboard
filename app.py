import streamlit as st
import pandas as pd

# 웹사이트 제목 설정
st.title('로얄호텔 퍼널분석')

# 데이터 소스 URL
DATA_URL = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vSykU-SnMVdxJvYHRPapTJFWUcgjHFUMfL4t48poiYqpfaVGCveH2l7B_I6XCXjRTdEZy5gTdm2sZiw/pub?gid=1019645524&single=true&output=csv'

@st.cache_data
def load_data():
    # 데이터 구조가 복잡하므로 header=2 (3번째 줄이 헤더)로 읽기
    data = pd.read_csv(DATA_URL, header=2)
    # 필요한 컬럼만 선택 (ID, Step 이름, Count)
    # CSV 실제 컬럼명: 'ID', '재플린', 'cnt' (Chunk 0 확인 기반)
    # 참고: 빈 컬럼이 많아서 이름을 명시적으로 선택
    # 첫번째 섹션(재플린)만 사용
    if '재플린' in data.columns and 'cnt' in data.columns:
        df_selected = data[['ID', '재플린', 'cnt']].copy()
        df_selected.columns = ['ID', 'Step', 'Users']
        # 데이터 정제: Step이 NaN인 행 제거
        df_selected = df_selected.dropna(subset=['Step'])
        return df_selected
    else:
        return data # fallback

try:
    # 데이터 불러오기
    df = load_data()

    # SECTION 1: 대시보드 상단 - 그래프 (Bar Chart)
    st.subheader('플레이어 진행 상황 (Bar Chart)')
    
    # Bar Chart 그리기: X축=Step, Y축=Users
    if not df.empty and 'Step' in df.columns and 'Users' in df.columns:
        st.bar_chart(data=df, x='Step', y='Users')
    else:
        st.write("시각화할 데이터를 불러오지 못했습니다.")

    # SECTION 2: 하단 - 데이터 표
    st.subheader('상세 데이터 목록')
    st.dataframe(df)

except Exception as e:
    st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")

