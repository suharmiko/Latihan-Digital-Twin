import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Digital Twin Risk Simulator",
    layout="wide"
)

st.title("Digital Twin Transformer Risk Simulator")
st.caption("Dashboard hasil simulasi dari Google Colab")

risk_results = pd.read_csv("scenario_risk_results.csv")
monte_carlo_summary = pd.read_csv("monte_carlo_summary.csv")

st.sidebar.header("Filter")

selected_unit = st.sidebar.selectbox(
    "Pilih Unit",
    risk_results["unit_name"].unique()
)

selected_result = risk_results[
    risk_results["unit_name"] == selected_unit
].iloc[0]

col1, col2, col3 = st.columns(3)

col1.metric(
    "Risk Score",
    f"{selected_result['risk_score']:.1f}"
)

col2.metric(
    "Loading",
    f"{selected_result['loading_pct_scenario']:.1f}%"
)

col3.metric(
    "Status",
    selected_result["risk_category"]
)

st.info(
    f"Top driver untuk {selected_unit}: "
    f"{selected_result['top_driver']}"
)

ranking = risk_results.sort_values(
    by="risk_score",
    ascending=False
)

fig_ranking = px.bar(
    ranking,
    x="unit_name",
    y="risk_score",
    color="risk_category",
    hover_data=[
        "transformer_id",
        "loading_pct_scenario",
        "status_scenario",
        "top_driver"
    ],
    title="Unit Risk Ranking"
)

st.plotly_chart(fig_ranking, use_container_width=True)

st.subheader("Scenario Risk Results")
st.dataframe(ranking, use_container_width=True)

st.subheader("Monte Carlo Summary")

fig_mc = px.bar(
    monte_carlo_summary.sort_values(
        by="p95",
        ascending=False
    ),
    x="unit_name",
    y=["mean_risk", "p80", "p95"],
    barmode="group",
    title="Monte Carlo Risk Summary"
)

st.plotly_chart(fig_mc, use_container_width=True)

st.dataframe(
    monte_carlo_summary.sort_values(
        by="p95",
        ascending=False
    ),
    use_container_width=True
)

with st.expander("Method Note"):
    st.write(
        """
        Dashboard ini membaca hasil simulasi dari file CSV yang dibuat di Google Colab.
        Jadi aplikasi Streamlit ini tidak menghitung ulang pandapower, tetapi hanya
        menampilkan hasil scenario risk dan Monte Carlo summary.
        """
    )
