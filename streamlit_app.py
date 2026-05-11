import streamlit as st
from openai import OpenAI

# ---------------------------------------------------
# 페이지 설정
# ---------------------------------------------------
st.set_page_config(
    page_title="NOIR TRAVEL",
    page_icon="✈️",
    layout="wide"
)

# ---------------------------------------------------
# 스타일
# ---------------------------------------------------
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Space Grotesk', sans-serif;
}

.stApp {
    background: radial-gradient(circle at top, #1a1a1a 0%, #070707 45%, #000000 100%);
    color: white;
}

/* 전체 여백 */
.block-container {
    padding-top: 2rem;
    padding-left: 3rem;
    padding-right: 3rem;
}

/* 헤더 */
.hero {
    position: relative;
    overflow: hidden;
    padding: 45px;
    border-radius: 32px;
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    backdrop-filter: blur(20px);
    margin-bottom: 28px;
}

.hero::before {
    content: "";
    position: absolute;
    width: 500px;
    height: 500px;
    background: radial-gradient(circle, rgba(255,255,255,0.08) 0%, transparent 70%);
    top: -250px;
    right: -150px;
}

.title {
    font-size: 72px;
    font-weight: 700;
    line-height: 0.9;
    letter-spacing: -3px;
    color: white;
}

.subtitle {
    margin-top: 18px;
    color: #9ca3af;
    font-size: 18px;
    line-height: 1.7;
    max-width: 650px;
}

/* 카드 */
.glass {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    backdrop-filter: blur(16px);
    border-radius: 28px;
    padding: 24px;
}

/* 사이드바 */
section[data-testid="stSidebar"] {
    background: #050505;
    border-right: 1px solid rgba(255,255,255,0.08);
}

/* 입력창 */
.stTextInput input {
    background-color: rgba(255,255,255,0.06) !important;
    color: white !important;
    border-radius: 16px !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
}

.stChatInput textarea {
    background-color: rgba(255,255,255,0.06) !important;
    color: white !important;
    border-radius: 18px !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
}

/* 셀렉트박스 */
.stSelectbox div[data-baseweb="select"] {
    background-color: rgba(255,255,255,0.06);
    border-radius: 16px;
}

/* 슬라이더 */
.stSlider {
    padding-top: 10px;
}

/* 채팅 메시지 */
.stChatMessage {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 24px;
    padding: 14px;
    margin-bottom: 12px;
}

/* 버튼 */
.stButton button {
    background: white;
    color: black;
    border-radius: 999px;
    border: none;
    padding: 10px 22px;
    font-weight: 600;
}

/* 태그 */
.tag {
    display: inline-block;
    padding: 10px 16px;
    margin: 6px;
    border-radius: 999px;
    background: rgba(255,255,255,0.06);
    color: #d1d5db;
    font-size: 14px;
    border: 1px solid rgba(255,255,255,0.08);
}

/* 작은 텍스트 */
.muted {
    color: #6b7280;
    font-size: 14px;
}

/* 구분선 */
hr {
    border-color: rgba(255,255,255,0.08);
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# 헤더
# ---------------------------------------------------
st.markdown("""
<div class="hero">
    <div class="title">
        NOIR<br>
        TRAVEL
    </div>

    <div class="subtitle">
        감각적인 여행을 위한 AI 여행 메이트.<br>
        도시의 무드, 로컬 스팟, 숨겨진 플레이스를 추천해줍니다.
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# 사이드바
# ---------------------------------------------------
with st.sidebar:

    st.markdown("## ✈️ Travel Setup")

    destination = st.text_input(
        "Destination",
        placeholder="Tokyo, Paris, Seoul..."
    )

    vibe = st.selectbox(
        "Mood",
        [
            "City Pop",
            "Minimal",
            "Vintage",
            "Luxury",
            "Street",
            "Night Vibes",
            "Art & Culture"
        ]
    )

    budget = st.select_slider(
        "Budget",
        options=["Low", "Medium", "High"]
    )

    days = st.slider(
        "Trip Days",
        min_value=1,
        max_value=14,
        value=4
    )

    st.markdown("---")

    st.markdown("### Recommended Prompts")

    st.markdown("""
    <div class="tag">도쿄 힙한 카페 추천</div>
    <div class="tag">오사카 빈티지샵 알려줘</div>
    <div class="tag">파리 야경 코스 짜줘</div>
    <div class="tag">현지인 맛집 추천</div>
    """, unsafe_allow_html=True)

# ---------------------------------------------------
# API KEY
# ---------------------------------------------------
openai_api_key = st.text_input(
    "OpenAI API Key",
    type="password",
    placeholder="sk-..."
)

if not openai_api_key:
    st.info("OpenAI API 키를 입력하면 여행 챗봇을 사용할 수 있어요 ✨")
else:

    client = OpenAI(api_key=openai_api_key)

    # ---------------------------------------------------
    # 세션 상태
    # ---------------------------------------------------
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content":
                "✈️ 어디로 떠나고 싶어?\n\n"
                "도시의 분위기에 맞는 여행 코스를 만들어줄게."
            }
        ]

    # ---------------------------------------------------
    # 채팅 출력
    # ---------------------------------------------------
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # ---------------------------------------------------
    # 입력창
    # ---------------------------------------------------
    if prompt := st.chat_input("Ask your next destination..."):

        st.session_state.messages.append({
            "role": "user",
            "content": prompt
        })

        with st.chat_message("user"):
            st.markdown(prompt)

        # ---------------------------------------------------
        # 시스템 프롬프트
        # ---------------------------------------------------
        system_prompt = f"""
        너는 힙하고 감각적인 여행 큐레이터 AI다.

        사용자의 여행 정보:
        - 여행지: {destination}
        - 무드: {vibe}
        - 예산: {budget}
        - 여행 기간: {days}일

        답변 스타일:
        - 트렌디하고 세련된 톤
        - 감성적인 문장
        - 보기 좋은 구성
        - 숨겨진 로컬 스팟 추천
        - 카페/바/빈티지샵/포토스팟 포함
        - 여행 코스는 시간대별 정리
        - 너무 딱딱하지 않게
        """

        # ---------------------------------------------------
        # GPT 응답
        # ---------------------------------------------------
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
            stream=True
        )

        # ---------------------------------------------------
        # 출력
        # ---------------------------------------------------
        with st.chat_message("assistant"):
            response = st.write_stream(stream)

        st.session_state.messages.append({
            "role": "assistant",
            "content": response
        })
