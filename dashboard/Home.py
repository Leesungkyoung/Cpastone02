import sys
from pathlib import Path
import streamlit as st
import graphviz

ROOT_DIR = Path(__file__).resolve().parents[1]

if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))
    
# 페이지 설정 - 넓은 레이아웃
st.set_page_config(
    page_title="Zero Q Factory - 랜딩 페이지",
    page_icon="🏭",
    layout="wide"
)

# CSS를 사용하여 카드 스타일 및 전반적인 디자인 개선
st.markdown("""
<style>
    /* 기본 폰트 및 배경 색상 설정 */
    .stApp {
        background-color: #FFFFFF;
    }

    /* 카드 스타일 */
    .card {
        background-color: #F8F9FA;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        transition: box-shadow 0.3s ease-in-out;
        height: 100%; /* 카드 높이 통일 */
    }
    .card:hover {
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
    }
    .card h3 {
        color: #007BFF; /* Problem 타이틀 색상 */
        margin-bottom: 15px;
        font-size: 1.5em;
    }
    .card h4 {
        font-size: 1.2em;
        color: #17A2B8;
    }
    .card .solution {
        color: #28A745; /* Solution 타이틀 색상 */
        font-weight: bold;
    }

    /* 키워드 배지 스타일 */
    .keyword-badge {
        display: inline-block;
        background-color: #E0E0E0;
        color: #333;
        padding: 5px 12px;
        border-radius: 15px;
        margin: 5px;
        font-size: 0.9em;
        font-weight: 500;
    }

    /* 섹션 제목 구분선 */
    hr.section-divider {
        margin-top: 40px;
        margin-bottom: 40px;
        border: 0;
        border-top: 2px solid #EEEEEE;
    }

    h1, h2, h3 {
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)


# --- Section 1: Hero Section ---
with st.container():
    st.title("Zero Q Factory")
    st.subheader("SECOM 데이터 기반 실시간 불량 탐지 및 스마트팩토리 최적화 솔루션")

    keywords = ["불균형 데이터 해결", "실시간 스트리밍", "경량화 모델"]
    st.markdown(
        " ".join([f'<span class="keyword-badge">{kw}</span>' for kw in keywords]),
        unsafe_allow_html=True
    )



st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

# --- Section 2: Project Background (Why & Solution) ---
st.header("Project Background: 기존 제조 현장의 문제점과 해결책")
st.write("기존 사후 검수 방식의 한계를 극복하고, 데이터 기반의 선제적 불량 탐지를 통해 스마트 팩토리의 비전을 제시합니다.")

cols = st.columns(3)
problems_solutions = [
    {
        "problem": "데이터 불균형",
        "problem_desc": "불량률 6.6% 미만의 극심한 데이터 불균형으로 인해 모델이 정상 데이터에 편중되어 학습되는 문제가 있었습니다.",
        "solution": "2-Stage Feature Selection과 SMOTE-ENN 오버샘플링을 적용하여 데이터 구조를 최적화하고 모델의 일반화 성능을 높였습니다."
    },
    {
        "problem": "실시간성 부재",
        "problem_desc": "전통적인 품질 검사는 사후에 이루어져 불량 발생 시 즉각적인 원인 파악과 대응이 어려웠습니다.",
        "solution": "Firebase-Streamlit으로 이어지는 실시간 파이프라인을 구축하여, 평균 1.8초 내에 불량 예측 결과를 시각화합니다."
    },
    {
        "problem": "고비용/저효율",
        "problem_desc": "복잡하고 무거운 분석 모델은 높은 컴퓨팅 자원을 요구하며, 비전문가가 해석하고 활용하기 어려웠습니다.",
        "solution": "LightGBM 기반의 경량화 모델을 채택하고, 직관적인 관제 UI를 제공하여 누구나 쉽게 사용 가능한 솔루션을 구현했습니다."
    }
]

for i, ps in enumerate(problems_solutions):
    with cols[i]:
        st.markdown(f"""
        <div class="card">
            <h3>Problem: {ps['problem']}</h3>
            <p>{ps['problem_desc']}</p>
            <hr>
            <p class="solution">Solution:</p>
            <p>{ps['solution']}</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

# --- Section 3: System Architecture ---
st.header("How it works: 시스템 아키텍처")
st.write("센서 데이터 수집부터 불량 탐지, 최종 결과 시각화까지의 전 과정을 자동화된 파이프라인으로 구성했습니다.")

# Graphviz를 사용하여 데이터 흐름도 생성
graph = graphviz.Digraph()
graph.attr('node', shape='box', style='rounded,filled', fillcolor='#E3F2FD', fontname='sans-serif', fontsize='11')
graph.attr('edge', fontname='sans-serif', fontsize='10')
graph.attr(rankdir='LR') # Left to Right layout

graph.node('A', '[Input]\n센서 로그 수집\n(Firebase)')
graph.node('B', '[Process]\n전처리/샘플링\n(Feature Selection, SMOTE-ENN)')
graph.node('C', '[Model]\n불량 탐지\n(LightGBM)')
graph.node('D', '[Output]\n관제/ROI\n(Streamlit)')

graph.edge('A', 'B', label='데이터 스트리밍')
graph.edge('B', 'C', label='최적화된 데이터셋')
graph.edge('C', 'D', label='예측 결과')

st.graphviz_chart(graph)

st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

# --- Section 3.5: Core Engine ---
st.header("Core Engine: 최종 모델 명세")
st.write("수많은 실험과 검증을 통해 선정된 Zero Q Factory의 최종 불량 탐지 모델과 핵심 최적화 기법입니다.")

cols = st.columns(2)
with cols[0]:
    st.markdown("""
    <div class="card">
        <h4>🤖 Model: LightGBM (Booster)</h4>
        <p>대용량 공정 데이터 처리에 최적화된 경량화 모델. 기존 무거운 모델 대비 연산 비용 절감 및 높은 정확도 보장.</p>
        <span class="keyword-badge">Hyperparameter Tuning</span>
        <span class="keyword-badge">Bayesian Optimization</span>
        <span class="keyword-badge">Target Metric: Recall & AUC-PR</span>
    </div>
    """, unsafe_allow_html=True)

with cols[1]:
    st.markdown("""
    <div class="card">
        <h4>🛠️ Optimization Strategy</h4>
        <ol>
            <li style="margin-bottom: 10px;"><b>SMOTE-ENN Sampling:</b><br>데이터 불균형 해소 및 경계면 노이즈 제거</li>
            <li style="margin-bottom: 10px;"><b>2-Stage Feature Selection:</b><br>Lasso(L1) + RF Importance로 590개 중 핵심 인자 도출</li>
            <li><b>Real-time Inference:</b><br>평균 추론 속도 3.2ms 달성 (실시간 관제 충족)</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

# --- Section 4: Key Achievements ---
st.header("Key Achievements: 수치로 증명된 성과")
st.write("본 프로젝트를 통해 달성한 핵심 성과 지표는 다음과 같습니다.")

cols = st.columns(4)
metrics = {
    "Recall (재현율)": ("87.0%", "+20%p vs Baseline"),
    "ROI (투자수익률)": ("285.7%", "18개월 내 회수"),
    "검사 시간 단축": ("~67%", "15분 → 5분"),
    "불량률 감소": ("~71%", "10.5% → 3.0% (시뮬레이션)")
}

# st.metric은 delta 부호에 따라 색이 바뀌므로, 긍정적 지표는 +로 표시
fixed_metrics = {
    "Recall (재현율)": ("87.0%", "+20.0%p"),
    "ROI (투자수익률)": ("285.7%", "긍정"),
    "검사 시간 단축": ("-67%", "감소"),
    "불량률 감소": ("-71.4%", "감소")
}

# st.metric은 delta_color='off' 옵션이 없어서 직접 HTML로 구성
for i, (label, (value, delta_text)) in enumerate(metrics.items()):
    with cols[i]:
        st.markdown(f"""
        <div class="card metric-card">
            <div class="label">{label}</div>
            <div class="value">{value}</div>
            <div style="color: #28A745; font-size: 0.9em;">{delta_text}</div>
        </div>
        """, unsafe_allow_html=True)


st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

# --- Section 5: Analytics Hub ---
st.header("Analytics Hub: 분석 모듈 바로가기")
st.write("관심 있는 분석 주제를 선택하여 더 깊이 있는 인사이트를 탐색해 보세요. (사이드바 메뉴 활용)")

analytics_hubs = {
    "📊 데이터 요약": "원천 데이터 구조 및 전처리 전략 확인",
    "🤖 모델 비교": "Baseline vs Advanced 성능 비교",
    "✨ 최종 모델": "최적 모델 성능 및 임계값 조정",
    "💰 ROI 분석": "비용 절감 효과 및 운영 시나리오"
}

# 2x2 그리드
row1 = st.columns(2)
row2 = st.columns(2)
rows = row1 + row2

for i, (title, desc) in enumerate(analytics_hubs.items()):
    with rows[i]:
        st.markdown(f"""
        <div class="card">
            <h4>{title}</h4>
            <p>{desc}</p>
        </div>
        """, unsafe_allow_html=True)


st.markdown("---")
st.write("© 2025 Zero Q Factory. All Rights Reserved.")
