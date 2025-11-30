#load_from_backend()-raw/clean(train)불러오기
#backend_summary.get_low_variance_and_vif_info-결측/저분산/상관관계/VIF 정보
#backend_summary.get_feature_importance()-최종 모델 기반 Feature Importance
#UI 구성만 수정 가능/ 계산 로직 수정 금지



import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

from src.backend import summary as backend_summary


st.set_page_config(
    page_title="데이터 요약",
    page_icon="📊",
    layout="wide"
)


# --- Backend 데이터를 불러오는 함수 ---
@st.cache_data
def load_from_backend():
    raw, clean = backend_summary.get_raw_and_clean(label_col="label")
    return raw, clean # 백엔드에서 raw_data(원본)와 clean_data(전처리 완료 데이터)를 한 번만 로딩하는 함수
                        #프론트는 이 함수 결과만 사용하면 되고, 파일 경로/전처리 로직은 백엔드에서 관리

raw_data, clean_data = load_from_backend()# 이 변수 2개만 가지고 아래에서 시각화


st.header("데이터 요약 (Data Summary)")# 이 페이지 제목(프론트에서 문구/스타일 변경 가능)


tab1, tab2, tab3 = st.tabs([
    "데이터 개요", #Tab1: 데이터 전체 요약
    "변수 제어(진단)", # Tab2: 결측/저분산/VIF 등 진단용
    "이상치 & 차원축소" #Tab3:이상치, t-SNE
])

# --- Tab 1: 데이터 개요 ---
with tab1:
    # 백엔드에서 계산된 데이터 요약 정보 (raw/train의 행 수, 컬럼 수, 결측치 개수 등)
    # ⚠️ 데이터 구조(키 이름)는 백엔드와 약속된 형태이므로 프론트에서 수정하지 않는 것이 좋습니다.
    overview = backend_summary.get_data_overview(label_col="label")
    label_info = backend_summary.get_label_distribution(label_col="label")

    raw_info = overview["raw"]
    tr_info = overview["train"]

    # NEW POSITION FOR LABEL DISTRIBUTION (DONUT CHART) SECTION
    st.markdown("#### 데이터 분포 (정상 vs 불량)")

    # 라벨 분포 계산 (clean_data 기준)
    label_counts = clean_data['label'].value_counts()

    # 정상/불량 라벨 키 자동 감지
    if -1 in label_counts.index:
        normal_key = -1
    elif 0 in label_counts.index:
        normal_key = 0
    else:
        normal_key = sorted(label_counts.index)[0]  # 예외 대비

    fail_key = 1  # 불량은 1로 고정

    # 파이 차트 값 준비 (정상 먼저, 불량 나중)
    pie_labels = [f'정상 ({normal_key})', '불량 (1)']
    values = [
        label_counts.get(normal_key, 0),
        label_counts.get(fail_key, 0)
    ]

    fig = go.Figure(data=[go.Pie(
        labels=pie_labels,
        values=values,
        hole=.4,
        marker_colors=['#2ca02c', '#d62728'] # COLOR CHANGE
    )])

    fig.update_layout(
        title_text='정상/불량 데이터 분포',# TEXT CHANGE: "라벨 분포" to "데이터 분포"
        annotations=[dict(
            text=f'총<br>{len(clean_data):,}',
            x=0.5, y=0.5,
            font_size=20,
            showarrow=False
        )]
    )

    st.plotly_chart(fig, use_container_width=True)

    # 비율 계산
    total = int(len(clean_data))
    pass_ratio = values[0] / total * 100 if total > 0 else 0.0
    fail_ratio = values[1] / total * 100 if total > 0 else 0.0

    # ✅ 안내문/경고도 Tab1 안에서만 표시
    st.info(
        f"정상({normal_key}) 클래스 비율이 약 **{pass_ratio:.2f}%**, "
        f"불량(1) 클래스 비율이 약 **{fail_ratio:.2f}%** 수준입니다."
    )

    if fail_ratio < 10:
        st.warning("클래스 불균형이 크므로 모델 학습 시 **별도 처리(예: SMOTE, 가중치 조절)**가 필요합니다.")
    
    st.markdown("---") # separator

    # NEW POSITION FOR DATA OVERVIEW SECTION
    st.markdown("#### 데이터 개요 (원본 데이터 vs 전처리 완료 데이터)") # Original heading

    col1, col2 = st.columns(2)

    # 왼쪽: Raw 요약
    with col1:
        st.markdown("### 📑 원본 데이터 요약")
        st.markdown(f"- Row 수: **{raw_info['rows']}**")
        st.markdown(f"- Column 수: **{raw_info['cols']}**")
        st.markdown(f"- 결측치 개수: **{raw_info['missing']}**")

    # 오른쪽: 전처리 요약 + 전처리 설명
    with col2:
        st.markdown("### ✨ 전처리 데이터 요약")
        st.markdown(f"- Row 수: **{tr_info['rows']}**")
        st.markdown(f"- Column 수: **{tr_info['cols']}**")
        st.markdown(f"- 결측치 개수: **{tr_info['missing']}**")
        
        # 백엔드에서 받은 라벨/카운트 (list -> dict 변환)
        labels = label_info["labels"]
        counts_list = label_info["counts"]
        counts = dict(zip(labels, counts_list))

        # 정상 라벨 자동 감지
        if -1 in counts:
            normal_key = -1
        elif 0 in counts:
            normal_key = 0
        else:
            normal_key = sorted(counts.keys())[0]

        fail_key = 1

        st.markdown(
            f"- 데이터 분포: **불량(1) {counts.get(fail_key, 0)}건 / 정상({normal_key}) {counts.get(normal_key, 0)}건**"
        )

        # ✅ expander는 전처리 요약 박스 안에 둠
    with st.expander("주요 전처리 내용 요약 보기"):

        # 실제 전처리 결과 가져오기 (Tab2에서도 쓰는 그 함수)
       lv_vif_info = backend_summary.get_low_variance_and_vif_info(using="mean")

       low_count = len(lv_vif_info.get("low_variance_removed", []))
       vif_count = len(lv_vif_info.get("vif_removed", []))


       st.markdown(f"""
        - 결측치 처리: 500개 이상의 결측치를 가진 행 제거
        - 수치형 변수: 평균(mean) 대치
        - 상수형/저분산 센서: **{low_count}개** 센서 제거
        - 상관관계 기반 제거: **92개** 센서 제거 (상관계수 > 0.95)
        - 다중공선성(VIF): VIF > 10 기준 **{vif_count}개** 센서 추가 제거
        """)


