import streamlit as st
import openai
import requests

# GitHub에서 data.txt 파일을 로드하는 함수
def load_data_from_github():
    url = "https://raw.githubusercontent.com/hyunnn24/RAG-test/main/data.txt"
    response = requests.get(url)
    if response.status_code == 200:
        return response.text.splitlines()
    else:
        st.error("data.txt 파일을 로드하는 데 실패했습니다.")
        return []

# 데이터 로드
documents = load_data_from_github()

# Streamlit UI 구성
st.title('RAG 모델 데모')
st.write("OpenAI API를 호출하여 응답을 받는 예제입니다.")

# OpenAI API 키 입력 받기
api_key = st.text_input("OpenAI API 키를 입력하세요:", type="password")

# 사용자 입력 받기
user_query = st.text_input("질문을 입력하세요:")

# 간단한 문서 검색 함수
def search_documents(query, docs):
    return [doc for doc in docs if query.lower() in doc.lower()]

# API 호출 함수
def call_openai_api(query, context, api_key):
    openai.api_key = api_key
    if context:
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Context: {context}\n\nQuery: {query}\n\nAnswer:"}
        ]
    else:
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Query: {query}\n\nAnswer:"}
        ]
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=150
    )
    return response.choices[0].message['content'].strip()

# 버튼 클릭시 API 호출
if st.button("응답 받기"):
    if not api_key:
        st.error("API 키를 입력하세요.")
    elif not user_query:
        st.error("질문을 입력하세요.")
    else:
        with st.spinner('문서 검색 중...'):
            # 문서 검색 단계
            relevant_docs = search_documents(user_query, documents)
            context = " ".join(relevant_docs)
            
            with st.spinner('OpenAI API 호출 중...'):
                # 텍스트 생성 단계
                try:
                    answer = call_openai_api(user_query, context, api_key)
                    st.write("응답:")
                    st.write(answer)
                except Exception as e:
                    st.error(f"오류 발생: {e}")
