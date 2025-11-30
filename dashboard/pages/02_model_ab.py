import streamlit as st
st.set_page_config(layout="wide")

import pandas as pd
import numpy as np
import plotly.graph_objects as go
from pathlib import Path

from src.backend import model_ab
from src.backend import summary as backend_summary  # 필요하면

# =====================================================================================
# 1. 데이터 생성 (Dummy Data Generation)
# =====================================================================================
@st.cache_data
def generate_model_ab_data():
    # --- Feature Analysis Tab Data ---
    # 🔥 Feature Importance (Lasso vs RandomForest) — 실제 Top-40 결과 사용
    feat_dict = model_ab.get_feature_importance_top40()
    importance_lasso = feat_dict["lasso"]   # pd.DataFrame
    importance_rf = feat_dict["rf"]         # pd.DataFrame

    # 실제 안정성 점수 사용
    stability_scores = model_ab.get_stability_scores()

    # ==========================================================
    # --- Baseline Model Tab Data (진짜 CSV 결과 사용) ---
    #   Model A : capstone02_project_final 쪽 결과
    #   Model B : capstone02_project(성경) 쪽 결과
    # ==========================================================
    # Model A 경로 (Median + RobustScaler 파이프라인)
    BASE_DIR = Path(__file__).resolve().parents[2]
    path_model_a = BASE_DIR / "results" / "final" / "metrics_summary_baseline.csv"

    # Model B 경로 (Mean + StandardScaler 파이프라인)
    path_model_b = BASE_DIR / "results" / "final" / "metrics_summary_baseline(mean).csv"

    df_a = pd.read_csv(path_model_a)
    df_b = pd.read_csv(path_model_b)

    # 히트맵에 사용할 모델 / 샘플링 순서 (baseline 노트북에서 쓰던 순서 기준)
    models_order = ["DecisionTree", "LinearSVM", "LogisticRegression"]
    sampling_order = ["RUS", "SMOTE", "SMOTE+Tomek"]

    def make_heatmaps_one_model(df: pd.DataFrame):
        """한 파이프라인(df)에 대해 Recall / F1 / AUC-PR 히트맵 3개 생성"""
        def _pivot(metric_col: str) -> pd.DataFrame:
            pivot = (
                df.pivot(index="Model", columns="Sampling", values=metric_col)
                  .loc[models_order, sampling_order]
            )
            return pivot

        return {
            "Recall": _pivot("Recall"),
            "F1-score": _pivot("F1"),
            "AUC-PR": _pivot("AUC_PR"),
        }

    # Model A / B용 히트맵 데이터
    heatmaps_a = make_heatmaps_one_model(df_a)
    heatmaps_b = make_heatmaps_one_model(df_b)

    # 👉 Baseline 성능 요약용 (각 파이프라인에서 F1이 가장 높은 조합 하나씩 선택)
    def summarize_best_row(df: pd.DataFrame):
        best = df.loc[df["F1"].idxmax()]
        return {
            "Recall": float(best["Recall"]),
            "F1": float(best["F1"]),
            "AUC-PR": float(best["AUC_PR"]),
        }

    sum_a = summarize_best_row(df_a)
    sum_b = summarize_best_row(df_b)

    baseline_perf = pd.DataFrame({
        "Metric": ["Recall", "F1-Score", "AUC-PR"],
        "Model A": [sum_a["Recall"], sum_a["F1"], sum_a["AUC-PR"]],
        "Model B": [sum_b["Recall"], sum_b["F1"], sum_b["AUC-PR"]],
    })

        # --- Advanced Model Tab Data (요약용: 두 파이프라인 최적 조합 비교) ---
    # baseline에서 뽑은 최적 조합(sum_a, sum_b)을 Advanced 탭 요약에도 재사용
    advanced_perf = pd.DataFrame({
        "Metric": ["Recall", "F1-Score", "AUC-PR"],
        "Model A": [sum_a["Recall"], sum_a["F1"], sum_a["AUC-PR"]],
        "Model B": [sum_b["Recall"], sum_b["F1"], sum_b["AUC-PR"]],
    })


          # Model A / B용 히트맵 데이터
    heatmaps_a = make_heatmaps_one_model(df_a)
    heatmaps_b = make_heatmaps_one_model(df_b)

    # 👉 탭2(불균형 처리 히트맵)에서 기본으로 사용할 3×3 히트맵은 Model A 기준으로 사용
    heatmap_recall = heatmaps_a["Recall"]      # 3×3 DataFrame
    heatmap_f1 = heatmaps_a["F1-score"]        # 3×3 DataFrame
    heatmap_aucpr = heatmaps_a["AUC-PR"]       # 3×3 DataFrame
 


    experiment_setup = pd.DataFrame([
        {"Category": "Feature Selection", "Method": "Top-60 + mRMR", "Details": "Top-40에서 추가 확장하여 모델 안정성과 재현율 향상 시도"},
        {"Category": "Sampling", "Method": "SMOTE-ENN", "Details": "과샘플링+언더샘플링 혼합으로 경계부 노이즈 제거 및 분리도 향상"},
        {"Category": "Model", "Method": "LightGBM", "Details": "불균형 데이터 및 수치형 Feature에 강점, 빠른 학습 속도"},
        {"Category": "Tuning", "Method": "Bayesian Optimization", "Details": "주요 하이퍼파라미터를 효율적으로 탐색하여 최적 조합 발견"},
    ])

    return {
        # 탭1용
        "importance_lasso": importance_lasso,
        "importance_rf": importance_rf,
        "stability_scores": stability_scores,
        # 탭2 히트맵용 (Model 선택 + 지표 선택에 따라 쓸 거)
        "baseline_heatmap_a": heatmaps_a,
        "baseline_heatmap_b": heatmaps_b,
        # 탭2 요약바 / metric 카드용
        "baseline_perf": baseline_perf,
        "advanced_perf": advanced_perf,
        # 탭3
        "experiment_setup": experiment_setup,
        "heatmap_recall": heatmap_recall,
        "heatmap_f1": heatmap_f1,
        "heatmap_aucpr": heatmap_aucpr,
    }