# --- Tab 2: 변수 제어 및 품질 진단 ---
with tab2:
    st.subheader("변수 제어 및 품질 진단")
    
    # --- 백엔드 데이터 로드 ---
    lv_vif_info = backend_summary.get_low_variance_and_vif_info(using="mean")
    sensors_after_missing = lv_vif_info.get("after_missing", [])
    low_variance_removed = lv_vif_info.get("low_variance_removed", [])
    sensors_after_low_variance = lv_vif_info.get("after_low_variance", [])

    # 상관관계 단계
    sensors_before_corr = lv_vif_info.get("before_corr", sensors_after_low_variance)
    sensors_after_corr  = lv_vif_info.get("after_corr", sensors_after_low_variance)
    corr_removed        = lv_vif_info.get("removed_corr", [])

    # VIF 단계
    vif_removed      = lv_vif_info.get("vif_removed", [])
    sensors_after_vif = lv_vif_info.get("after_vif", [])
    sensors_before_vif = lv_vif_info.get("before_vif", sensors_after_corr)

    st.markdown("---")

    # --- 1단계: 상수형 / 저분산 센서 탐색 ---
    st.markdown("### 1. 상수형 / 저분산 센서 탐색")
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"Before: {len(sensors_after_missing)}개")
        st.dataframe(pd.DataFrame(sensors_after_missing, columns=["센서 리스트"]), height=300)
    with col2:
        st.success(f"After: {len(sensors_after_low_variance)}개")
        st.dataframe(pd.DataFrame(sensors_after_low_variance, columns=["제거 후 센서 리스트"]), height=300)
    st.warning(f"총 {len(low_variance_removed)}개 센서가 제거되었습니다.")

    st.markdown("---")



