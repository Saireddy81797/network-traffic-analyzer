# app.py
import streamlit as st
import pandas as pd
from src.packet_capture import capture_packets
from src.packet_analysis import analyze_packets
from src.visualizer import plot_protocol_distribution

st.set_page_config(page_title="Network Traffic Analyzer", layout="wide")

st.title("🛰️ Network Traffic Analyzer & Performance Dashboard")
st.markdown("Monitor and visualize real-time network packets in your local environment.")

duration = st.slider("Capture Duration (seconds)", 5, 60, 10)
if st.button("Start Capture"):
    with st.spinner("Capturing packets..."):
        df = capture_packets(duration)
        if df.empty:
            st.warning("No packets captured. Try increasing the duration.")
        else:
            summary, proto_summary = analyze_packets(df)

            st.subheader("📊 Network Summary")
            st.json(summary)

            st.subheader("📡 Protocol Usage")
            fig = plot_protocol_distribution(proto_summary)
            if fig:
                st.plotly_chart(fig, use_container_width=True)

            st.subheader("🧾 Raw Packet Data")
            st.dataframe(df)