data = generate_model_ab_data()

# =====================================================================================
# 2. 페이지 렌더링
# =====================================================================================
def render():
    st.header("Model A & Model B")
    
    tab1, tab2, tab3 = st.tabs([
        "Feature Analysis", 
        "Baseline Model", 
        "Advanced Model"
    ])

    # ---------------------------------------------------------------------------------
    # TAB 1: Feature Analysis
    # ---------------------------------------------------------------------------------
    with tab1:
        st.subheader("Feature Analysis")
        st.markdown("Lasso와 RandomForest 기반 Feature 중요도와 안정성을 비교하여 핵심 Feature들을 분석합니다.")
        st.markdown("---")
        
        # --- Layout: 2x2 Grid ---
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("##### Feature Importance (Lasso vs RandomForest)")
            
            # Selectbox for controlling other charts
            importance_method = st.selectbox(
                "Feature Importance 기준 (옆 'Top-10' 차트에 적용)", 
                ["Lasso", "RandomForest"]
            )

            # Side-by-side bar charts
            sub_col1, sub_col2 = st.columns(2)

            with sub_col1:
                df_lasso = data['importance_lasso'].head(20).sort_values('importance', ascending=True)
                fig_lasso = go.Figure(go.Bar(
                    x=df_lasso['importance'],
                    y=df_lasso['feature'],
                    orientation='h',
                    name='Lasso',
                    marker=dict(color='indianred'),
                    text=df_lasso['importance'],        # 막대에 값 라벨
                    textposition='outside'              # 막대 바깥에 표시
                ))

                fig_lasso.update_layout(
                    title='Lasso Importance',
                    height=400,
                    margin=dict(l=10, r=10, t=30, b=10),
                    plot_bgcolor="white",               # 그래프 배경
                    paper_bgcolor="rgba(0,0,0,0)",      # 바깥 배경(투명)
                    xaxis=dict(
                        showline=True,
                        linewidth=1,
                        linecolor="black"
                    ),
                    yaxis=dict(
                        showline=True,
                        linewidth=1,
                        linecolor="black",
                        showticklabels=True           # 기존처럼 센서 이름은 오른쪽 큰 그래프에서만
                    )
                )

                fig_lasso.update_xaxes(
                    tickmode="linear",
                    tick0=0,
                    dtick=1,                            # 0,1,2,3,4,5 눈금
                    showgrid=True,
                    gridwidth=1
                )

                st.plotly_chart(fig_lasso, use_container_width=True)

        with sub_col2:
            df_rf = data['importance_rf'].head(20).sort_values('importance', ascending=True)
            fig_rf = go.Figure(go.Bar(
                x=df_rf['importance'],
                y=df_rf['feature'],
                orientation='h',
                name='RandomForest',
                marker=dict(color='lightsalmon'),
                text=df_rf['importance'],           # 라벨
                textposition='outside'
            ))

            fig_rf.update_layout(
                title='RandomForest Importance',
                height=400,
                margin=dict(l=10, r=10, t=30, b=10),
                plot_bgcolor="white",
                paper_bgcolor="rgba(0,0,0,0)",
                xaxis=dict(
                    showline=True,
                    linewidth=1,
                    linecolor="black"
                ),
                yaxis=dict(
                    showline=True,
                    linewidth=1,
                    linecolor="black"
                )
            )

            fig_rf.update_xaxes(
                tickmode="linear",
                tick0=0,
                dtick=1,
                showgrid=True,
                gridwidth=1
            )

            st.plotly_chart(fig_rf, use_container_width=True)
        

            

        st.success("💡 **Top-40 Feature Set**이 모델 성능과 안정성 간 최적 균형을 제공함을 확인했습니다.")

        # ✅ 1행 오른쪽: Top-10 그래프
        with col2:
            st.markdown(f"##### Top-10 Influential Sensors (Based on **{importance_method}**)")

            if importance_method == "Lasso":
                top_10_df = data['importance_lasso'].head(10)
            else:
                top_10_df = data['importance_rf'].head(10)

            top_10_df = top_10_df.sort_values('importance', ascending=True)

            fig_top10 = go.Figure(go.Bar(
                x=top_10_df['importance'],
                y=top_10_df['feature'],
                orientation='h',
                # 중요도가 높을수록 색이 진해지게
                marker=dict(
                    color=top_10_df['importance'],
                    colorscale="Blues"
                ),
                text=top_10_df['importance'],
                textposition='outside'
            ))

            fig_top10.update_layout(
                title=f'{importance_method} 기반 상위 10개 센서',
                xaxis_title='Importance (count 기반)',
                yaxis_title='Sensor ID',
                height=500,
                plot_bgcolor="white",
                paper_bgcolor="rgba(0,0,0,0)",
                xaxis=dict(
                    showline=True,
                    linewidth=1,
                    linecolor="black"
                ),
                yaxis=dict(
                    showline=True,
                    linewidth=1,
                    linecolor="black"
                )
            )

            fig_top10.update_xaxes(
                tickmode="linear",
                tick0=0,
                dtick=1,
                showgrid=True,
                gridwidth=1
            )

            st.plotly_chart(fig_top10, use_container_width=True)

        # ✅ 1행 아래 구분선
        st.markdown("---")

        # ✅ 2행: 안정성 점수 분포 (전체 폭)
        st.markdown("##### Feature Stability Score (Lasso vs RandomForest)")

        fig_stability = go.Figure()

        # Lasso Boxplot
        fig_stability.add_trace(go.Box(
            y=data['stability_scores']['Lasso'],
            name='Lasso',
            marker_color='royalblue',
            boxmean=True   # 평균선 표시
        ))

        # RandomForest Boxplot
        fig_stability.add_trace(go.Box(
            y=data['stability_scores']['RandomForest'],
            name='RandomForest',
            marker_color='lightskyblue',
            boxmean=True
        ))

        fig_stability.update_layout(
            title_text="안정성 점수 분포 비교",
            yaxis_title="Stability Score",
            height=450,
            plot_bgcolor="white",
            paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=20, r=20, t=50, b=20)
        )

        st.plotly_chart(fig_stability, use_container_width=True)

        st.info(
            "RandomForest는 Lasso보다 안정성 점수가 높아 더 일관적으로 Feature를 선택하는 경향을 보입니다."
        )

    # ---------------------------------------------------------------------------------
    # TAB 2: Baseline Model
    # ---------------------------------------------------------------------------------
    with tab2:
        st.subheader("Baseline Model")
        st.markdown("Model A와 B의 Baseline 성능을 다양한 관점에서 비교 분석합니다.")
        st.markdown("---")

        st.markdown("###  Baseline 실험 설계 (Experiment Setup)")
        st.write("")

        # --- 카드 스타일 CSS (Advanced에서 이미 선언했으면 생략 가능) ---
        st.markdown("""
        <style>
        .info-card {
            background-color: #ffffff;
            padding: 18px 20px;
            border-radius: 12px;
            box-shadow: 0px 2px 6px rgba(0,0,0,0.08);
            margin-bottom: 12px;
            border-left: 6px solid #4A90E2;
        }
        .info-title {
            font-weight: 700;
            font-size: 16px;
            margin-bottom: 6px;
        }
        .info-text {
            font-size: 14px;
            line-height: 1.5;
        }
        </style>
        """, unsafe_allow_html=True)

        # ------- 1줄 (데이터 분할 / 불균형 처리) -------
        bcol1, bcol2 = st.columns(2)

        with bcol1:
            st.markdown("""
            <div class="info-card">
                <div class="info-title">① 데이터 분할 방식</div>
                <div class="info-text">
                    • Train 80% / Test 20% (Hold-out, random_state=42)<br>
                    • numpy / sklearn 등 주요 난수 연산에 동일한 시드(42)를 적용
                </div>
            </div>
            """, unsafe_allow_html=True)

        with bcol2:
            st.markdown("""
            <div class="info-card">
                <div class="info-title">② 불균형 처리 기법</div>
                <div class="info-text">
                    • RUS<br>
                    • SMOTE<br>
                    • SMOTE + Tomek Links
                </div>
            </div>
            """, unsafe_allow_html=True)

        # ------- 2줄 (평가 지표 / 비교 모델) -------
        bcol3, bcol4 = st.columns(2)

        with bcol3:
            st.markdown("""
            <div class="info-card">
                <div class="info-title">③ 평가 지표</div>
                <div class="info-text">
                    • Recall<br>
                    • F1-score<br>
                    • AUC-PR
                </div>
            </div>
            """, unsafe_allow_html=True)

        with bcol4:
            st.markdown("""
            <div class="info-card">
                <div class="info-title">④ 비교 모델</div>
                <div class="info-text">
                    • Logistic Regression<br>
                    • Linear SVM<br>
                    • Decision Tree
                </div>
            </div>
            """, unsafe_allow_html=True)


        # ---------------------------------------
        # 1행: Model Summary + Heatmap
        # ---------------------------------------
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("##### 모델 요약 (Model Summary)")
            selected_baseline_model = st.selectbox("모델 선택", ["Model A", "Model B"])
            
            if selected_baseline_model == "Model A":
                st.markdown("""
                - **Scaling:** RobustScaler  
                - **Model Type:** LogisticRegression  
                - **주요 전처리 파이프라인:** Median Imputation → Robust Scaling → Feature Top-40 선택  
                - **모델 장점:** 이상치에 덜 민감하여 센서 분포가 치우친 환경에서도 성능이 안정적입니다. 재학습 시 스케일 변화에 강인해 로버스트한 Baseline 모델로 활용 가능합니다.  
                - **모델 한계:** 평균 정보를 활용하지 않아 완만한 변동을 세밀하게 반영하는 데는 다소 불리할 수 있고, RobustScaler 사용으로 StandardScaler 대비 해석이 직관적이지 않을 수 있습니다.  
                """)
            else:
                st.markdown("""
                - **Scaling:** StandardScaler  
                - **Model Type:** LogisticRegression  
                - **주요 전처리 파이프라인:** Mean Imputation → Standard Scaling → Feature Top-40 선택  
                - **모델 장점:** 구조가 단순하고 계산 비용이 적으며, 선형 관계 해석에 용이합니다. 평균·분산 기반 StandardScaler를 사용해 해석이 직관적입니다.  
                - **모델 한계:** 이상치에 민감하여 센서 값에 큰 튀는 값이 존재할 때 성능이 불안정해질 수 있고, 복잡한 비선형 관계를 충분히 표현하는 데 한계가 있습니다.  
                """)

        with col2:
            st.markdown("##### 불균형 처리 기법별 모델 성능 비교")

            # 📌 1) 지표 선택 UI
            metric = st.selectbox("지표 선택", ["F1-score", "Recall", "AUC-PR"])

            # 📌 2) 모델 선택값에 따라 히트맵 그룹 선택
            if selected_baseline_model == "Model A":
                heatmap_dict = data["baseline_heatmap_a"]
            else:
                heatmap_dict = data["baseline_heatmap_b"]

            # 📌 3) 모델 + 지표 조합으로 히트맵 선택
            heatmap_df = heatmap_dict[metric]

            # 📌 4) 히트맵 출력
            fig_heatmap = go.Figure(data=go.Heatmap(
                z=heatmap_df.values,
                x=heatmap_df.columns,
                y=heatmap_df.index,
                colorscale='Blues',
                text=heatmap_df.applymap(lambda x: f'{x:.3f}'),
                texttemplate="%{text}",
                textfont={"size": 12}
            ))

            fig_heatmap.update_layout(
                title=f'{metric} 기준 성능 히트맵 ({selected_baseline_model})',
                height=300
            )

            st.plotly_chart(fig_heatmap, use_container_width=True)


        # ---------------------------------------
        # 구분선
        # ---------------------------------------
        st.markdown("---")

        # ---------------------------------------
        # 2행: Bar Chart + Summary Metrics
        # ---------------------------------------
       

        # ==============================
        # 🔹 Baseline Model A vs B 섹션
        # ==============================

        # 0) Baseline 성능 데이터 & 그래프 준비 (레이아웃 바깥에서 먼저)
        baseline_perf = data["baseline_perf"]  # Metric, Model A, Model B 컬럼 있음

        # --- 막대 그래프 생성 ---
        fig_baseline = go.Figure()
        for model_name in ["Model A", "Model B"]:
            fig_baseline.add_trace(
                go.Bar(
                    x=baseline_perf["Metric"],
                    y=baseline_perf[model_name],
                    name=model_name,
                    text=[f"{v:.3f}" for v in baseline_perf[model_name]],
                    textposition="auto",
                )
            )

        fig_baseline.update_layout(
            barmode="group",
            xaxis_title="Metric",
            yaxis_title="Score",
            legend_title="Model",
            height=350,
        )

        # --- Metric 값 꺼내고 증감 계산 ---
        def get_metric(metric_name):
            row = baseline_perf[baseline_perf["Metric"] == metric_name].iloc[0]
            a = float(row["Model A"])
            b = float(row["Model B"])
            return a, b

        recall_a, recall_b = get_metric("Recall")
        f1_a, f1_b = get_metric("F1-Score")
        auc_a, auc_b = get_metric("AUC-PR")

        def diff_and_rate(a, b):
            diff = b - a
            rate = (diff / a * 100) if a != 0 else 0.0
            return diff, rate

        rec_diff, rec_rate = diff_and_rate(recall_a, recall_b)
        f1_diff, f1_rate = diff_and_rate(f1_a, f1_b)
        auc_diff, auc_rate = diff_and_rate(auc_a, auc_b)

        # 1) 이전 섹션과의 간격
        st.markdown("<div style='margin-top:40px'></div>", unsafe_allow_html=True)

        # 2) 제목 줄 (왼쪽/오른쪽)
        title_col1, title_col2 = st.columns([1.2, 1])

        with title_col1:
            st.markdown("### Baseline Model A vs Model B Performance")

        with title_col2:
            st.markdown("### Performance Summary – Baseline")

        # 3) 내용 줄 (왼쪽: 그래프, 오른쪽: metric 카드)
        col1, col2 = st.columns([1.2, 1])

        # 🔸 왼쪽: 그래프
        with col1:
            st.markdown("<div style='margin-top:20px'></div>", unsafe_allow_html=True)
            st.plotly_chart(fig_baseline, use_container_width=True)

        # 🔸 오른쪽: metric 카드 + Best Combination
        with col2:
            # 👉 세로로 하나씩 나열하던 metric은 삭제하고, 가로 3개만 사용
            c1, c2_, c3 = st.columns(3)

            with c1:
                st.metric(
                    label="Recall (Baseline)",
                    value=f"{recall_b:.3f}",
                    delta=f"{rec_diff:+.3f} ({rec_rate:+.1f}%)"
                )

            with c2_:
                st.metric(
                    label="F1-Score (Baseline)",
                    value=f"{f1_b:.3f}",
                    delta=f"{f1_diff:+.3f} ({f1_rate:+.1f}%)"
                )

            with c3:
                st.metric(
                    label="AUC-PR (Baseline)",
                    value=f"{auc_b:.3f}",
                    delta=f"{auc_diff:+.3f} ({auc_rate:+.1f}%)"
                )

            st.write("")  # 여백

            # === 여기가 Performance Summary – Baseline 3개 metric 밑 ===
            st.markdown("### 🏆 Baseline Best Combination 요약")

            col_a, col_b = st.columns(2)

            with col_a:
                st.markdown(
                    """
                    <div style='background:#F8FAFF; padding:18px 20px; border-radius:12px;
                                border:1px solid #E1ECFF; box-shadow:0 2px 6px rgba(0,0,0,0.03);'>
                    <h4 style='margin:0 0 6px;'>Model A (Baseline)</h4>
                    <p style='margin:0 0 4px;'><b>Best 조합:</b> RUS + DecisionTree</p>
                    <ul style='margin:8px 0 0 18px; padding:0;'>
                        <li><b>Recall:</b> 0.6667</li>
                        <li><b>F1-Score:</b> 0.1830</li>
                        <li><b>AUC-PR:</b> 0.0930</li>
                    </ul>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            with col_b:
                st.markdown(
                    """
                    <div style='background:#FFF8F2; padding:18px 20px; border-radius:12px;
                                border:1px solid #FFE0C2; box-shadow:0 2px 6px rgba(0,0,0,0.03);'>
                    <h4 style='margin:0 0 6px;'>Model B (Baseline)</h4>
                    <p style='margin:0 0 4px;'><b>Best 조합:</b> RUS + LinearSVM</p>
                    <ul style='margin:8px 0 0 18px; padding:0;'>
                        <li><b>Recall:</b> 0.8095</li>
                        <li><b>F1-Score:</b> 0.2411</li>
                        <li><b>AUC-PR:</b> 0.2142</li>
                    </ul>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                st.divider()  # 👈 가로선 긋기
                
            # 5) 한 줄 요약 Insight
        st.info(
                "Baseline 조건에서 Model B는 Recall, F1-score, AUC-PR 전 지표에서 "
                "Model A 대비 성능 향상을 보입니다. 특히 AUC-PR은 약 "
                f"{auc_rate:.1f}% 증가하여 불균형 데이터 환경에서 더 안정적인 예측 성능을 제공합니다."
            )


        # 🔽 결론 아래로 내리기
        st.markdown("<div style='margin-top:60px;'></div>", unsafe_allow_html=True)

    # ---------------------------------------------------------------------------------
    # TAB 3: Advanced Model
    # ---------------------------------------------------------------------------------
    with tab3:
        st.subheader("Advanced Model")
        st.markdown("Baseline 대비 Advanced 모델의 구성과 성능을 분석하고, 최종 결론을 도출합니다.")
        st.markdown("---")

        st.markdown("###  Advanced Model 실험 설계 (Experiment Setup)")
        st.write("")

        # CSS 스타일 (카드 UI)
        st.markdown("""
        <style>
        .info-card {
            background-color: #ffffff;
            padding: 18px 20px;
            border-radius: 12px;
            box-shadow: 0px 2px 6px rgba(0,0,0,0.08);
            margin-bottom: 12px;
            border-left: 6px solid #4A90E2;
        }
        .info-title {
            font-weight: 700;
            font-size: 16px;
            margin-bottom: 6px;
        }
        .info-text {
            font-size: 14px;
            line-height: 1.5;
        }
        </style>
        """, unsafe_allow_html=True)

        # ------- 1줄 -------
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("""
            <div class="info-card">
                <div class="info-title">① 데이터 분할</div>
                <div class="info-text">
                    • Train 80% / Test 20%<br>
                    • random_state = 42
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("""
            <div class="info-card">
                <div class="info-title">② 전처리 방식</div>
                <div class="info-text">
                    • Model A: Median + RobustScaler<br>
                    • Model B: Mean + StandardScaler
                </div>
            </div>
            """, unsafe_allow_html=True)

        # ------- 2줄 -------
        col3, col4 = st.columns(2)

        with col3:
            st.markdown("""
            <div class="info-card">
                <div class="info-title">③ 불균형 처리 기법</div>
                <div class="info-text">
                    • RUS<br>
                    • SMOTE<br>
                    • SMOTE + Tomek Links
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col4:
            st.markdown("""
            <div class="info-card">
                <div class="info-title">④ 모델 종류</div>
                <div class="info-text">
                    • RandomForest<br>
                    • LightGBM<br>
                    • XGBoost<br>
                    • CatBoost
                </div>
            </div>
            """, unsafe_allow_html=True)

        # ------- 3줄 -------
        col5, col6 = st.columns(2)

        with col5:
            st.markdown("""
            <div class="info-card">
                <div class="info-title">⑤ 평가 지표</div>
                <div class="info-text">
                    • Recall<br>
                    • F1-score<br>
                    • AUC-PR
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col6:
            st.markdown("""
            <div class="info-card">
                <div class="info-title">⑥ 최종 선정 기준</div>
                <div class="info-text">
                    • 1순위: AUC-PR<br>
                    • 2순위: F1-score
                </div>
            </div>
            """, unsafe_allow_html=True)


        # ============================================================
        # 🔹 Advanced Model – 불균형 처리/모델별 성능 히트맵 (Model A vs B)
        # ============================================================
        BASE_DIR = Path(__file__).resolve().parents[2]

        # 1) CSV 불러오기 (고급 모델 Stage D 결과)
        path_a = r"C:\Users\seo58\OneDrive\바탕 화면\capstone02_project_final\capstone02_project\results\stageD\holdout_metrics_summary.csv"
        path_b = r"C:\Users\seo58\OneDrive\바탕 화면\capstone02_project_final\capstone02_project\results\stageD\advanced_results_youngeun.csv"

        df_a = pd.read_csv(path_a)  # Model A (median pipeline)
        df_b = pd.read_csv(path_b)  # Model B (mean pipeline)

        # Model B 쪽은 컬럼명이 Sampler라서 Sampling으로 통일
        df_b = df_b.rename(columns={"Sampler": "Sampling"})

        # 🔹 AUC-PR 기준 고급 모델 Best Combination (A, B 각각)
        best_a = df_a.sort_values("AUC_PR", ascending=False).iloc[0]
        best_b = df_b.sort_values("AUC_PR", ascending=False).iloc[0]

        # 🔹 Performance Summary – Advanced 에서 쓸 요약 테이블
        advanced_perf_df = pd.DataFrame({
            "Metric": ["Recall", "F1-Score", "AUC-PR"],
            "Model A": [best_a["Recall"], best_a["F1"], best_a["AUC_PR"]],
            "Model B": [best_b["Recall"], best_b["F1"], best_b["AUC_PR"]],
        })

        # 2) 지표 선택 (F1 / Recall / AUC-PR 히트맵)
        metric_label_map = {
            "Recall": "Recall",
            "F1-score": "F1",
            "AUC-PR": "AUC_PR",
        }

        selected_label = st.selectbox(
            "지표 선택",
            list(metric_label_map.keys()),
            index=1,   # 기본값: F1-score
        )
        metric_col = metric_label_map[selected_label]

        st.markdown(f"#### {selected_label} 기준 성능 히트맵 (Model A vs Model B)")

        # 3) 피벗테이블 만들기 (행=Sampling, 열=Model)
        pivot_a = df_a.pivot(index="Sampling", columns="Model", values=metric_col)
        pivot_b = df_b.pivot(index="Sampling", columns="Model", values=metric_col)

        # 4) 두 히트맵이 같은 색 범위를 쓰도록 min/max 공통 설정
        zmin = min(pivot_a.min().min(), pivot_b.min().min())
        zmax = max(pivot_a.max().max(), pivot_b.max().max())

        # ==========================
        # 좌우 2열 레이아웃 (히트맵)
        # ==========================
        col_left, col_right = st.columns(2)

        # 왼쪽: Model A 히트맵
        with col_left:
            st.markdown("##### Model A")

            fig_a = go.Figure(
                data=go.Heatmap(
                    z=pivot_a.values,
                    x=pivot_a.columns.tolist(),     # 모델들
                    y=pivot_a.index.tolist(),       # Sampling 방법
                    colorscale="Blues",
                    zmin=zmin,
                    zmax=zmax,
                    text=np.round(pivot_a.values, 3),
                    texttemplate="%{text}",
                    colorbar=dict(title=selected_label),
                )
            )
            fig_a.update_layout(
                height=600,
                margin=dict(l=60, r=40, t=60, b=80),
                xaxis_title="Model",
                yaxis_title="Sampling Method",
                coloraxis_colorbar=dict(
                    len=0.8,
                    thickness=15,
                )
            )

            st.plotly_chart(fig_a, use_container_width=True)

        # 오른쪽: Model B 히트맵
        with col_right:
            st.markdown("##### Model B")

            fig_b = go.Figure(
                data=go.Heatmap(
                    z=pivot_b.values,
                    x=pivot_b.columns.tolist(),
                    y=pivot_b.index.tolist(),
                    colorscale="Blues",
                    zmin=zmin,
                    zmax=zmax,
                    text=np.round(pivot_b.values, 3),
                    texttemplate="%{text}",
                    colorbar=dict(title=selected_label),
                )
            )
            fig_b.update_layout(
                height=600,
                margin=dict(l=40, r=60, t=60, b=80),
                xaxis_title="Model",
                yaxis_title="Sampling Method",
                coloraxis_colorbar=dict(
                    len=0.8,
                    thickness=15,
                )
            )

            st.plotly_chart(fig_b, use_container_width=True)

        # ============================================================
        # 🔹 Advanced 성능 요약 (라인그래프 + 카드 + Best Combination)
        # ============================================================

        col1, col2 = st.columns(2)

        # ⬅️ 왼쪽: Advanced 성능 Line Chart (A vs B)
        with col1:
            st.markdown("##### Advanced Model – A vs B Performance")

            fig_adv_perf = go.Figure()

            # Model A Line
            fig_adv_perf.add_trace(go.Scatter(
                x=advanced_perf_df['Metric'],
                y=advanced_perf_df['Model A'],
                mode='lines+markers',
                name='Model A (Adv)',
                line=dict(color='darkgrey', width=3),
                marker=dict(size=10)
            ))

            # Model B Line
            fig_adv_perf.add_trace(go.Scatter(
                x=advanced_perf_df['Metric'],
                y=advanced_perf_df['Model B'],
                mode='lines+markers',
                name='Model B (Adv)',
                line=dict(color='royalblue', width=3),
                marker=dict(size=10)
            ))

            fig_adv_perf.update_layout(
                title='Advanced 성능 비교 (AUC-PR 기준 Best 조합)',
                yaxis_title='Score',
                xaxis_title='Metric',
                height=450,
                legend=dict(orientation="h", yanchor="bottom", y=-0.3),
                margin=dict(l=60, r=20, t=60, b=80)
            )        
            
            st.plotly_chart(fig_adv_perf, use_container_width=True)

        # ➡️ 오른쪽: Metric 카드 요약 + Best Combination 카드
        with col2:
            st.markdown("##### Performance Summary – Advanced")
            st.write("")

            perf_pivot = advanced_perf_df.set_index('Metric')

            recall_a_adv = float(perf_pivot.loc['Recall',   'Model A'])
            recall_b_adv = float(perf_pivot.loc['Recall',   'Model B'])
            f1_a_adv     = float(perf_pivot.loc['F1-Score', 'Model A'])
            f1_b_adv     = float(perf_pivot.loc['F1-Score', 'Model B'])
            auc_a_adv    = float(perf_pivot.loc['AUC-PR',   'Model A'])
            auc_b_adv    = float(perf_pivot.loc['AUC-PR',   'Model B'])

            # 증감 계산 (B - A)
            def diff_rate(a, b):
                diff = b - a
                rate = (diff / a * 100) if a != 0 else 0.0
                return diff, rate

            rec_diff, rec_rate = diff_rate(recall_a_adv, recall_b_adv)
            f1_diff,  f1_rate  = diff_rate(f1_a_adv,     f1_b_adv)
            auc_diff, auc_rate = diff_rate(auc_a_adv,    auc_b_adv)

            c1, c2_m, c3 = st.columns(3)

            with c1:
                st.metric(
                    label="Recall (Advanced)",
                    value=f"{recall_b_adv:.3f}",
                    delta=f"{rec_diff:+.3f} ({rec_rate:+.1f}%)"
                )

            with c2_m:
                st.metric(
                    label="F1-Score (Advanced)",
                    value=f"{f1_b_adv:.3f}",
                    delta=f"{f1_diff:+.3f} ({f1_rate:+.1f}%)"
                )

            with c3:
                st.metric(
                    label="AUC-PR (Advanced)",
                    value=f"{auc_b_adv:.3f}",
                    delta=f"{auc_diff:+.3f} ({auc_rate:+.1f}%)"
                )

            st.write("")  # Summary와 Best 조합 사이 여백

            # 🏆 Advanced Best Combination 요약 (여기 추가!)
            st.markdown("### 🏆 Advanced Best Combination 요약")
            st.write("")

            bc1, bc2 = st.columns(2)

            # Model A 카드
            with bc1:
                st.markdown("""
                <div style="
                    background-color:#F6F9FF;
                    padding:20px;
                    border-radius:16px;
                    border:1px solid #E0E6F5;
                    ">
                    <h4>Model A (Advanced)</h4>
                    <p><b>Best 조합 (AUC-PR 기준):</b> LightGBM + SMOTE</p>
                    <ul>
                        <li><b>Recall:</b> 0.238</li>
                        <li><b>F1-Score:</b> 0.303</li>
                        <li><b>AUC-PR:</b> 0.302</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)

            # Model B 카드
            with bc2:
                st.markdown("""
                <div style="
                background-color:#FFF7EB;
                padding:20px;
                border-radius:16px;
                border:1px solid #F3E0B8;
                ">
                <h4>Model B (Advanced)</h4>
                <p><b>Best 조합 (AUC-PR 기준):</b> LightGBM + SMOTE+Tomek</p>
                <ul>
                    <li><b>Recall:</b> 0.190</li>
                    <li><b>F1-Score:</b> 0.276</li>
                    <li><b>AUC-PR:</b> 0.218</li>
                </ul>
            </div>


                """, unsafe_allow_html=True)



        # ============================================================
        # Conclusion
        # ============================================================
            
        st.markdown("### Conclusion – Advanced Model")
        st.write("")

        con_col1, con_col2 = st.columns(2)

        # ---------------- 기술적 성과 ----------------
        with con_col1:
            st.markdown("""
            <div style='background-color:#E9F5E9; padding:18px; border-radius:10px; border-left:6px solid #7BC47F;'>
            <h4>기술적 성과 (Technical Achievements)</h4>
            <ul>
                <li><b>모델 비교 결과</b>: LGBM + SMOTE 조합이 AUC-PR 기준 가장 안정적 성능을 보였습니다.</li>
                <li><b>불균형 데이터 대응</b>: SMOTE·SMOTE+Tomek 적용 시 일부 개선 효과가 있었으나, 절대 성능은 기대 수준에는 미치지 못했습니다.</li>
                <li><b>운영 안정성</b>: LightGBM 모델은 가벼운 구조로 일관된 결과를 제공하며 운영 효율성이 높았습니다.</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)

        # ---------------- 비즈니스 임팩트 ----------------
        with con_col2:
            st.markdown("""
            <div style='background-color:#FFF9E6; padding:18px; border-radius:10px; border-left:6px solid #E2C275;'>
            <h4>비즈니스 임팩트 (Business Impact)</h4>
            <ul>
                <li><b>리스크 최소화</b>: Recall 유지력은 확보했지만 절대 수치가 낮아 추가 성능 개선이 필요한 것으로 판단됩니다.</li>
                <li><b>비용 절감</b>: 모델 구조는 실시간 모니터링 환경에 적합하지만, 오탐·미탐 개선 여지가 존재합니다.</li>
                <li><b>향후 적용성</b>: 고급 모델 결과를 기반으로 <b>파생 피처 + Model A/B Core Feature Union 기반 재학습 전략</b>을 Stage Final에서 적용하여 실사용 성능 확보를 목표로 진행했습니다.</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)

if __name__ == '__main__':
    render()    
    