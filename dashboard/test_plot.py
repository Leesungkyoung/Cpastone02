import streamlit as st
import plotly.graph_objects as go

st.set_page_config(layout="wide")
st.title("그래프 표시 테스트")

st.markdown("---")
st.markdown("### Plotly 그래프 테스트")
st.markdown("아래에 막대 그래프가 보인다면, Streamlit과 Plotly 라이브러리 자체는 정상적으로 동작하는 것입니다.")

try:
    # 간단한 막대 그래프 생성
    fig = go.Figure(
        data=[go.Bar(x=['A', 'B', 'C'], y=[10, 20, 15])],
        layout_title_text="테스트용 막대 그래프"
    )
    
    # Streamlit에 그래프 표시
    st.plotly_chart(fig, use_container_width=True)
    
    st.success("테스트 그래프가 성공적으로 렌더링되었습니다.")
    
except Exception as e:
    st.error(f"그래프를 렌더링하는 중 오류가 발생했습니다: {e}")