# =============================================================================
# 2. 상관관계 기반 피처 필터링
# =============================================================================

    st.markdown("### 2. 상관관계 기반 피처 필터링")

    before_count = len(sensors_before_corr)
    after_count = len(sensors_after_corr)
    removed_count = len(corr_removed)

    col1, col2 = st.columns(2)

    with col1:
        # 👇 [수정] st.markdown -> st.info (파란색 박스)
        st.info(f"Before: {before_count}개")
        st.dataframe(
            pd.DataFrame({"센서 리스트": sensors_before_corr}),
            use_container_width=True,
            height=300, # 높이도 300으로 통일
        )

    with col2:
        # 👇 [수정] st.markdown -> st.success (초록색 박스)
        st.success(f"After: {after_count}개")
        st.dataframe(
            pd.DataFrame({"제거 후 센서 리스트": sensors_after_corr}),
            use_container_width=True,
            height=300, # 높이도 300으로 통일
        )

    # 👇 [수정] st.info -> st.warning (노란색 경고창)
    st.warning(f"총 {removed_count}개 센서가 제거되었습니다. (상관관계 > 0.95 기준)")

# --- 3단계: 다중공선성(VIF) 제거 ---
    st.markdown("### 3. 다중공선성(VIF) 제거")
    # VIF 단계의 Before는 상관관계 필터링 후의 After 리스트를 사용

    col1, col2 = st.columns(2)
    with col1:
        st.info(f"Before: {len(sensors_before_vif)}개")
        st.dataframe(pd.DataFrame(sensors_before_vif, columns=["센서 리스트"]), height=300)
    with col2:
        st.success(f"After: {len(sensors_after_vif)}개")
        st.dataframe(pd.DataFrame(sensors_after_vif, columns=["제거 후 센서 리스트"]), height=300)
    st.warning(f"총 {len(vif_removed)}개 센서가 제거되었습니다. (VIF > 10 기준)")




from sklearn.manifold import TSNE

# --- Tab 3(구 Tab 4)용 데이터 생성 함수 ---
@st.cache_data
def generate_tab4_data(raw_data: pd.DataFrame, clean_data: pd.DataFrame, label_col: str = "label"):
    # 1) IQR Boxplot용 대표 센서 선택 (clean_data 기준, 첫 번째 센서)
    numeric_cols = [c for c in clean_data.columns if c != label_col]
    sensor_to_check = numeric_cols[0] if numeric_cols else None

    if sensor_to_check is not None:
        series = clean_data[sensor_to_check].dropna()
        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)
        iqr_val = q3 - q1
        lower_bound = q1 - 1.5 * iqr_val
        upper_bound = q3 + 1.5 * iqr_val

        data_before_iqr = series
        # IQR 기준으로 클리핑(상하한 밖의 값은 경계값으로 잘라냄)
        data_after_iqr = series.clip(lower=lower_bound, upper=upper_bound)
    else:
        data_before_iqr = pd.Series([], dtype=float)
        data_after_iqr = pd.Series([], dtype=float)
        sensor_to_check = "N/A"

    # 2) Z-score 기반 이상치 개수 (clean_data 전체 센서 기준)
    num_df = clean_data.drop(columns=[label_col]).select_dtypes(include=["float64", "float32", "int64", "int32"])
    means = num_df.mean()
    stds = num_df.std(ddof=0).replace(0, np.nan)
    z = (num_df - means) / stds

    threshold = 3.0  # |z| > 3 기준
    outlier_counts = (z.abs() > threshold).sum()

    z_scores = (
        outlier_counts.sort_values(ascending=False)
        .head(10)
        .reset_index()
    )
    z_scores.columns = ["Sensor", "Z-score 이상치 개수"]

    # 3) 결측률 ≥ 0.4 컬럼 (raw_data 기준)
    missing_ratio = raw_data.isna().mean()
    missing_df = missing_ratio[missing_ratio >= 0.4].sort_values(ascending=False)

    if len(missing_df) > 0:
        missing_cols = missing_df.reset_index()
        missing_cols.columns = ["Column", "결측률"]
    else:
        # 고결측 컬럼이 없으면 빈 테이블 반환
        missing_cols = pd.DataFrame(columns=["Column", "결측률"])

    # 4) t-SNE (clean_data 기반, 필요 시 샘플링)
    X = clean_data.drop(columns=[label_col])
    y = clean_data[label_col]

    max_n = 2000
    if len(X) > max_n:
        X_sample = X.sample(n=max_n, random_state=42)
        y_sample = y.loc[X_sample.index]
    else:
        X_sample = X
        y_sample = y

    tsne = TSNE(n_components=2, perplexity=30, random_state=42)
    tsne_results = tsne.fit_transform(X_sample.values)

    tsne_df = pd.DataFrame(tsne_results, columns=["tsne-2d-one", "tsne-2d-two"])
    tsne_df["label"] = y_sample.values

    return sensor_to_check, data_before_iqr, data_after_iqr, z_scores, missing_cols, tsne_df

