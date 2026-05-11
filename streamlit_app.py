import streamlit as st
from openai import OpenAI

# -----------------------------
# 페이지 설정
# -----------------------------
st.set_page_config(
    page_title="AI Travel Mate",
    page_icon="✈️",
    layout="wide"
)

# -----------------------------
# 커스텀 CSS
# -----------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"]  {
    font-family: 'Pretendard', sans-serif;
}

.main {
    background: linear-gradient(180deg, #0F172A 0%, #111827 100%);
    color: white;
}

.stApp {
    background: linear-gradient(135deg, #0f172a 0%, #111827 50%, #1e293b 100%);
}

.hero {
    padding: 40px 30px;
    border-radius: 28px;
    background: rgba(255,255,255,0.06);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255,255,255,0.1);
    margin-bottom: 24px;
}

.hero-title {
    font-size: 48px;
    font-weight: 700;
    color: white;
    margin-bottom: 10px;
}

.hero-sub {
    font-size: 18px;
    color: #CBD5E1;
    line-height: 1.6;
}

.card {
    background: rgba(255,255,255,0.05);
    border-radius: 24px;
    padding: 20px;
    border: 1px solid rgba(255,255,255,0.08);
    margin-top: 20px;
}

.small-title {
    font-size: 20px;
    font-weight: 600;
    color: white;
    margin-bottom: 12px;
}

.tag {
    display: inline-block;
    padding: 8px 14px;
    background: rgba(255,255,255,0.08);
    border-radius: 999px;
    margin: 5px;
    color: #E2E8F0;
    font-size: 14px;
}

.stChatMessage {
    background: rgba(255,255,255,0.04);
    border-radius: 18px;
    padding: 10px;
    border: 1px solid rgba(255,255,255,0.06);
}

.stTextInput > div > div > input {
    background-color: rgba(255,255,255,0.08);
    color: white;
}

.stChatInput textarea {
    background-color: rgba(255,255,255,0.08) !important;
    color: white !important;
}

.block-container {
    padding-top: 2rem;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# 헤더
# -----------------------------
st.markdown("""
<div class="hero">
    <div class="hero-title">✈️ AI Travel Mate</div>
    <div class="hero-sub">
        여행 일정을 추천하고, 맛집과 관광지를 찾아주고,<br>
        여행 스타일에 맞는 플랜을 만들어주는 AI 여행 챗봇
    </div>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# 사이드바
# -----------------------------
with st.sidebar:
    st.markdown("## 🌍 여행 설정")

    destination = st.text_input("📍 여행지", placeholder="예: 도쿄, 파리, 뉴욕")

    travel_style = st.selectbox(
        "🎨 여행 스타일",
        [
            "감성 여행",
            "맛집 투어",
            "휴양",
            "액티비티",
            "혼자 여행",
            "우정 여행",
            "럭셔리 여행"
        ]
    )

    budget = st.select_slider(
        "💸 예산",
        options=["저예산", "보통", "고급"]
    )

    days = st.slider("📅 여행 기간", 1, 14, 3)

    st.markdown("---")
    st.markdown("### ✨ 추천 질문")
    st.markdown("""
    <div class="tag">도쿄 3박4일 일정 짜줘</div>
    <div class="tag">현지인 맛집 추천해줘</div>
    <div class="tag">감성 카페 알려줘</div>
    <div class="tag">야경 명소 추천</div>
    """, unsafe_allow_html=True)

# -----------------------------
# API 키 입력
# -----------------------------
openai_api_key = st.text_input(
    "🔑 OpenAI API Key",
    type="password",
    placeholder="OpenAI API 키를 입력하세요"
)

if not openai_api_key:
    st.info("OpenAI API 키를 입력하면 여행 챗봇을 사용할 수 있어요 ✨")
else:

    client = OpenAI(api_key=openai_api_key)

    # 세션 상태
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "안녕하세요 ✈️ 여행 계획을 도와드릴게요! 여행지를 알려주세요 😊"
            }
        ]

    # 기존 메시지 출력
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 입력창
    if prompt := st.chat_input("여행에 대해 물어보세요..."):

        # 사용자 메시지 저장
        st.session_state.messages.append({
            "role": "user",
            "content": prompt
        })

        with st.chat_message("user"):
            st.markdown(prompt)

        # 시스템 프롬프트
        system_prompt = f"""
        너는 감성적인 AI 여행 플래너야.

        사용자의 여행 스타일:
        - 여행지: {destination}
        - 여행 스타일: {travel_style}
        - 예산: {budget}
        - 여행 기간: {days}일

        다음과 같이 답변해:
        - 감성적이고 친근한 톤
        - 보기 좋게 이모지 활용
        - 일정은 시간대별로 정리
        - 맛집/카페/관광지 추천 포함
        - 여행 팁도 함께 제공
        """

        # GPT 응답 생성
        stream = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                *[
                    {
                        "role": m["role"],
                        "content": m["content"]
                    }
                    for m in st.session_state.messages
                ]
            ],
            stream=True,
        )

        # 응답 출력
        with st.chat_message("assistant"):
            response = st.write_stream(stream)

        # 응답 저장
        st.session_state.messages.append({
            "role": "assistant",
            "content": response
        })
