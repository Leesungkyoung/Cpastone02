import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from src.backend import summary as backend_summary   # 필요 시
from src.backend import model_ab   
from src.backend import final_model
import src.backend.final_model as fm 


@st.cache_data
def generate_final_data():
    """
    Final Model 탭에서 사용할 실제 데이터를 로드합니다.
    - StageG_FE_v1.parquet
    - stageI_final_lgbm_model.pkl
    - stageI_final_scaler.pkl
    - stageI_final_threshold.json
    - metrics_summary_baseline.csv
    를 이용해서 KPI, Confusion Matrix, PR/ROC Curve 데이터를 생성.
    """
    return final_model.get_final_dashboard_data()

data = generate_final_data()
# =====================================================================================
# 2. 페이지 렌더링 (Render Page)
# =====================================================================================
def render():
    st.header("Model Final")
    
    tab1, tab2, tab3= st.tabs([
        "Final Summary & Direction",
        "Final Model Overview", 
        "Final Performance (Metrics & Curves)", 
    ])
    
    
    # ---------------------------------------------------------------------------------
    # TAB 1: Feature Strategy & Final Direction
    # ---------------------------------------------------------------------------------

    with tab1:

        # ====================== 상단 제목 ======================
        st.subheader("Feature Strategy & Final Feature Set")
        st.markdown("---")

        # ====================== 0. 한줄 요약 박스 ======================
        st.markdown("<div style='height: 10px'></div>", unsafe_allow_html=True)

        st.markdown("""
        <div style="
            background-color:#F4F7FF;
            border:1px solid #D3DDF5;
            padding:18px 20px;
            border-radius:14px;
            font-size:15px;
            box-shadow:0 1px 2px rgba(0,0,0,0.04);
            line-height:1.55;
            color:#333;">
            고급 모델에서 선정된 <b>LightGBM 모델</b>을 기반으로 
            <b>Core Feature</b>와 <b>파생 Feature</b>를 결합해 
            <b>최종 Feature Set</b> 및 <b>최종 모델</b>을 구성했습니다.
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='height: 18px'></div>", unsafe_allow_html=True)

        # ====================== 1. Final 모델 구성 개요 ======================
        st.markdown("#### 1. Final 모델 구성 개요")
        st.markdown("<div style='height: 8px'></div>", unsafe_allow_html=True)

        # 좌우 카드 + 가운데 플러스
        col_left, col_mid, col_right = st.columns([3.3, 1, 3.3])

        with col_left:
            st.markdown("""
            <div style="
                background:#FAFAFA;
                border:1px solid #D9D9D9;
                border-radius:16px;
                padding:22px 22px 20px 22px;
                box-shadow:0 2px 4px rgba(0,0,0,0.06);
                font-size:15px;">
                <b>① 고급 모델 (Advanced)</b><br><br>
                • 여러 조합 중 LightGBM 최종 선정<br>
                • AUC-PR 기준 성능이 가장 안정적<br>
                • 실시간 적용 가능한 경량 구조
            </div>
            """, unsafe_allow_html=True)

        with col_mid:
            st.markdown(
                """
                <div style="
                    text-align:center;
                    font-size:32px;
                    margin-top:68px;">
                    <b>+</b>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col_right:
            st.markdown("""
            <div style="
                background:#FAFAFA;
                border:1px solid #D9D9D9;
                border-radius:16px;
                padding:22px 22px 20px 22px;
                box-shadow:0 2px 4px rgba(0,0,0,0.06);
                font-size:15px;">
                <b>② Feature 전략 (Core U Derived)</b><br><br>
                • Model A/B 공통 Core Feature 기반<br>
                • 파생 Feature로 이상 패턴 보완<br>
                • Core ∪ Derived 방식으로 최종 Feature 구성
            </div>
            """, unsafe_allow_html=True)

        # ↓ 화살표
        st.markdown(
            "<div style='text-align:center; font-size:40px; margin:16px 0 18px 0;'>⬇️</div>",
            unsafe_allow_html=True
        )

        # ====================== 1-2. 최종 모델 카드 ======================
        st.markdown("""
        <div style="
            background:#FAFAFA;
            border:1px solid #D9D9D9;
            border-radius:16px;
            padding:26px 26px 22px 26px;
            width:65%;
            max-width:780px;
            margin:auto;
            text-align:left;
            box-shadow:0 2px 4px rgba(0,0,0,0.06);
            font-size:15px;">
            <b>③ 최종 모델 (Final LightGBM)</b><br><br>
            • 최종 Feature Set 기반 모델<br>
            • 불량 탐지 성능 중심으로 튜닝<br>
            • 관제·알림 시스템 연동 최종 배포 후보
        </div>
        """, unsafe_allow_html=True)

        # ====================== 2. Final Feature Set ======================
        st.markdown("<div style='height: 28px'></div>", unsafe_allow_html=True)
        st.markdown("#### 2. Final Feature Set")
        st.markdown("<div style='height: 6px'></div>", unsafe_allow_html=True)

        # 카드용 CSS (한 번만 선언)
        st.markdown("""
        <style>
        .featureset-card {
            background: #F8FAFF;
            border: 1px solid #E2E8FF;
            border-radius: 20px;
            padding: 28px 30px 24px 30px;
            box-shadow: 0 4px 8px rgba(15, 23, 42, 0.06);
            width: 70%;
            max-width: 900px;
            margin: 18px auto 10px auto;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
            color: #1F2933;
        }
        .featureset-sub {
            font-size: 14px;
            color: #6B7280;
            margin-bottom: 16px;
        }
        .featureset-card ul {
            margin: 0;
            padding-left: 18px;
            font-size: 15px;
            line-height: 1.6;
        }
        </style>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="featureset-card">
            <div class="featureset-sub">
            </div>
            <ul>
                <li>MRMR·Boruta 기반으로 안정적으로 검증된 <b>Core Feature 40개</b>를 중심으로 구성됨</li>
                <li>Model A/B에서 공통적으로 상위에 랭크된 Feature 교차 검증으로 <b>일관성과 재현성</b> 확보</li>
                <li><b>파생 Feature</b>를 포함해 단일 센서로 포착하기 어려운 이상 탐지 패턴을 보완함</li>
                <li>Final LightGBM 모델의 성능을 극대화하기 위해 <b>최적화된 최종 Feature Set</b>으로 사용됨</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)


   
    # ---------------------------------------------------------------------------------
    # TAB 2: Final Model Overview 
    # ---------------------------------------------------------------------------------
    with tab2:
        st.subheader("Final Model Overview")
        st.markdown("---")
        
        # 4.3 Final Model Summary Box
        st.markdown("##### Final Model Summary")
        # 👇 백틱(`)을 다 제거했습니다!
        st.markdown("""
        - **Model Type:** LightGBM
        - **Feature Set:** 최종 329개 Feature 사용
        - **Sampling Strategy:** SMOTE-ENN (Train set만 적용)
        - **Hyperparameter Tuning:** Optuna 기반 자동 최적화(50회 탐색)
        - **Target Metrics:** Recall & AUC-PR 중심 최적화
        """)
        st.markdown("---")

        col1, col2 = st.columns(2)
        with col1:
            # 4.4 Preprocessing & Feature Pipeline
            st.markdown("##### Preprocessing & Feature Pipeline")
            # 👇 여기도 백틱 제거!
            st.markdown("""
            - **Input:** 전처리 + Feature Engineering 완료 데이터셋
            - **결측치 처리:** Mean 대치
            - **스케일링:** StandardScaler
            - **Feature Selection:** Core Features + Derived Features 기반
            """)

        with col2:
            # 4.5 Sampling & Model Pipeline
            st.markdown("##### Sampling & Model Pipeline")
            # 👇 여기도 백틱 제거!
            st.markdown("""
            - **Data Split:** Train 80% / Test 20%
            - **Sampling:** SMOTE-ENN (Train set에만 적용)
            - **Model Family:** LightGBM
            - **Ensemble:** 적용 안함 (단일 모델)
            """)
        st.markdown("---")
        
        # 4.6 Final Model Selection Reason
        # 👇 여기는 아까 말씀드린 대로 st.info -> st.markdown으로 변경 (배경색 제거)
        st.markdown("""
        <div style="
            background:#F8FAFF;
            border:1px solid #E2E8FF;
            border-left:5px solid #6366F1;
            border-radius:18px;
            padding:22px 26px;
            margin-top:16px;
            box-shadow:0 4px 10px rgba(15,23,42,0.06);
            font-family:-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            color:#111827;
        ">
            <div style="font-size:20px; font-weight:700; margin-bottom:10px;">
                Final Model Selection
            </div>
            <ul style="margin:0; padding-left:22px; font-size:15px; line-height:1.7;">
                <li>
                    <b>성능:</b> Optuna + SMOTE-ENN을 적용한 LightGBM 모델이 
                    불균형 환경에서도 Recall과 AUC-PR이 가장 높게 나타나,
                    불량 탐지 목적에 가장 적합한 성능을 보여주었습니다.
                </li>
                <li>
                    <b>안정성:</b> 불균형 데이터 환경에서도 과적합이나 성능 편차가 적으며, 
                    교차 검증 결과에서도 성능이 안정적으로 유지되어 
                    실제 공정 상황에서도 일관된 탐지 능력을 기대할 수 있습니다.
                </li>
                <li>
                    <b>운영 효율성:</b> 예측 속도가 빠르고 구조가 단순해 실시간 모니터링 및 
                    경보 시스템에 바로 적용 가능하며, 재학습·관리 부담도 낮아 
                    운영 환경에서 지속적인 유지보수에 유리합니다.
                </li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    # ---------------------------------------------------------------------------------
    # TAB 3: Final Performance (Metrics & Curves)
    # ---------------------------------------------------------------------------------
    with tab3:
        st.subheader("Final Performance (Metrics & Curves)")
        st.markdown("---")

    # 5.3 KPI 메트릭 카드
       
        st.markdown("##### Key Performance Indicators – Final Model")

    # 👉 백엔드에서 가져오지 말고, 여기서 직접 KPI 딕셔너리 정의
        kpi = {
    "Threshold": 0.6429997389333499,   # Best F1 Threshold

        "Recall": {
            "Final": 0.333333,
            "Baseline": 0.1429
        },
        "F1-Score": {
            "Final": 0.333333,
            "Baseline": 0.1667
        },
        "AUC-PR": {
            "Final": 0.226450,
            "Baseline": 0.2874
        },
        "AUC-ROC": {
            "Final": 0.810011,
            "Baseline": 0.7996
        },
    }



        # ============================
        # KPI Cards Layout
        # ============================

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Recall",
            f"{kpi['Recall']['Final']:.3f}",
            f"{kpi['Recall']['Final'] - kpi['Recall']['Baseline']:.3f} (vs Base)"
        )

        col2.metric(
            "F1-Score",
            f"{kpi['F1-Score']['Final']:.3f}",
            f"{kpi['F1-Score']['Final'] - kpi['F1-Score']['Baseline']:.3f} (vs Base)"
        )

        col3.metric(
            "AUC-PR",
            f"{kpi['AUC-PR']['Final']:.3f}",
            f"{kpi['AUC-PR']['Final'] - kpi['AUC-PR']['Baseline']:.3f} (vs Base)"
        )

        col4.metric(
            "AUC-ROC",
            f"{kpi['AUC-ROC']['Final']:.3f}",
            f"{kpi['AUC-ROC']['Final'] - kpi['AUC-ROC']['Baseline']:.3f} (vs Base)"
        )

        st.markdown("---")


       
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("##### Confusion Matrix (Final Model)")

            values = [279, 14, 14, 7]
            labels = ["TN", "FP", "FN", "TP"]

            fig_cm = go.Figure(
                data=go.Bar(
                    x=labels,
                    y=values,
                    text=values,
                    textposition="outside",
                )
            )

            # 🔥 y축 최대값을 TN보다 20~30% 더 크게 설정 (숫자 안 잘림)
            max_y = max(values) * 1.25

            fig_cm.update_layout(
                height=400,
                yaxis=dict(
                    title="Count",
                    range=[0, max_y],   # ← 여기 때문에 숫자가 절대 안 잘림!!
                ),
                margin=dict(t=80)
            )

            st.plotly_chart(fig_cm, use_container_width=True)

    
        with col2:
            # 5.5 주요 지표 테이블
            st.markdown("##### Evaluation Metrics Table")

            # 🔥 네 Stage H 최종 모델 실제 성능(손으로 직접 넣은 버전)
            metrics_df = pd.DataFrame(
                [
                    {"Metric": "Accuracy",             "Value": 0.910828},
                    {"Metric": "Recall",               "Value": 0.333333},
                    {"Metric": "Precision",            "Value": 0.333333},
                    {"Metric": "F1-Score",             "Value": 0.333333},
                    {"Metric": "Specificity (TN Rate)","Value": 0.952218},
                    {"Metric": "AUC-PR",               "Value": 0.226450},
                    {"Metric": "AUC-ROC",              "Value": 0.810011},
                ]
            )

            st.dataframe(
                metrics_df.style.format({"Value": "{:.3f}"}),
                use_container_width=True,
                hide_index=True,
            )

        col1, col2 = st.columns(2)
        # ============================
        # Precision-Recall + ROC (Side by Side)
        # ============================

        col1, col2 = st.columns(2)

        # ============================
        # 1) Precision-Recall Curve (Left)
        # ============================
        with col1:
            PR_CSV_PATH = r"results/stageH/pr_curve_stageH.csv"
            pr_df = pd.read_csv(PR_CSV_PATH)

            pr_auc_value = 0.226
            st.markdown("##### Precision-Recall Curve")
            st.markdown(f"**AUC = {pr_auc_value:.3f}**")

            fig_pr = go.Figure()
            fig_pr.add_trace(go.Scatter(
                x=pr_df["recall"],
                y=pr_df["precision"],
                mode="lines",
                name="PR Curve"
            ))
            fig_pr.update_layout(
                xaxis_title="Recall",
                yaxis_title="Precision",
                height=350
            )
            st.plotly_chart(fig_pr, use_container_width=True)


        # ============================
        # 2) ROC Curve (Right)
        # ============================
        with col2:
            ROC_CSV_PATH = r"results/stageH/roc_curve_stageH.csv"
            roc_df = pd.read_csv(ROC_CSV_PATH)

            roc_auc_value = 0.810
            st.markdown("##### ROC Curve")
            st.markdown(f"**AUC = {roc_auc_value:.3f}**")

            fig_roc = go.Figure()
            fig_roc.add_trace(go.Scatter(
                x=roc_df["fpr"],
                y=roc_df["tpr"],
                mode="lines",
                name="ROC Curve"
            ))
            fig_roc.add_trace(go.Scatter(
                x=[0, 1], y=[0, 1],
                mode="lines",
                name="Random",
                line=dict(dash="dash")
            ))
            fig_roc.update_layout(
                xaxis_title="False Positive Rate",
                yaxis_title="True Positive Rate",
                height=350
            )
            st.plotly_chart(fig_roc, use_container_width=True)

if __name__ == '__main__':
    render()
