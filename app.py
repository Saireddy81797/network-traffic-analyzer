# app.py
import streamlit as st
import pandas as pd
import platform
import os

from src.packet_analysis import analyze_packets
from src.visualizer import plot_protocol_distribution
from src.utils import filter_by_protocol, filter_by_ip

# Try importing packet capture (Scapy)
try:
    from src.packet_capture import capture_packets
    SCAPY_AVAILABLE = True
except Exception:
    SCAPY_AVAILABLE = False

# Page setup
st.set_page_config(page_title="🛰️ Network Traffic Analyzer", layout="wide")
with open("assets/styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.image("assets/logo.png", width=80)
st.title("🛰️ Network Traffic Analyzer & Performance Dashboard")
st.markdown("Monitor and visualize real-time network packets in your local environment.")

# Check environment
running_on_cloud = os.getenv("STREAMLIT_RUNTIME") is not None or not SCAPY_AVAILABLE

mode = st.radio("Select Mode:", ["Demo (sample data)", "Live Capture"])
if running_on_cloud:
    st.info("⚠️ Running on Streamlit Cloud — live packet sniffing is disabled. Demo mode only.")
    mode = "Demo (sample data)"

duration = st.slider("Capture Duration (seconds)", 5, 60, 10)

if st.button("Start Analysis"):
    if mode == "Demo (sample data)":
        df = pd.read_csv("data/sample_packets.csv")
    else:
        try:
            with st.spinner("Capturing packets..."):
                df = capture_packets(duration)
        except PermissionError:
            st.error("❌ Permission denied: Live capture not supported in this environment. Use Demo mode.")
            st.stop()
        except Exception as e:
            st.error(f"⚠️ Error: {e}")
            st.stop()

    if df.empty:
        st.warning("No packets captured or loaded.")
    else:
        # Sidebar filters
        st.sidebar.header("🔍 Filters")
        protocol = st.sidebar.selectbox("Filter by Protocol", ["All", "TCP", "UDP", "ICMP"])
        ip_filter = st.sidebar.text_input("Filter by IP (optional)")

        if protocol != "All":
            df = filter_by_protocol(df, protocol)
        if ip_filter:
            df = filter_by_ip(df, ip_filter)

        # Analysis
        summary, proto_summary = analyze_packets(df)
        st.subheader("📊 Network Summary")
        st.json(summary)

        st.subheader("📡 Protocol Usage")
        fig = plot_protocol_distribution(proto_summary)
        if fig:
            st.plotly_chart(fig, use_container_width=True)

        st.subheader("🧾 Raw Packet Data")
        st.dataframe(df, use_container_width=True)
