import streamlit as st
import time 
import json
import streamlit.components.v1 as components
import os
from PIL import Image
# =========================================================
# 페이지 기본 설정
# =========================================================
st.set_page_config(
    page_title="무면허진료소 정합 건강 문진표",
    page_icon="🩺",
    layout="centered"
)

# =========================================================
# 기본 스타일
# =========================================================
st.markdown("""
<style>
.block-container {
    max-width: 864px;
    padding-top: 1.2rem;
    padding-bottom: 3rem;
}

.hero-card {
    background: linear-gradient(135deg, #ff7eb6 0%, #ff5ea2 50%, #ffb3d5 100%);
    border-radius: 28px;
    padding: 30px 26px;
    color: white;
    box-shadow: 0 18px 42px rgba(255, 94, 162, 0.22);
    margin-bottom: 14px;
}

.info-card {
    background: white;
    border-radius: 22px;
    padding: 18px 18px;
    border: 1px solid #f1e3ea;
    box-shadow: 0 10px 24px rgba(0,0,0,0.05);
    margin-bottom: 14px;
}

.question-card {
    background: white;
    border-radius: 22px;
    padding: 18px 18px 8px 18px;
    border: 1px solid #f1e3ea;
    box-shadow: 0 10px 24px rgba(0,0,0,0.05);
    margin-bottom: 16px;
}

.result-card {
    background: white;
    border-radius: 24px;
    overflow: hidden;
    border: 1px solid #f1e3ea;
    box-shadow: 0 10px 26px rgba(0,0,0,0.06);
    margin-bottom: 16px;
}

.result-top {
    background: linear-gradient(135deg, #ff7eb6 0%, #ff5ea2 50%, #ffb3d5 100%);
    color: white;
    padding: 24px 22px;
}

.badge {
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 6px 8px;
    border-radius: 999px;
    background: #fff1f7;
    color: #d63384;
    font-size: 11px;
    font-weight: 700;
    border: 1px solid #ffd8e8;
    white-space: nowrap;
}
.badge-row{
    display:grid;
    grid-template-columns:repeat(4,1fr);
    gap:6px;
    width:100%;
}

.keyword {
    display: inline-block;
    padding: 7px 12px;
    border-radius: 999px;
    background: #ffe8f2;
    color: #c22574;
    font-size: 13px;
    font-weight: 700;
    margin-right: 6px;
    margin-bottom: 8px;
}

.title-xl {
    font-size: clamp(25px, 6vw, 34px);
    font-weight: 900;
    line-height: 1.2;
    margin-top: 8px;
    text-align: center;
    white-space: normal;
    word-break: keep-all;
}

.title-lg {
    font-size: clamp(18px, 4.5vw, 24px);
    font-weight: 900;
    line-height: 1.35;
    color: #241f24;
    white-space: normal;
    word-break: keep-all;
    overflow-wrap: anywhere

}

@media (max-width: 768px) {
    .title-xl {
        font-size: 20px !important;
    }
}

@media (max-width: 480px) {
    .title-xl {
        font-size: 16px !important;
    }
}

.body-text {
    color: #5b555d;
    font-size: 16px;
    line-height: 1.75;
}

.meta {
    color: #7b737b;
    font-size: 14px;
}

.section-title {
    color: #4c444a;
    font-size: 14px;
    font-weight: 800;
    margin-bottom: 8px;
}

.score-box {
    background: #fff8fc;
    border: 1px solid #f6dde9;
    border-radius: 18px;
    padding: 14px 16px;
    margin-top: 14px;
}

.loading-box {
    background: linear-gradient(135deg, #fff8fc 0%, #fff3f8 100%);
    border: 1px solid #f6dce8;
    border-radius: 18px;
    padding: 16px 18px;
    margin-top: 14px;
    margin-bottom: 14px;
    box-shadow: 0 8px 20px rgba(255, 94, 162, 0.08);
}

.loading-title {
    font-size: 14px;
    font-weight: 800;
    color: #c22574;
    margin-bottom: 8px;
}

.loading-text {
    font-size: 16px;
    font-weight: 700;
    color: #4d434b;
    line-height: 1.6;
    min-height: 48px;
}

.loading-sub {
    font-size: 13px;
    color: #8a7d86;
    margin-top: 8px;
}

.dot-wave {
    display: inline-block;
    letter-spacing: 2px;
    color: #ff5ea2;
    font-weight: 900;
}

.stButton > button {
    width: 100%;
    min-height: 54px;
    border-radius: 16px;
    font-size: 16px;
    font-weight: 700;
}

div[data-testid="stProgressBar"] > div > div {
    background-color: #ff6fa9;
}

hr {
    border: none;
    border-top: 1px solid #f1e3ea;
    margin: 14px 0 18px 0;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# 테스트 데이터
# 첨부 문서의 문항 내용을 그대로 반영
# =========================================================
PAGES = [
    {
        "key": "love",
        "title": "연애 관련 문제",
        "description": "현재 연애/외로움/소개팅 선호와 관련된 문항입니다.",
        "questions": [
            {
                "question": "Q1. 하루 중 ‘누구랑 같이 있었으면 좋겠다’는 생각을 하는 빈도는?",
                "options": [
                    ("① 거의 없음", 0),
                    ("② 주 1-2회", 5),
                    ("③ 주 3-4회", 10),
                    ("④ 주 5-6회", 15),
                    ("⑤ 거의 매일", 20),
                ],
            },
            {
                "question": "Q2. 혼자 벚꽃을 보게 된다면 가장 가까운 반응은?",
                "options": [
                    ("① 혼자서도 충분히 즐김", 0),
                    ("② 사진 찍고 바로 집 감", 5),
                    ("③ 살짝 아쉽지만 보긴 함", 10),
                    ("④ 커플들 보면 기분 이상해짐", 15),
                    ("⑤ “왜 나만 혼자야” 라는 생각이 듦", 20),
                ],
            },
            {
                "question": "Q3. 외로움을 느낄 때 가장 자주 하는 행동은?",
                "options": [
                    ("① 취미/운동/게임 등 혼자 잘 놀기", 0),
                    ("② 유튜브/넷플릭스 보면서 시간 보내기", 5),
                    ("③ 친구에게 연락하기", 10),
                    ("④ 의미 없이 SNS 계속 보기", 15),
                    ("⑤ 연락할 사람 찾다가 아무도 없어서 더 우울해짐", 20),
                ],
            },
            {
                "question": "Q4. 길 가다가 커플을 봤을 때 반응은?",
                "options": [
                    ("① 아무 생각 없음", 0),
                    ("② 그냥 지나감", 5),
                    ("③ 살짝 부럽다", 10),
                    ("④ 괜히 더 의식됨", 15),
                    ("⑤ 갑자기 외로움 급상승", 20),
                ],
            },
            {
                "question": "Q5. 미팅/소개팅 제안이 들어오면 당신은?",
                "options": [
                    ("① 정중히 거절함. 관심 없음", 0),
                    ("② 고민하다가 보통 안 나감", 5),
                    ("③ 조건 괜찮으면 나가봄", 10),
                    ("④ 일단 나가보고 판단", 15),
                    ("⑤ 개같이 환영", 20),
                ],
            },
        ],
    },
    {
        "key": "grade",
        "title": "성적 관련 문제",
        "description": "시험 준비와 공부 습관에 대한 문항입니다.",
        "questions": [
            {
                "question": "Q1. 언제 공부를 시작하는지?",
                "options": [
                    ("① 시험 2주 전부터 계획, 실행까지 완벽하게", 0),
                    ("② 시험 1주 전부터 슬슬 시작", 5),
                    ("③ 시험 3-4일 전부터 현실 인지", 10),
                    ("④ 시험 전날 밤 “아 망했다”", 15),
                    ("⑤ 시험 당일 “이게 뭐지?”", 20),
                ],
            },
            {
                "question": "Q2. 공부하다 딴짓하는 빈도는?",
                "options": [
                    ("① 폰 OFF, 완전 집중", 0),
                    ("② 가끔 딴짓함", 5),
                    ("③ 공부 : 딴짓 = 5 : 5", 10),
                    ("④ 딴짓하다가 가끔 공부함", 15),
                    ("⑤ 유튜브 보다가 이따금씩 시험 생각함", 20),
                ],
            },
            {
                "question": "Q3. 시험 전날 나는?",
                "options": [
                    ("① 여유롭게 복습", 0),
                    ("② 부족한 부분 정리", 5),
                    ("③ 처음 보는 내용 보고 당황하기", 10),
                    ("④ “범위가 뭐지?”", 15),
                    ("⑤ 과목 이름이 낯섦", 20),
                ],
            },
            {
                "question": "Q4. 중간고사 기간 동안 술 마시는 빈도는?",
                "options": [
                    ("① 아예 안 마심", 0),
                    ("② 주 1회 (적당히 환기용)", 5),
                    ("③ 주 2-3회 (시험? 그게 뭐였지)", 10),
                    ("④ 거의 격일로 마심 (공부와 병행 중)", 15),
                    ("⑤ 시험 기간 = 술 시즌 (거의 매일)", 20),
                ],
            },
            {
                "question": "Q5. 요즘 내 필기 상태는?",
                "options": [
                    ("① 깔끔 + 완벽 정리됨", 0),
                    ("② 중요한 것만 정리됨", 5),
                    ("③ 필기 있긴 하지만 이해는 안 됨", 10),
                    ("④ 필기 못 읽음", 15),
                    ("⑤ 필기? 그런 거 안 함", 20),
                ],
            },
        ],
    },
    {
        "key": "campus",
        "title": "대학생활 관련 문제",
        "description": "생활 리듬, 스트레스, 인간관계 상태에 대한 문항입니다.",
        "questions": [
            {
                "question": "Q1. 요즘 당신의 취침 루틴은?",
                "options": [
                    ("① “이래야 개운하지” 12시 이전 규칙적인 취침", 0),
                    ("② “그래도 사람답게 살자!” 12시 전후로 취침", 5),
                    ("③ “조금만 더…” 하다 1-3시쯤 취침", 10),
                    ("④ “이제 자야지…” 거의 매일 3-5시 취침", 15),
                    ("⑤ “새벽 공기 좋다” 해 뜨는 거 보고 잠", 20),
                ],
            },
            {
                "question": "Q2. 핸드폰과 당신의 관계는?",
                "options": [
                    ("① 일부러 안 보려고 함", 0),
                    ("② 필요할 때만 보는 편", 5),
                    ("③ 할 거 없으면 바로 폰 켬", 10),
                    ("④ 의미 없이 계속 켰다 끄고 켰다 끄고 반복", 15),
                    ("⑤ 하루종일 손에 붙어 있음", 20),
                ],
            },
            {
                "question": "Q3. 요즘 당신의 상태는?",
                "options": [
                    ("① 컨디션 매우 좋음 짜릿함", 0),
                    ("② 적당히 좋을 때도 있음", 5),
                    ("③ 그냥 하루하루 버티는 중", 10),
                    ("④ 항상 피곤하고 의욕 없음", 15),
                    ("⑤ “아무것도 하기 싫다”가 기본값", 20),
                ],
            },
            {
                "question": "Q4. 최근 당신의 인간관계 상태는?",
                "options": [
                    ("① 사람 만나면 에너지 충전됨", 0),
                    ("② 적당히 만나고 잘 지냄", 5),
                    ("③ 가끔 보긴 하지만 적당히 거리 둠", 10),
                    ("④ 사람 만나면 기 빨림", 15),
                    ("⑤ 사람 만나는 거 자체가 너무 귀찮음", 20),
                ],
            },
            {
                "question": "Q5. 당신의 스트레스 해소 방식은?",
                "options": [
                    ("① 확실한 관리 루틴이 있음", 0),
                    ("② 나름대로의 해소 방법이 있음", 5),
                    ("③ 일단 자고 나면 괜찮아지겠지", 10),
                    ("④ 릴스나 쇼츠 보다가 시간 순삭", 15),
                    ("⑤ 없음. 그냥 쌓임", 20),
                ],
            },
        ],
    },
]

# =========================================================
# 결과 유형 데이터
# 문서 기준:
# - 각 영역 70점 이상 여부로 판정
# - 총 8가지 유형 필요
# 문서에 일부 유형명만 있어서 나머지는 자연스럽게 보완
# =========================================================
RESULT_MAP = {
    (0, 0, 0): {
        "title": "이게 되네",
        "subtitle": "아직은 멀쩡한 편",
        "image": "images/results/normal.jpg",
        "keywords": ["균형", "무난", "안정"],
        "prescription": [
            "당신 비법이 뭐죠..?!",
            "지금 루틴만 너무 무너지지 않게 유지하면 졸업까쥐~,무난하게 버틸 수 있어요.",
            "자! 축제 즐겨~!!!"
        ],
    },
    (1, 0, 0): {
        "title": "벚꽃 시즌 최대 피해자",
        "subtitle": "연애 결핍형",
        "image": "images/results/love.jpg",
        "keywords": ["연애", "외로움", "설렘부족"],
        "prescription": [
            "누구보다 강하게 연애를 하고 싶어하는군요! 이 정도면 떨어지는 벚꽃만 봐도 눈물이 또르륵하겠는걸요.",
            "연애를 하고 싶다면 역시 플러팅이죠",
            "간식 처방: 초콜릿 하나 들고 가서 플러팅 하고 오세요!."
        ],
    },
    (0, 1, 0): {
        "title": "실수로 대학을 왔어요",
        "subtitle": "시험 불안형",
        "image": "images/results/grade.jpg",
        "keywords": ["시험", "벼락치기", "현실자각"],
        "prescription": [
            "고학력자가 될 생각이 일도 없었는데 실수로 대학을 오신 당신!",
            "이왕 온 김에 공부를 한 번 시작해보는 건 어떨까요?",
            "간식 처방: 일단 당부터 챙겨~금강산도 식후경!"
        ],
    },
    (0, 0, 1): {
        "title": "스트레스 많이 받을 거야~",
        "subtitle": "생활 지침형",
        "image": "images/results/campus.jpg",
        "keywords": ["수면", "피로", "무기력"],
        "prescription": [
            "당신의 일상이 힘겨운 게 아니라 일상이 당신을 힘겨워하는 중입니다! ",
            "간식 처방: 당장 오늘은 일찍 눕기."
        ],
    },
    (1, 1, 0): {
        "title": "세상이 호락호락하지 않죠?",
        "subtitle": "연애 결핍형+시험 불안형",
        "image": "images/results/22.jpg",
        "keywords": ["연애", "시험", "멘붕"],
        "prescription": [
            "괜찮아요 당신도 호락호락하지 않으니까. Queen Never Cry!",
            "연애도, 학업도 쉽지 않지만 퀸은 절대 울지 않죠. 잘하고 있어요! ",
            "간식 처방: Queen력을 모두 모아, 끌어올려~!"
        ],
    },
    (1, 0, 1): {
        "title": "세상이 호락호락하지 않죠?",
        "subtitle": "연애 결핍형+생활 지침형",
        "image": "images/results/22.jpg",
        "keywords": ["외로움", "피로", "감정소모"],
        "prescription": [
            "괜찮아요 당신도 호락호락하지 않으니까. Queen Never Cry!",
            "연애도, 일상도 쉽지 않지만 퀸은 절대 울지 않죠. 잘하고 있어요! ",
            "간식 처방: Queen력을 모두 모아, 끌어올려~!"
        ],
    },
    (0, 1, 1): {
        "title": "세상이 호락호락하지 않죠?",
        "subtitle": "시험 불안형+생활 지침형",
        "image": "images/results/22.jpg",
        "keywords": ["시험", "피로", "번아웃"],
        "prescription": [
            "괜찮아요 당신도 호락호락하지 않으니까. Queen Never Cry!",
            "학업도, 일상도 쉽지 않지만 퀸은 절대 울지 않죠. 잘하고 있어요! ",
            "간식 처방: Queen력을 모두 모아, 끌어올려~!"
        ],
    },
    (1, 1, 1): {
        "title": "대학생학대는 거꾸로 해도 대학생학대",
        "subtitle": "전영역 위험형",
        "image": "images/results/all_risk.jpg",
        "keywords": ["연애", "시험", "생활", "총체적난국"],
        "prescription": [
            "이럴 수가, 연애는 하고 싶고, 공부는 하기 싫고, 학교에서 기도 쭉쭉 빨리고 있는 상황이군요! ",
            "나도 모르게 학대당하고 있는 대학생이랍니다.",
            "간식 처방: 달콤한 약과와 함께 생활을 되돌아보는 여유를 가지는 건 어떨까요?."
        ],
    },
}

# =========================================================
# 세션 상태 초기화
# =========================================================
if "page_index" not in st.session_state:
    st.session_state.page_index = 0  # 0=표지, 1=연애, 2=성적, 3=대학생활, 4=결과

if "responses" not in st.session_state:
    st.session_state.responses = {
        "love": [None] * 5,
        "grade": [None] * 5,
        "campus": [None] * 5,
    }

# =========================================================
# 유틸 함수
# =========================================================
def go_to_page(idx: int):
    st.session_state.page_index = idx
    st.rerun()

def get_section_score(section_key: str) -> int:
    values = st.session_state.responses[section_key]
    return sum(v for v in values if v is not None)

def all_answered(section_key: str) -> bool:
    return all(v is not None for v in st.session_state.responses[section_key])

def all_test_answered() -> bool:
    return all(all_answered(section["key"]) for section in PAGES)

def get_progress_value() -> float:
    # 2~4페이지 동안 진행률 표시 요청 반영
    # 1페이지 표지는 제외, 2/3/4 페이지만 진행률로 계산
    current = st.session_state.page_index
    if current <= 1:
        return 1 / 3
    if current == 2:
        return 2 / 3
    return 1.0

def get_result_key():
    love_high = 1 if get_section_score("love") >= 70 else 0
    grade_high = 1 if get_section_score("grade") >= 70 else 0
    campus_high = 1 if get_section_score("campus") >= 70 else 0
    return (love_high, grade_high, campus_high)
import json
import streamlit.components.v1 as components

def render_rotating_message_box(section_title: str):
    messages = [
        f"{section_title}에 알맞은 처방을 고민 중이에요...",
        "당신에게 어떤 고민이 있죠?",
        "오늘 잘 찾아오셨어요.",
        "답변을 바탕으로 상태를 정리하고 있어요...",
        "조금만 더 보면 당신의 유형이 보여요.",
        "지금 당신에게 맞는 결과를 고민 중이에요...",
    ]
    messages_js = json.dumps(messages, ensure_ascii=False)

    html = """
     <style>
    .loading-box {
        background: linear-gradient(135deg, #fff8fc 0%, #fff3f8 100%);
        border: 1px solid #f2c8da;
        border-radius: 18px;
        padding: 16px 18px;
        margin-top: 14px;
        margin-bottom: 14px;
        box-shadow: 0 8px 20px rgba(255, 94, 162, 0.08);
        text-align: left;
        box-sizing: border-box;
        width: 100%;
    }

    .loading-title {
        font-size: 13px;
        font-weight: 800;
        color: #c22574;
        margin-bottom: 8px;
    }

    .loading-text {
        font-size: 15px;
        font-weight: 700;
        color: #4d434b;
        line-height: 1.6;
        min-height: 44px;
        transition: opacity 0.2s ease;
    }

    .loading-sub {
        font-size: 12px;
        color: #8a7d86;
        margin-top: 8px;
        margin-bottom: 10px;
    }

    .dots-loading {
        display: flex;
        justify-content: flex-start;
        align-items: center;
        gap: 6px;
    }

    .dots-loading span {
        width: 5px;
        height: 5px;
        border-radius: 999px;
        background: #ff5ea2;
        opacity: 0.25;
        transform: scale(0.9);
        display: inline-block;
        animation: dotBounce 1.2s infinite ease-in-out;
    }

    .dots-loading span:nth-child(1) {
        animation-delay: 0s;
    }

    .dots-loading span:nth-child(2) {
        animation-delay: 0.3s;
    }

    .dots-loading span:nth-child(3) {
        animation-delay: 0.6s;
    }

    @keyframes dotBounce {
        0%, 80%, 100% {
            opacity: 0.22;
            transform: translateY(0) scale(0.9);
        }
        40% {
            opacity: 1;
            transform: translateY(-3px) scale(1.18);
        }
    }
    </style>

    <div class="loading-box">
        <div class="loading-title">문진 분석 중</div>
        <div class="loading-text" id="loading-message"></div>
        <div class="loading-sub">잠시만요 기다려주세요</div>
        <div class="dots-loading">
            <span></span>
            <span></span>
            <span></span>
        </div>
    </div>
   
 <script>
    const messages = __MESSAGES__;
    let currentIndex = 0;
    const messageEl = document.getElementById("loading-message");
    const dots = document.querySelectorAll(".dot-wave span");

    function showMessage(index) {
        messageEl.style.opacity = "0.25";
        setTimeout(() => {
            messageEl.textContent = messages[index];
            messageEl.style.opacity = "1";
        }, 150);
    }

    showMessage(currentIndex);
    animateDots();

    setInterval(() => {
        currentIndex = (currentIndex + 1) % messages.length;
        showMessage(currentIndex);
    }, 4000);
    </script>

    """.replace("__MESSAGES__", messages_js)

    components.html(html, height=165)

# =========================================================
# 1페이지 표지
# =========================================================
if st.session_state.page_index == 0:
    st.markdown("""
    <div class="hero-card">
        <div class="meta" style="color:#fff6fb; font-weight:700;">무면허 진료소</div>
        <div class="title-xl">종합 건강 문진표</div>
        <div class="body-text" style="color:white; margin-top:12px;">
            연애, 성적, 대학생활 상태를 가볍게 체크하고<br>
            마지막 결과 유형에 따라 간식 처방을 받아보세요.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="info-card">
        <div class="section-title">진행 안내</div>
        <div class="body-text">
            총 3개 영역, 각 영역당 5문항입니다.<br>
            각 페이지에서 5개 문항에 모두 답하면 다음으로 넘어갈 수 있어요.
        </div>
        <hr>
        <div class="badge-row">
            <span class="badge">연애 5문항</span>
            <span class="badge">성적 5문항</span>
            <span class="badge">대학생활 5문항</span>
            <span class="badge">결과 8유형</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("테스트 시작"):
        go_to_page(1)

# =========================================================
# 2~4페이지 문항 화면
# =========================================================
elif st.session_state.page_index in [1, 2, 3]:
    section = PAGES[st.session_state.page_index - 1]
    section_key = section["key"]

    # 진행률 바
    st.markdown(
        f"<div class='meta'>진행률 · {st.session_state.page_index}/3 영역</div>",
        unsafe_allow_html=True
    )
    st.progress(get_progress_value())

    st.markdown(
        f"""
        <div class="hero-card">
            <div class="meta" style="color:#fff6fb; font-weight:700;">{st.session_state.page_index + 1} 페이지</div>
            <div class="title-xl">{section["title"]}</div>
            <div class="body-text" style="color:white; margin-top:10px;">
                {section["description"]}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="info-card">
            <div class="section-title">응답 방식</div>
            <div class="body-text">
                각 문항마다 가장 가까운 보기를 하나씩 선택하세요.<br>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # 문항 5개 한 페이지 표시
    for idx, q in enumerate(section["questions"]):
        st.markdown(
            f"""
            <div class="question-card">
                <div class="title-lg">{q["question"]}</div>
            """,
            unsafe_allow_html=True
        )

        labels = [label for label, _ in q["options"]]
        values = [score for _, score in q["options"]]

        current_value = st.session_state.responses[section_key][idx]
        selected_index = values.index(current_value) if current_value in values else None

        selected_label = st.radio(
            label=f"{section_key}_{idx}",
            options=labels,
            index=selected_index if selected_index is not None else None,
            label_visibility="collapsed",
            key=f"radio_{section_key}_{idx}",
        )

        if selected_label is not None:
            selected_score = dict(q["options"])[selected_label]
            st.session_state.responses[section_key][idx] = selected_score

        st.markdown("</div>", unsafe_allow_html=True)

    render_rotating_message_box(section["title"])

    col1, col2 = st.columns(2)

    with col1:
        if st.session_state.page_index > 1:
            if st.button("이전 페이지"):
                go_to_page(st.session_state.page_index - 1)

    with col2:
        next_label = "결과 보기" if st.session_state.page_index == 3 else "다음 페이지"
        if st.button(next_label, disabled=not all_answered(section_key)):
            if st.session_state.page_index < 3:
                go_to_page(st.session_state.page_index + 1)
            else:
                go_to_page(4)

# =========================================================
# 5페이지 결과 화면
# =========================================================
else:
    if not all_test_answered():
        st.warning("아직 응답하지 않은 문항이 있습니다. 이전 페이지로 돌아가 주세요.")
        if st.button("문항으로 돌아가기"):
            go_to_page(1)
        st.stop()

    result_key = get_result_key()
    result = RESULT_MAP[result_key]


    st.markdown("<div style='height:40px'></div>", unsafe_allow_html=True)

        
    love_score = get_section_score("love")
    grade_score = get_section_score("grade")
    campus_score = get_section_score("campus")

    st.markdown(
        f"""
        <div class="result-card">
            <div class="result-top">
                <div class="meta" style="color:#fff7fb; font-weight:700;">최종 진단 결과</div>
                <div class="title-xl">{result["title"]}</div>
                <div class="body-text" style="color:white; margin-top:10px;">{result["subtitle"]}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

    if result.get("image") and os.path.exists(result["image"]):
        img= Image.open(result["image"])
        
        col1, col2, col3 = st.columns([1,4,1])
        with col2:
            st.image(img, use_container_width=True)

    st.markdown(
        """
        <div class="info-card">
            <div class="section-title">영역별 점수</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(f"**연애 영역** · {love_score}점")
    st.progress(min(love_score / 100, 1.0))

    st.markdown(f"**성적 영역** · {grade_score}점")
    st.progress(min(grade_score / 100, 1.0))

    st.markdown(f"**대학생활 영역** · {campus_score}점")
    st.progress(min(campus_score / 100, 1.0))

    st.markdown(
        """
        <div class="info-card">
            <div class="section-title">결과 키워드</div>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown(
        "".join([f"<span class='keyword'>{word}</span>" for word in result["keywords"]]),
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="info-card">
            <div class="section-title">처방</div>
        </div>
        """,
        unsafe_allow_html=True
    )
    for line in result["prescription"]:
        st.markdown(f"- {line}")

    st.markdown(
        """
        <div class="score-box">
            <div class="section-title">판정 기준</div>
            <div class="body-text">
                각 영역 100점 만점 기준으로 70점 이상이면 해당 영역 위험 신호로 분류합니다.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)
    with col1:
        if st.button("다시 검사하기"):
            st.session_state.page_index = 0
            st.session_state.responses = {
                "love": [None] * 5,
                "grade": [None] * 5,
                "campus": [None] * 5,
            }
            st.rerun()
   
