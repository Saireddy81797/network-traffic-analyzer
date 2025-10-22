# app.py
import streamlit as st
import pandas as pd
import os

from src.packet_capture import simulate_live_packets
from src.packet_analysis import analyze_packets
from src.visualizer import plot_protocol_distribution, plot_bandwidth_over_time
from src.utils import filter_by_protocol, filter_by_ip

# ------------------- Page Config -------------------
st.set_page_config(page_title="Network Traffic Analyzer", page_icon="🛰️", layout="wide")

# ------------------- Styles -------------------
if os.path.exists("assets/styles.css"):
    with open("assets/styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ------------------- Header -------------------
if os.path.exists("assets/logo.png"):
    st.image("assets/logo.png", width=100)
st.title("🛰️ Network Traffic Analyzer & Performance Dashboard")
st.write("Monitor and visualize simulated real-time network packets — demo and simulated live capture modes.")

# ------------------- Sidebar Filters -------------------
st.sidebar.header("🔍 Filters")
protocol_choice = st.sidebar.selectbox(
    "Filter by Protocol",
    ["All", "TCP", "UDP", "HTTP", "HTTPS", "DNS", "SSH", "FTP", "ICMP"]
)
ip_filter = st.sidebar.text_input("Filter by IP (src or dst)")

mode = st.radio("Select Mode:", ["Demo (sample data)", "Live Capture (simulated)"])

# ------------------- Session State -------------------
if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame(columns=["timestamp", "src_ip", "dst_ip", "protocol", "length"])
if "running" not in st.session_state:
    st.session_state.running = False

# ------------------- Controls -------------------
col1, col2 = st.columns([1, 3])
with col1:
    duration = st.slider("Capture Duration (seconds)", 5, 60, 15)
    start = st.button("▶️ Start Capture")
    stop = st.button("⏹️ Stop")
with col2:
    st.markdown("### Controls")
    st.write("Choose Demo to load the sample CSV, or Live Capture (simulated) for streaming data.")

# ------------------- Start/Stop Capture -------------------
if start:
    st.session_state.running = True
    st.session_state.df = pd.DataFrame(columns=["timestamp", "src_ip", "dst_ip", "protocol", "length"])

if stop:
    st.session_state.running = False

# ------------------- Demo Mode -------------------
if mode == "Demo (sample data)":
    try:
        df_demo = pd.read_csv("data/sample_packets.csv")
        st.session_state.df = df_demo
    except Exception as e:
        st.error("Could not load sample_packets.csv: " + str(e))

# ------------------- Live Capture Mode -------------------
if mode == "Live Capture (simulated)" and st.session_state.running:
    placeholder_table = st.empty()
    protocol_chart = st.empty()
    bandwidth_chart = st.empty()
    progress_bar = st.progress(0)

    for i, df_live in enumerate(simulate_live_packets(duration)):
        st.session_state.df = df_live

        # Apply filters
        filtered = filter_by_protocol(st.session_state.df, protocol_choice)
        filtered = filter_by_ip(filtered, ip_filter)

        # Analysis
        summary, proto_summary = analyze_packets(filtered)

        # Display Network Summary
        with st.container():
            st.markdown("## Network Summary")
            st.json(summary)

        # Plots
        protocol_fig = plot_protocol_distribution(proto_summary)
        bandwidth_fig = plot_bandwidth_over_time(filtered)

        # Display tables and charts
        placeholder_table.dataframe(filtered.tail(15), use_container_width=True)
        if protocol_fig:
            protocol_chart.plotly_chart(protocol_fig, use_container_width=True)
        if bandwidth_fig:
            bandwidth_chart.plotly_chart(bandwidth_fig, use_container_width=True)

        # Progress bar
        progress_bar.progress((i + 1) / duration)
        if not st.session_state.running:
            break

    st.success("Simulated live capture finished or stopped.")

# ------------------- Static Dashboard -------------------
if not st.session_state.running:
    df_show = st.session_state.df.copy()
    filtered_df = filter_by_protocol(df_show, protocol_choice)
    filtered_df = filter_by_ip(filtered_df, ip_filter)

    summary, proto_summary = analyze_packets(filtered_df)

    st.markdown("## Network Summary")
    st.json(summary)

    # Plots side by side
    cols = st.columns(2)
    with cols[0]:
        st.markdown("### Protocol Usage")
        proto_fig = plot_protocol_distribution(proto_summary)
        if proto_fig:
            st.plotly_chart(proto_fig, use_container_width=True)
    with cols[1]:
        st.markdown("### Bandwidth Over Time")
        bw_fig = plot_bandwidth_over_time(filtered_df)
        if bw_fig:
            st.plotly_chart(bw_fig, use_container_width=True)

    # Raw packets table
    st.markdown("### Raw Packets (latest)")
    st.dataframe(filtered_df.tail(40), use_container_width=True)

    # ------------------- CSV Export -------------------
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download CSV",
        data=csv,
        file_name="network_traffic.csv",
        mime="text/csv"
    )

# ------------------- Future Enhancement -------------------
# TODO: Add anomaly detection flag (threshold-based alerts)

