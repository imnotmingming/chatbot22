import streamlit as st
from openai import OpenAI

# 제목과 설명 표시
st.title("💬 챗봇")
st.write(
    "이 앱은 OpenAI의 GPT-3.5 모델을 사용하여 응답을 생성하는 간단한 챗봇입니다. "
    "이 앱을 사용하려면 OpenAI API 키가 필요합니다. "
    "API 키는 아래 링크에서 발급받을 수 있습니다.\n\n"
    "👉 https://platform.openai.com/account/api-keys\n\n"
    "또한 아래 튜토리얼을 통해 이 앱을 단계별로 만드는 방법을 배울 수 있습니다.\n\n"
    "👉 https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps"
)

# 사용자에게 OpenAI API 키 입력받기
# 또는 ./streamlit/secrets.toml 파일에 저장 후 st.secrets로 불러올 수도 있음
openai_api_key = st.text_input("OpenAI API 키", type="password")

if not openai_api_key:
    st.info("계속하려면 OpenAI API 키를 입력해주세요.", icon="🗝️")
else:

    # OpenAI 클라이언트 생성
    client = OpenAI(api_key=openai_api_key)

    # 세션 상태에 채팅 메시지 저장
    # 새로고침해도 대화 내용 유지됨
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # 기존 채팅 메시지 출력
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 사용자 입력창 생성
    if prompt := st.chat_input("무엇이든 물어보세요!"):

        # 사용자 메시지 저장 및 출력
        st.session_state.messages.append({
            "role": "user",
            "content": prompt
        })

        with st.chat_message("user"):
            st.markdown(prompt)

        # OpenAI API로 응답 생성
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )

        # 응답 스트리밍 출력 후 세션에 저장
        with st.chat_message("assistant"):
            response = st.write_stream(stream)

        st.session_state.messages.append({
            "role": "assistant",
            "content": response
        })