with tab3:
    st.subheader(" 이상치 & 차원축소")
    
    # --- 데이터 로드 ---
    sensor_to_check, data_before_iqr, data_after_iqr, z_scores, missing_cols, tsne_df = generate_tab4_data(
        raw_data, clean_data
    )

    st.markdown("---")

    # --- 섹션 1: 이상치 탐지 및 처리 (Outlier Detection) ---
    st.markdown("#### 1. 이상치 탐지 및 처리 (Outlier Detection)")
    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("##### IQR 기반 이상치 처리 예시")
        fig_iqr = go.Figure()
        fig_iqr.add_trace(go.Box(y=data_before_iqr, name="Before"))
        fig_iqr.add_trace(go.Box(y=data_after_iqr, name="After"))
        fig_iqr.update_layout(
            title_text=f"대표 센서({sensor_to_check}) 처리 전/후",
            yaxis_title="Sensor Value",
            height=400
        )
        st.plotly_chart(fig_iqr, use_container_width=True)
    
    with col2:
        st.markdown("##### Z-score 기반 이상치 상위 센서")
        st.dataframe(z_scores, height=400, use_container_width=True)
    
    st.info("IQR 및 Z-score를 활용하여 극단적인 이상치를 탐지하고, 데이터 분포를 안정화합니다.")

    st.markdown("---")

    # --- 섹션 2: 결측치 분석 (Missing Values) ---
    st.markdown("#### 2. 결측치 분석 (Missing Values)")
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("##### 전체 컬럼 결측률 분포")
        missing_ratios = raw_data.isna().mean()
        fig_missing = go.Figure()
        fig_missing.add_trace(go.Histogram(
            x=missing_ratios,
            name='결측률',
            marker_color='#636EFA',
            opacity=0.7
        ))
        fig_missing.add_vline(x=0.4, line_dash="dash", line_color="red", annotation_text="제거 기준선 (40%)")
        fig_missing.update_layout(
            title_text='전체 센서의 결측률 분포',
            xaxis_title='결측률 (Missing Ratio)',
            yaxis_title='컬럼 수 (Count)',
            bargap=0.1
        )
        st.plotly_chart(fig_missing, use_container_width=True)

    with col2:
        st.markdown("##### 결측률 40% 이상 컬럼")
        if len(missing_cols) > 0:
            st.dataframe(missing_cols, use_container_width=True)
        else:
            st.success("결측률 40% 이상인 컬럼이 없습니다.")
        st.warning("결측률이 높은 컬럼은 모델 학습에서 제외됩니다.")

    st.markdown("---")

    # --- 섹션 3: 차원 축소 및 분포 (Distribution Visualization) ---
    st.markdown("#### 3. 차원 축소 및 분포 시각화")
    
    fig_tsne = go.Figure()
    label_values = sorted(tsne_df["label"].unique())
    colors = ["#636EFA", "#EF553B", "#00CC96", "#AB63FA"]

    for label_val, color in zip(label_values, colors):
        subset = tsne_df[tsne_df["label"] == label_val]
        name = f"정상 ({label_val})" if label_val in [0, -1] else f"불량 ({label_val})"
        fig_tsne.add_trace(
            go.Scatter(
                x=subset["tsne-2d-one"],
                y=subset["tsne-2d-two"],
                mode="markers",
                name=name,
                marker=dict(color=color, size=6, opacity=0.7),
            )
        )
    
    fig_tsne.update_layout(
        title="t-SNE를 통한 2차원 분포 시각화",
        xaxis_title="t-SNE Dimension 1",
        yaxis_title="t-SNE Dimension 2",
        legend_title_text="Label",
    )
    st.plotly_chart(fig_tsne, use_container_width=True)

    st.info(
        "정상/불량 데이터가 t-SNE 상에서 구분되는지 확인하여 모델 학습 난이도를 가늠합니다."
    )