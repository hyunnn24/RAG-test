import streamlit as st
import openai

# OpenAI API 키 설정
openai.api_key = 'your-openai-api-key'

# Streamlit UI 구성
st.title('RAG 모델 데모')
st.write("OpenAI API를 호출하여 응답을 받는 예제입니다.")

# 문서 저장소 (예시로 간단한 리스트를 사용)
documents = [
    "OpenAI는 인공지능 연구소입니다.",
    "Streamlit은 데이터 과학을 위한 웹 애플리케이션 프레임워크입니다.",
    "Python은 널리 사용되는 프로그래밍 언어입니다."
]

# 사용자 입력 받기
user_query = st.text_input("질문을 입력하세요:")

# 간단한 문서 검색 함수
def search_documents(query):
    return [doc for doc in documents if query.lower() in doc.lower()]

# API 호출 함수
def call_openai_api(query, context):
    prompt = f"Context: {context}\n\nQuery: {query}\n\nAnswer:"
    response = openai.Completion.create(
        engine="text-davinci-003",  # 사용할 OpenAI 모델 엔진
        prompt=prompt,
        max_tokens=150  # 응답으로 받을 최대 토큰 수
    )
    return response.choices[0].text.strip()

# 버튼 클릭시 API 호출
if st.button("응답 받기"):
    if user_query:
        with st.spinner('문서 검색 중...'):
            # 문서 검색 단계
            relevant_docs = search_documents(user_query)
            context = " ".join(relevant_docs)
            
            if context:
                with st.spinner('OpenAI API 호출 중...'):
                    # 텍스트 생성 단계
                    answer = call_openai_api(user_query, context)
                    st.write("응답:")
                    st.write(answer)
            else:
                st.write("관련 문서를 찾을 수 없습니다.")
    else:
        st.write("질문을 입력하세요.")
